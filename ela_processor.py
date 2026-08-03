"""
Validador Multimodal de Comprobantes de Nequi (Forense ELA + Estructura Visual de Plantilla)
Detecta tanto aplicaciones falsas/clonadas (diseño incorrecto) como ediciones en Photoshop (ELA).
"""

import os
from io import BytesIO
from PIL import Image, ImageChops, ImageEnhance, ImageStat
import numpy as np

# Rango de color oficial del marco verde menta del QR en Nequi
# RGB aprox: R in [100, 160], G in [190, 255], B in [160, 225]
MINT_RGB_MIN = np.array([90, 180, 150])
MINT_RGB_MAX = np.array([175, 255, 235])

def calcular_ela_adaptativo(img_pil, calidad=92, factor_escala=12):
    """Calcula el mapa forense de error de compresión ELA."""
    img_rgb = img_pil.convert("RGB")
    buf = BytesIO()
    img_rgb.save(buf, format="JPEG", quality=calidad)
    buf.seek(0)
    recomprimida = Image.open(buf)
    
    dif = ImageChops.difference(img_rgb, recomprimida)
    stat = ImageStat.Stat(dif)
    std_dev = np.mean(stat.stddev)
    
    extremos = dif.getextrema()
    max_dif = max([ex[1] for ex in extremos]) or 1
    factor = factor_escala * (255.0 / (max_dif + std_dev * 2.0))
    return ImageEnhance.Brightness(dif).enhance(factor)

def validar_estructura_oficial_nequi(img_pil):
    """
    Analiza la estructura visual del comprobante para verificar si coincide con el diseño
    oficial de Nequi (QR superior con marco verde menta y fondo claro) o si es una App Falsa.
    """
    img_rgb = img_pil.convert("RGB")
    arr = np.array(img_rgb)
    alto, ancho, _ = arr.shape
    
    razones_fraude = []
    score_estructura = 1.0 # 1.0 = 100% auténtico en diseño, 0.0 = Falso
    
    # 1. Análisis del tercio superior (Zona del encabezado / QR)
    tercio_sup = arr[0:int(alto * 0.35), :]
    
    # Detectar si hay un banner morado/oscuro gigante en la parte superior (típico de Apps Falsas de Nequi antiguas)
    # R: 70-130, G: 20-60, B: 100-180
    mask_morado = (tercio_sup[:, :, 0] > 60) & (tercio_sup[:, :, 0] < 150) & \
                  (tercio_sup[:, :, 1] < 70) & \
                  (tercio_sup[:, :, 2] > 90) & (tercio_sup[:, :, 2] < 200)
    pct_morado_sup = np.mean(mask_morado)
    
    if pct_morado_sup > 0.25:
        razones_fraude.append(f"Detectado banner morado arcaico/falso ({pct_morado_sup*100:.1f}% de la cabecera). La app oficial actual usa fondo blanco.")
        score_estructura = 0.0
        return False, score_estructura, razones_fraude
        
    # 2. Detección del Código QR con marco verde menta (#84E4BD)
    # Buscamos píxeles verde menta en la región superior central
    mask_menta = (tercio_sup[:, :, 0] >= MINT_RGB_MIN[0]) & (tercio_sup[:, :, 0] <= MINT_RGB_MAX[0]) & \
                 (tercio_sup[:, :, 1] >= MINT_RGB_MIN[1]) & (tercio_sup[:, :, 1] <= MINT_RGB_MAX[1]) & \
                 (tercio_sup[:, :, 2] >= MINT_RGB_MIN[2]) & (tercio_sup[:, :, 2] <= MINT_RGB_MAX[2])
    n_pixeles_menta = np.sum(mask_menta)
    
    # En el comprobante oficial, el marco del QR tiene miles de píxeles verde menta
    tiene_marco_qr = n_pixeles_menta > 300
    
    if not tiene_marco_qr:
        razones_fraude.append("Ausencia del código QR oficial con marco verde menta (#84E4BD) en la cabecera.")
        score_estructura = min(score_estructura, 0.15)
        
    # 3. Dominancia del fondo claro (debe ser >65% blanco/gris claro en el comprobante real)
    mask_fondo_claro = (arr[:, :, 0] > 220) & (arr[:, :, 1] > 220) & (arr[:, :, 2] > 220)
    pct_fondo_claro = np.mean(mask_fondo_claro)
    
    if pct_fondo_claro < 0.45:
        razones_fraude.append(f"Distribución de color no corresponde al comprobante oficial (Fondo claro: {pct_fondo_claro*100:.1f}%).")
        score_estructura = min(score_estructura, 0.20)
        
    es_diseno_valido = len(razones_fraude) == 0
    return es_diseno_valido, score_estructura, razones_fraude

def analizar_discrepancia_monto(img_pil):
    """Evalúa si hay recorte/pegado en el monto mediante varianza ELA."""
    ela_img = calcular_ela_adaptativo(img_pil)
    arr = np.array(ela_img, dtype=np.float32)
    alto, ancho, _ = arr.shape
    
    y1, y2 = int(alto * 0.45), int(alto * 0.60)
    x1, x2 = int(ancho * 0.10), int(ancho * 0.90)
    
    m_monto = np.mean(arr[y1:y2, x1:x2])
    m_resto = np.mean(np.concatenate([arr[0:y1, :], arr[y2:, :]], axis=0))
    return m_monto / (m_resto + 1e-5), ela_img

def diagnostico_completo_comprobante(img_pil, modelo_cnn=None, transform=None, device="cpu"):
    """
    Pipeline Multimodal Completo:
    1. Validador de Plantilla y Estructura Oficial (QR, colores, cabecera).
    2. Validador Forense ELA y Discrepancia Local (Photoshop, parches).
    3. Inferencia de Red Neuronal Convolucional.
    """
    # 1. Validación de Estructura
    es_diseno_valido, score_est, razones = validar_estructura_oficial_nequi(img_pil)
    ratio_disc, img_ela = analizar_discrepancia_monto(img_pil)
    
    if not es_diseno_valido:
        # Es fraude por app falsa o diseño apócrifo
        prob_fraude = 0.99
        tipo_dictamen = "FRAUDE [APP FALSA / DISEÑO APÓCRIFO]"
        detalles = razones
        return prob_fraude, tipo_dictamen, detalles, img_ela
        
    # Si la estructura es válida, verificamos si fue editada digitalmente (Photoshop)
    prob_cnn = 0.1
    if modelo_cnn is not None and transform is not None:
        import torch
        t_input = transform(img_ela).unsqueeze(0).to(device)
        with torch.no_grad():
            prob_cnn = torch.sigmoid(modelo_cnn(t_input)).item()
            
    if ratio_disc >= 1.45 or prob_cnn >= 0.60:
        prob_fraude = max(prob_cnn, 0.92)
        tipo_dictamen = "FRAUDE [EDICIÓN DIGITAL DETECTADA EN MONTO/FECHA]"
        detalles = [f"Discrepancia ELA anormal en zona de transacción: {ratio_disc:.2f}x"]
    else:
        prob_fraude = min(prob_cnn * 0.2, 0.05)
        tipo_dictamen = "AUTÉNTICO [COMPROBANTE OFICIAL VÁLIDO]"
        detalles = [
            "Código QR oficial con marco verde menta verificado.",
            "Estructura y colores del comprobante válidos.",
            f"Distribución de compresión uniforme (Ratio ELA: {ratio_disc:.2f})."
        ]
        
    return prob_fraude, tipo_dictamen, detalles, img_ela
