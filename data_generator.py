"""
Generador Aumentado con Plantillas Reales Oficiales de Nequi
Crea un dataset realista de alta fidelidad para entrenamiento de redes neuronales profundas.
"""

import os
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageEnhance, ImageFilter
import numpy as np

def aplicar_aumentacion_realista(img_pil, es_autentico=True):
    """Aplica variaciones realistas de captura de pantalla, WhatsApp y compresión."""
    img = img_pil.copy()
    
    # 1. Jitter sutil de brillo y contraste (simula pantallas de diferentes marcas)
    b_factor = random.uniform(0.92, 1.08)
    c_factor = random.uniform(0.92, 1.08)
    img = ImageEnhance.Brightness(img).enhance(b_factor)
    img = ImageEnhance.Contrast(img).enhance(c_factor)
    
    # 2. Rotación leve (-1.5 a +1.5 grados) o recorte mínimo
    if random.random() > 0.5:
        angulo = random.uniform(-1.2, 1.2)
        img = img.rotate(angulo, resample=Image.BILINEAR, expand=False, fillcolor=(255, 255, 255))
        
    # 3. Compresión multicalidad (simula envíos por WhatsApp, Telegram o descarga web)
    calidad = random.choice([55, 68, 78, 85, 92, 98])
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=calidad)
    buf.seek(0)
    return Image.open(buf)

def generar_edicion_monto(img_autentica_pil):
    """Simula una falsificación por edición en Photoshop/editor sobre el comprobante real."""
    img = img_autentica_pil.copy().convert("RGB")
    draw = ImageDraw.Draw(img)
    ancho, alto = img.size
    
    # Ubicación proporcional del campo "¿Cuánto?"
    y_ini = int(alto * 0.57)
    y_fin = int(alto * 0.63)
    x_ini = int(ancho * 0.10)
    x_fin = int(ancho * 0.85)
    
    # Parche de color que no coincide exactamente con la textura del fondo
    color_parche = random.choice([(255, 255, 255), (245, 248, 250), (240, 242, 245)])
    draw.rectangle([(x_ini, y_ini), (x_fin, y_fin)], fill=color_parche)
    
    # Escribir monto falso
    monto_falso = f"$ {random.randint(5, 50) * 50000:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    draw.text((x_ini + 10, y_ini + 5), monto_falso, fill=(15, 15, 20))
    
    # Guardar con compresión secundaria que deja huella ELA
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=60)
    buf.seek(0)
    return Image.open(buf)
