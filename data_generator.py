"""
Generador Sintético de Comprobantes Modernos de Nequi (Versión Actualizada con Código QR)
Replica con exactitud milimétrica el diseño actual de Nequi (Fondo claro, QR de verificación, tipografía y comprobante tipo ticket).
"""

import os
import random
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# Paleta de colores oficial del comprobante actual de Nequi
COLOR_BG_TICKET = (252, 252, 253)       # Blanco tiquete suave (#FCFCFD)
COLOR_MINT_QR = (132, 228, 189)          # Verde menta/cian del marco QR (#84E4BD)
COLOR_PURPLE_NEQUI = (32, 4, 34)         # Morado oscuro característico Nequi (#200422)
COLOR_TEXT_BLACK = (20, 20, 25)          # Texto principal casi negro (#141419)
COLOR_TEXT_GRAY = (110, 110, 120)        # Texto secundario/etiquetas (#6E6E78)
COLOR_DOODLE_LINE = (235, 235, 240)      # Líneas sutiles de la ilustración de fondo

NOMBRES = ["Erick Guardo", "Carlos Rodríguez", "María Camila Gómez", "Andrés Martínez", 
           "Valentina López", "Juan David García", "Laura Sofía Pérez", "Daniel Felipe Hernández"]

MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def get_default_font(size):
    """Carga fuente estándar del sistema."""
    font_names = ["arial.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf", "Roboto-Regular.ttf"]
    for f in font_names:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def get_bold_font(size):
    """Carga fuente en negrita para montos y títulos."""
    font_names = ["arialbd.ttf", "LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf", "Roboto-Bold.ttf"]
    for f in font_names:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def dibujar_qr_simulado(draw, x, y, size=180):
    """Dibuja un código QR estilizado con el marco verde menta y la 'N' central de Nequi."""
    # 1. Marco verde menta con bordes redondeados
    pad = 12
    draw.rounded_rectangle([(x - pad, y - pad), (x + size + pad, y + size + pad)], radius=8, fill=COLOR_MINT_QR)
    
    # 2. Fondo blanco del QR
    draw.rounded_rectangle([(x, y), (x + size, y + size)], radius=4, fill=(255, 255, 255))
    
    # 3. Cuadrícula de módulos QR simulados
    grid_n = 21
    cell_size = size / grid_n
    
    # Patrón estocástico pseudo-QR con esquinas fijas (Position Detection Patterns)
    np.random.seed(x + y)
    for row in range(grid_n):
        for col in range(grid_n):
            # Esquinas de posicionamiento QR
            es_esquina = (row < 7 and col < 7) or (row < 7 and col >= grid_n - 7) or (row >= grid_n - 7 and col < 7)
            # Centro del logo 'N'
            es_centro = (7 <= row <= 13 and 7 <= col <= 13)
            
            if es_esquina:
                # Dibujar patrón de cuadro exterior e interior
                if (row in [0, 6] and 0 <= col <= 6) or (col in [0, 6] and 0 <= row <= 6) or (2 <= row <= 4 and 2 <= col <= 4):
                    draw.rectangle([(x + col * cell_size, y + row * cell_size), 
                                    (x + (col + 1) * cell_size, y + (row + 1) * cell_size)], fill=COLOR_PURPLE_NEQUI)
                elif (row in [0, 6] and grid_n - 7 <= col < grid_n) or (col in [grid_n - 7, grid_n - 1] and 0 <= row <= 6) or (2 <= row <= 4 and grid_n - 5 <= col <= grid_n - 3):
                    draw.rectangle([(x + col * cell_size, y + row * cell_size), 
                                    (x + (col + 1) * cell_size, y + (row + 1) * cell_size)], fill=COLOR_PURPLE_NEQUI)
                elif (row in [grid_n - 7, grid_n - 1] and 0 <= col <= 6) or (col in [0, 6] and grid_n - 7 <= row < grid_n) or (grid_n - 5 <= row <= grid_n - 3 and 2 <= col <= 4):
                    draw.rectangle([(x + col * cell_size, y + row * cell_size), 
                                    (x + (col + 1) * cell_size, y + (row + 1) * cell_size)], fill=COLOR_PURPLE_NEQUI)
            elif not es_centro:
                if np.random.rand() > 0.45:
                    draw.rectangle([(x + col * cell_size, y + row * cell_size), 
                                    (x + (col + 1) * cell_size, y + (row + 1) * cell_size)], fill=COLOR_PURPLE_NEQUI)
    
    # 4. Logo 'N' en el centro del QR
    c_x, c_y = x + size / 2, y + size / 2
    r_n = 22
    draw.rounded_rectangle([(c_x - r_n, c_y - r_n), (c_x + r_n, c_y + r_n)], radius=6, fill=(255, 255, 255))
    font_n = get_bold_font(26)
    draw.text((c_x - 10, c_y - 17), "·N", fill=COLOR_PURPLE_NEQUI, font=font_n)

def dibujar_fondo_ilustrado(draw, ancho, alto):
    """Dibuja sutiles trazos de ilustración de fondo típicos del comprobante Nequi."""
    for i in range(150, alto - 50, 45):
        draw.line([(30, i), (ancho - 30, i)], fill=COLOR_DOODLE_LINE, width=1)
    # Círculos y monumentos de fondo simulados
    draw.arc([(ancho - 160, 200), (ancho - 40, 320)], start=0, end=360, fill=COLOR_DOODLE_LINE, width=1)
    draw.arc([(40, 350), (140, 450)], start=0, end=360, fill=COLOR_DOODLE_LINE, width=1)

def simular_datos_transaccion():
    """Genera datos verosímiles con el formato exacto del nuevo comprobante."""
    nombre = random.choice(NOMBRES)
    telefono = f"300 {random.randint(100, 999)} {random.randint(1000, 9999)}"
    
    montos = [20000, 50000, 100000, 150000, 200000, 350000, 500000, 1000000]
    monto_val = random.choice(montos)
    monto_str = f"$ {monto_val:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    
    fecha_base = datetime.now() - timedelta(days=random.randint(0, 40), minutes=random.randint(1, 1440))
    dia_str = f"{fecha_base.day:02d}"
    mes_str = MESES_ES[fecha_base.month - 1]
    hora_12 = fecha_base.strftime("%I:%M")
    ampm = "a. m." if fecha_base.hour < 12 else "p. m."
    fecha_str = f"{dia_str} de {mes_str} de {fecha_base.year} a las {hora_12} {ampm}"
    
    # Referencia oficial: 'M' + 8 dígitos
    referencia = f"M{random.randint(10000000, 99999999)}"
    
    return {
        "nombre": nombre,
        "telefono": telefono,
        "monto": monto_str,
        "monto_num": monto_val,
        "fecha": fecha_str,
        "referencia": referencia
    }

def crear_comprobante_nequi_moderno(datos, ancho=480, alto=880):
    """Renderiza el comprobante de Nequi con el nuevo diseño oficial blanco/QR."""
    img = Image.new("RGB", (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Línea perforada superior de tiquete
    for x_p in range(15, ancho - 15, 8):
        draw.rectangle([(x_p, 25), (x_p + 4, 27)], fill=(200, 200, 210))
        
    # Ilustración sutil de fondo
    dibujar_fondo_ilustrado(draw, ancho, alto)
    
    # 1. Código QR central
    qr_size = 190
    qr_x = (ancho - qr_size) // 2
    qr_y = 65
    dibujar_qr_simulado(draw, qr_x, qr_y, size=qr_size)
    
    # 2. Mensaje de verificación bajo el QR
    font_info = get_default_font(15)
    font_bold_info = get_bold_font(15)
    info_y = 310
    
    # Icono info (i)
    draw.ellipse([(qr_x - 15, info_y - 2), (qr_x + 10, info_y + 23)], outline=COLOR_TEXT_BLACK, width=2)
    draw.text((qr_x - 6, info_y + 2), "i", fill=COLOR_TEXT_BLACK, font=font_bold_info)
    
    # Texto de aviso
    draw.text((qr_x + 20, info_y - 4), "¡Escanea este QR con Nequi para", fill=COLOR_TEXT_BLACK, font=font_info)
    draw.text((qr_x + 20, info_y + 14), "verificar tu envío al instante!", fill=COLOR_TEXT_BLACK, font=font_info)
    
    # Fuentes para los campos
    font_label = get_default_font(18)
    font_value = get_bold_font(23)
    font_amount = get_bold_font(27)
    
    left_margin = 55
    y_cursor = 390
    
    # Campo: Para
    draw.text((left_margin, y_cursor), "Para", fill=COLOR_TEXT_GRAY, font=font_label)
    draw.text((left_margin, y_cursor + 24), datos["nombre"], fill=COLOR_TEXT_BLACK, font=font_value)
    
    # Campo: ¿Cuánto?
    y_cursor += 70
    draw.text((left_margin, y_cursor), "¿Cuánto?", fill=COLOR_TEXT_GRAY, font=font_label)
    draw.text((left_margin, y_cursor + 24), datos["monto"], fill=COLOR_TEXT_BLACK, font=font_amount)
    
    # Campo: Número Nequi
    y_cursor += 75
    draw.text((left_margin, y_cursor), "Número Nequi", fill=COLOR_TEXT_GRAY, font=font_label)
    draw.text((left_margin, y_cursor + 24), datos["telefono"], fill=COLOR_TEXT_BLACK, font=font_value)
    
    # Campo: Fecha
    y_cursor += 70
    draw.text((left_margin, y_cursor), "Fecha", fill=COLOR_TEXT_GRAY, font=font_label)
    draw.text((left_margin, y_cursor + 24), datos["fecha"], fill=COLOR_TEXT_BLACK, font=get_bold_font(18))
    
    # Campo: Referencia
    y_cursor += 70
    draw.text((left_margin, y_cursor), "Referencia", fill=COLOR_TEXT_GRAY, font=font_label)
    draw.text((left_margin, y_cursor + 24), datos["referencia"], fill=COLOR_TEXT_BLACK, font=font_value)
    
    # Texto vertical 'VIGILADO Superintendencia Financiera de Colombia' en el borde izquierdo
    vig_img = Image.new("RGBA", (300, 30), (255, 255, 255, 0))
    vig_draw = ImageDraw.Draw(vig_img)
    vig_draw.rectangle([(2, 4), (65, 24)], outline=COLOR_TEXT_GRAY, width=1)
    vig_draw.text((8, 6), "VIGILADO", fill=COLOR_TEXT_GRAY, font=get_default_font(11))
    vig_draw.text((75, 4), "Superintendencia Financiera\nde Colombia", fill=COLOR_TEXT_GRAY, font=get_default_font(9))
    vig_rotada = vig_img.rotate(90, expand=True)
    img.paste(vig_rotada, (10, alto - 320), mask=vig_rotada)
    
    # Línea perforada inferior
    for x_p in range(15, ancho - 15, 8):
        draw.rectangle([(x_p, alto - 25), (x_p + 4, alto - 23)], fill=(200, 200, 210))
        
    return img

def generar_comprobante_moderno_legitimo(datos, calidad_jpeg=92):
    """Genera comprobante original con compresión homogénea."""
    img = crear_comprobante_nequi_moderno(datos)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=calidad_jpeg)
    buf.seek(0)
    return Image.open(buf)

def generar_comprobante_moderno_fraudulento(datos, tipo_fraude=None):
    """
    Genera comprobante falsificado en el nuevo diseño:
    1. 'edicion_monto': Parche de color y sobreescritura de monto en Photoshop/Canva.
    2. 'app_falsa': QR desalineado sin logo, colores menta alterados, fuentes erróneas.
    3. 'edicion_fecha_ref': Modificación de fecha y referencia para reutilizar comprobante.
    """
    if tipo_fraude is None:
        tipo_fraude = random.choice(["edicion_monto", "app_falsa", "edicion_fecha_ref"])
        
    img_base = crear_comprobante_nequi_moderno(datos)
    
    if tipo_fraude == "edicion_monto":
        # Simula compresión previa
        buf = BytesIO()
        img_base.save(buf, format="JPEG", quality=90)
        buf.seek(0)
        img_edit = Image.open(buf).convert("RGB")
        draw = ImageDraw.Draw(img_edit)
        
        # Parche sobre el monto (con leve diferencia de tono de blanco y ruido)
        draw.rectangle([(50, 480), (380, 525)], fill=(247, 248, 250))
        
        monto_adulterado = f"$ {datos['monto_num'] * random.choice([5, 10]):,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
        font_edit = get_default_font(26) # Fuente desalineada
        draw.text((54, 484), monto_adulterado, fill=(10, 10, 15), font=font_edit)
        
        # Doble compresión localizada JPEG
        buf2 = BytesIO()
        img_edit.save(buf2, format="JPEG", quality=75)
        buf2.seek(0)
        return Image.open(buf2)
        
    elif tipo_fraude == "app_falsa":
        # Simula clon con marco de color incorrecto (verde oscuro o azulado) y fuentes del sistema
        ancho, alto = 480, 880
        img_falsa = Image.new("RGB", (ancho, alto), color=(255, 255, 255))
        draw = ImageDraw.Draw(img_falsa)
        
        # QR sin marco de calidad
        draw.rectangle([(130, 60), (350, 270)], fill=(0, 180, 120)) # Verde descalibrado
        draw.text((150, 140), "QR FAKE CLONE", fill=(255, 255, 255), font=get_bold_font(20))
        
        draw.text((50, 380), f"Para: {datos['nombre']}", fill=(0, 0, 0), font=get_default_font(20))
        draw.text((50, 460), f"Total: {datos['monto']}", fill=(200, 0, 50), font=get_bold_font(26)) # Color rojo anómalo
        draw.text((50, 540), f"Tel: {datos['telefono']}", fill=(0, 0, 0), font=get_default_font(20))
        draw.text((50, 620), f"Fecha: {datos['fecha']}", fill=(0, 0, 0), font=get_default_font(18))
        draw.text((50, 700), f"Ref: {datos['referencia']}", fill=(0, 0, 0), font=get_default_font(18))
        return img_falsa
        
    else: # edicion_fecha_ref
        draw = ImageDraw.Draw(img_base)
        draw.rectangle([(50, 630), (450, 665)], fill=(255, 255, 255))
        draw.rectangle([(50, 700), (350, 735)], fill=(255, 255, 255))
        
        draw.text((55, 634), "02 de agosto de 2026 a las 18:00 p. m. (Falsa)", fill=(10, 10, 10), font=get_default_font(16))
        draw.text((55, 704), "M_ALTERADA_001", fill=(10, 10, 10), font=get_default_font(20))
        return img_base

def construir_dataset(directorio_raiz="dataset", n_entrenamiento=400, n_validacion=80, n_prueba=80):
    """Genera el dataset balanceado con el diseño actual de Nequi."""
    splits = {"train": n_entrenamiento, "val": n_validacion, "test": n_prueba}
    clases = ["legitimo", "fraude"]
    
    print(f"🚀 Generando dataset con la NUEVA imagen de Nequi (QR/Ticket) en: {directorio_raiz}")
    
    for split_name, total_samples in splits.items():
        n_por_clase = total_samples // 2
        for clase in clases:
            ruta_carpeta = os.path.join(directorio_raiz, split_name, clase)
            os.makedirs(ruta_carpeta, exist_ok=True)
            
            for i in range(n_por_clase):
                datos = simular_datos_transaccion()
                if clase == "legitimo":
                    img = generar_comprobante_moderno_legitimo(datos)
                else:
                    img = generar_comprobante_moderno_fraudulento(datos)
                
                nombre_archivo = f"{clase}_{split_name}_{i+1:04d}.jpg"
                img.save(os.path.join(ruta_carpeta, nombre_archivo), format="JPEG", quality=90)
                
        print(f"  ✓ Split '{split_name}': {n_por_clase} legítimos y {n_por_clase} fraudulentos generados.")
        
    print("✨ ¡Dataset del nuevo formato Nequi generado con éxito!")

if __name__ == "__main__":
    construir_dataset()
