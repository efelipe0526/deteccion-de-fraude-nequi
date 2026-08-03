"""
Generador Sintético Robusto de Comprobantes Nequi con Simulación Multicalidad
Enseña a la IA a distinguir entre compresión normal de WhatsApp/redes y falsificación real.
"""

import os
import random
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

COLOR_MINT_QR = (132, 228, 189)     # Verde menta/cian (#84E4BD)
COLOR_PURPLE = (32, 4, 34)          # Morado Nequi (#200422)
COLOR_TEXT_DARK = (20, 20, 25)      # Texto principal
COLOR_LABEL_GRAY = (110, 110, 120)  # Etiquetas
COLOR_DOODLE = (235, 235, 240)      # Ilustración de fondo

NOMBRES_EJEMPLO = ["Erick Guardo", "Carlos Rodríguez", "María Gómez", "Andrés Martínez", "Valentina López", "Juan David García", "Laura Pérez", "Daniel Morales"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def get_default_font(size):
    font_names = ["arial.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf", "Roboto-Regular.ttf"]
    for f in font_names:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def get_bold_font(size):
    font_names = ["arialbd.ttf", "LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf", "Roboto-Bold.ttf"]
    for f in font_names:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def dibujar_qr_nequi(draw, x, y, size=180):
    pad = 12
    draw.rounded_rectangle([(x - pad, y - pad), (x + size + pad, y + size + pad)], radius=8, fill=COLOR_MINT_QR)
    draw.rounded_rectangle([(x, y), (x + size, y + size)], radius=4, fill=(255, 255, 255))
    
    grid_n = 21
    cell_size = size / grid_n
    np.random.seed(x + y)
    for r in range(grid_n):
        for c in range(grid_n):
            es_esq = (r < 7 and c < 7) or (r < 7 and c >= grid_n - 7) or (r >= grid_n - 7 and c < 7)
            es_cntr = (7 <= r <= 13 and 7 <= c <= 13)
            if es_esq:
                if (r in [0, 6] and 0 <= c <= 6) or (c in [0, 6] and 0 <= r <= 6) or (2 <= r <= 4 and 2 <= c <= 4):
                    draw.rectangle([(x + c*cell_size, y + r*cell_size), (x + (c+1)*cell_size, y + (r+1)*cell_size)], fill=COLOR_PURPLE)
                elif (r in [0, 6] and grid_n - 7 <= c < grid_n) or (c in [grid_n - 7, grid_n - 1] and 0 <= r <= 6) or (2 <= r <= 4 and grid_n - 5 <= c <= grid_n - 3):
                    draw.rectangle([(x + c*cell_size, y + r*cell_size), (x + (c+1)*cell_size, y + (r+1)*cell_size)], fill=COLOR_PURPLE)
                elif (r in [grid_n - 7, grid_n - 1] and 0 <= c <= 6) or (c in [0, 6] and grid_n - 7 <= r < grid_n) or (grid_n - 5 <= r <= grid_n - 3 and 2 <= c <= 4):
                    draw.rectangle([(x + c*cell_size, y + r*cell_size), (x + (c+1)*cell_size, y + (r+1)*cell_size)], fill=COLOR_PURPLE)
            elif not es_cntr and np.random.rand() > 0.45:
                draw.rectangle([(x + c*cell_size, y + r*cell_size), (x + (c+1)*cell_size, y + (r+1)*cell_size)], fill=COLOR_PURPLE)
                
    c_x, c_y = x + size/2, y + size/2
    draw.rounded_rectangle([(c_x - 22, c_y - 22), (c_x + 22, c_y + 22)], radius=6, fill=(255, 255, 255))
    draw.text((c_x - 10, c_y - 12), "·N", fill=COLOR_PURPLE, font=get_bold_font(24))

def crear_comprobante_nequi_actual(datos, ancho=480, alto=880):
    img = Image.new("RGB", (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Líneas perforadas
    for x_p in range(15, ancho - 15, 8):
        draw.rectangle([(x_p, 25), (x_p + 4, 27)], fill=(200, 200, 210))
        draw.rectangle([(x_p, alto - 25), (x_p + 4, alto - 23)], fill=(200, 200, 210))
        
    # Fondo ilustrado
    for i in range(150, alto - 50, 45):
        draw.line([(30, i), (ancho - 30, i)], fill=COLOR_DOODLE, width=1)
        
    qr_x = (ancho - 190) // 2
    dibujar_qr_nequi(draw, qr_x, 65, size=190)
    
    # Aviso
    info_y = 310
    draw.ellipse([(qr_x - 15, info_y - 2), (qr_x + 10, info_y + 23)], outline=COLOR_TEXT_DARK, width=2)
    draw.text((qr_x - 4, info_y + 2), "i", fill=COLOR_TEXT_DARK, font=get_bold_font(15))
    draw.text((qr_x + 18, info_y - 4), "¡Escanea este QR con Nequi para", fill=COLOR_TEXT_DARK, font=get_default_font(15))
    draw.text((qr_x + 18, info_y + 14), "verificar tu envío al instante!", fill=COLOR_TEXT_DARK, font=get_default_font(15))
    
    # Campos
    y_cur = 390
    margen = 55
    
    draw.text((margen, y_cur), "Para", fill=COLOR_LABEL_GRAY, font=get_default_font(18))
    draw.text((margen, y_cur + 24), datos["nombre"], fill=COLOR_TEXT_DARK, font=get_bold_font(23))
    
    y_cur += 70
    draw.text((margen, y_cur), "¿Cuánto?", fill=COLOR_LABEL_GRAY, font=get_default_font(18))
    draw.text((margen, y_cur + 24), datos["monto"], fill=COLOR_TEXT_DARK, font=get_bold_font(27))
    
    y_cur += 75
    draw.text((margen, y_cur), "Número Nequi", fill=COLOR_LABEL_GRAY, font=get_default_font(18))
    draw.text((margen, y_cur + 24), datos["telefono"], fill=COLOR_TEXT_DARK, font=get_bold_font(23))
    
    y_cur += 70
    draw.text((margen, y_cur), "Fecha", fill=COLOR_LABEL_GRAY, font=get_default_font(18))
    draw.text((margen, y_cur + 24), datos["fecha"], fill=COLOR_TEXT_DARK, font=get_bold_font(18))
    
    y_cur += 70
    draw.text((margen, y_cur), "Referencia", fill=COLOR_LABEL_GRAY, font=get_default_font(18))
    draw.text((margen, y_cur + 24), datos["referencia"], fill=COLOR_TEXT_DARK, font=get_bold_font(23))
    
    return img

def simular_datos_nequi():
    nom = random.choice(NOMBRES_EJEMPLO)
    tel = f"300 {random.randint(100, 999)} {random.randint(1000, 9999)}"
    val = random.choice([20000, 50000, 100000, 150000, 200000, 350000, 500000, 1000000])
    monto_str = f"$ {val:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    f_base = datetime.now() - timedelta(days=random.randint(0, 30), minutes=random.randint(1, 1440))
    hora_12 = f_base.strftime("%I:%M")
    ampm = "a. m." if f_base.hour < 12 else "p. m."
    fecha = f"{f_base.day:02d} de {MESES[f_base.month - 1]} de {f_base.year} a las {hora_12} {ampm}"
    ref = f"M{random.randint(10000000, 99999999)}"
    return {"nombre": nom, "telefono": tel, "monto": monto_str, "monto_num": val, "fecha": fecha, "referencia": ref}

def generar_muestra_moderna(es_fraude=False):
    d = simular_datos_nequi()
    base = crear_comprobante_nequi_actual(d)
    
    # Calidades realistas simulando capturas de distintos teléfonos y apps de mensajería (WhatsApp)
    calidad_base = random.choice([55, 65, 75, 82, 90, 95])
    
    if not es_fraude:
        buf = BytesIO()
        base.save(buf, format="JPEG", quality=calidad_base)
        buf.seek(0)
        return Image.open(buf)
    else:
        # Fraude por edición localizada (Photoshop/Canva/Pintar encima)
        buf = BytesIO()
        base.save(buf, format="JPEG", quality=85)
        buf.seek(0)
        img_edit = Image.open(buf).convert("RGB")
        draw = ImageDraw.Draw(img_edit)
        
        # Parche sobre ¿Cuánto?
        draw.rectangle([(50, 480), (380, 525)], fill=(245, 246, 248))
        monto_falso = f"$ {d['monto_num']*5:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
        draw.text((54, 484), monto_falso, fill=(10, 10, 15), font=get_default_font(26))
        
        buf2 = BytesIO()
        # Se guarda a calidad dispareja respecto al parche
        img_edit.save(buf2, format="JPEG", quality=60)
        buf2.seek(0)
        return Image.open(buf2)

def construir_dataset(directorio_raiz="dataset", n_entrenamiento=400, n_validacion=80, n_prueba=80):
    splits = {"train": n_entrenamiento, "val": n_validacion, "test": n_prueba}
    clases = ["legitimo", "fraude"]
    
    print(f"🚀 Generando dataset robusto multicalidad en: {directorio_raiz}")
    for split_name, total_samples in splits.items():
        n_por_clase = total_samples // 2
        for clase in clases:
            ruta_carpeta = os.path.join(directorio_raiz, split_name, clase)
            os.makedirs(ruta_carpeta, exist_ok=True)
            for i in range(n_por_clase):
                img = generar_muestra_moderna(es_fraude=(clase == "fraude"))
                nombre_archivo = f"{clase}_{split_name}_{i+1:04d}.jpg"
                img.save(os.path.join(ruta_carpeta, nombre_archivo), format="JPEG", quality=random.choice([70, 85, 92]))
        print(f"  ✓ Split '{split_name}': {n_por_clase} legítimos y {n_por_clase} fraudulentos generados.")
    print("✨ ¡Dataset generado!")

if __name__ == "__main__":
    construir_dataset()
