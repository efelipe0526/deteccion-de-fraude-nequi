"""
Módulo Forense Mejorado: ELA Adaptativo y Detección de Discrepancia Localizada
Distingue entre compresión global normal (WhatsApp/descarga) y manipulación localizada real.
"""

from io import BytesIO
from PIL import Image, ImageChops, ImageEnhance, ImageStat
import numpy as np

def calcular_ela_adaptativo(img_pil, calidad=92, factor_escala=12):
    """
    Calcula el mapa ELA con normalización adaptativa para evitar falsos positivos
    producidos por la compresión natural de redes sociales o capturas de pantalla.
    """
    img_rgb = img_pil.convert("RGB")
    
    # 1. Re-compresión controlada
    buf = BytesIO()
    img_rgb.save(buf, format="JPEG", quality=calidad)
    buf.seek(0)
    recomprimida = Image.open(buf)
    
    # 2. Diferencia absoluta
    diferencia = ImageChops.difference(img_rgb, recomprimida)
    
    # 3. Análisis estadístico de distribución de ruido
    stat = ImageStat.Stat(diferencia)
    std_dev_media = np.mean(stat.stddev)
    
    # Si la desviación estándar global es uniforme, normalizamos para que el ruido homogéneo no se confunda con fraude
    extremos = diferencia.getextrema()
    max_dif = max([ex[1] for ex in extremos]) or 1
    
    # Factor adaptativo basado en la uniformidad del fondo
    factor = factor_escala * (255.0 / (max_dif + std_dev_media * 2.0))
    
    potenciador = ImageEnhance.Brightness(diferencia)
    ela_normalizado = potenciador.enhance(factor)
    
    return ela_normalizado

def analizar_discrepancia_monto(img_pil):
    """
    Compara la varianza de error en la región crítica del monto ('¿Cuánto?')
    contra la varianza del resto del documento para detectar sobreescritura.
    """
    img_ela = calcular_ela_adaptativo(img_pil)
    arr = np.array(img_ela, dtype=np.float32)
    
    alto, ancho, _ = arr.shape
    
    # Coordenadas relativas de la zona del monto en el formato actual de Nequi (~45% a 60% del alto)
    y1, y2 = int(alto * 0.45), int(alto * 0.60)
    x1, x2 = int(ancho * 0.10), int(ancho * 0.90)
    
    zona_monto = arr[y1:y2, x1:x2]
    resto_doc = np.concatenate([arr[0:y1, :], arr[y2:, :]], axis=0)
    
    media_monto = np.mean(zona_monto)
    media_resto = np.mean(resto_doc)
    
    # Ratio de discrepancia localizada
    ratio_discrepancia = media_monto / (media_resto + 1e-5)
    return ratio_discrepancia, img_ela
