"""
Módulo Forense Digital: Error Level Analysis (ELA)
Calcula las discrepancias en los niveles de compresión JPEG para exponer zonas modificadas digitalmente.
"""

from io import BytesIO
from PIL import Image, ImageChops, ImageEnhance
import numpy as np

def calcular_ela(imagen_o_ruta, calidad=90, factor_escala=15):
    """
    Aplica el algoritmo de Error Level Analysis (ELA) a una imagen.
    
    Parámetros:
        imagen_o_ruta: Objeto PIL.Image o string con la ruta del archivo.
        calidad (int): Calidad de compresión JPEG de referencia (típicamente 90-92).
        factor_escala (int): Multiplicador para amplificar las diferencias sutiles de error.
        
    Retorna:
        PIL.Image: Imagen con el mapa ELA procesado.
    """
    if isinstance(imagen_o_ruta, str):
        img_original = Image.open(imagen_o_ruta).convert("RGB")
    else:
        img_original = imagen_o_ruta.convert("RGB")
        
    # Paso 1: Re-comprimir la imagen temporalmente en memoria a una tasa conocida
    buffer = BytesIO()
    img_original.save(buffer, format="JPEG", quality=calidad)
    buffer.seek(0)
    img_recomprimida = Image.open(buffer)
    
    # Paso 2: Calcular la diferencia absoluta de píxeles entre la original y la re-comprimida
    diferencia = ImageChops.difference(img_original, img_recomprimida)
    
    # Paso 3: Amplificar las diferencias para hacerlas visibles al ojo y al modelo
    extremos = diferencia.getextrema()
    max_dif = max([ex[1] for ex in extremos])
    if max_dif == 0:
        max_dif = 1 # Evitar división por cero
        
    escala = factor_escala * (255.0 / max_dif)
    potenciador = ImageEnhance.Brightness(diferencia)
    ela_resultado = potenciador.enhance(escala)
    
    return ela_resultado

def obtener_tensor_fusionado(img_original, factor_escala=15):
    """
    Genera una representación combinada (Original + ELA) como matriz NumPy
    para alimentar la red neuronal convolucional (CNN).
    """
    ela_img = calcular_ela(img_original, factor_escala=factor_escala)
    
    arr_orig = np.array(img_original.convert("RGB"), dtype=np.float32) / 255.0
    arr_ela = np.array(ela_img.convert("RGB"), dtype=np.float32) / 255.0
    
    # Retorna un tensor de 6 canales (R, G, B original + R, G, B ELA) o el mapa ELA directamente
    return arr_orig, arr_ela
