"""
Generador Sintético de Comprobantes de Nequi (Legítimos y Fraudulentos)
Permite construir un dataset balanceado sin vulnerar la privacidad de datos reales.
"""

import os
import random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# Paleta de colores oficial aproximada de Nequi
COLOR_BG_DARK = (28, 4, 34)         # Morado oscuro de fondo (#1C0422)
COLOR_CARD = (40, 10, 50)           # Fondo de tarjeta (#280A32)
COLOR_MAGENTA = (218, 0, 129)       # Magenta corporativo (#DA0081)
COLOR_TEXT_WHITE = (255, 255, 255)  # Blanco puro
COLOR_TEXT_GRAY = (180, 170, 190)   # Gris claro para subtítulos
COLOR_GREEN_CHECK = (0, 200, 115)   # Verde de confirmación

# Lista de nombres y apellidos comunes para simulación realista
NOMBRES = ["Carlos", "María", "Andrés", "Valentina", "Juan", "Camila", "Daniel", "Laura", "Sebastián", "Sofía", "Erick", "Diana"]
APELLIDOS = ["Rodríguez", "Gómez", "Martínez", "López", "García", "Pérez", "Hernández", "Torres", "Morales", "Ramírez"]

def get_default_font(size):
    """Carga una fuente disponible en el sistema o la fuente por defecto de PIL."""
    try:
        # Intenta cargar fuentes estándar comunes (Windows/Linux/Colab)
        font_names = ["arial.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf", "Roboto-Regular.ttf"]
        for f in font_names:
            try:
                return ImageFont.truetype(f, size)
            except Exception:
                continue
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()

def get_bold_font(size):
    """Carga fuente en negrita para montos y títulos."""
    try:
        font_names = ["arialbd.ttf", "LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf", "Roboto-Bold.ttf"]
        for f in font_names:
            try:
                return ImageFont.truetype(f, size)
            except Exception:
                continue
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()

def generar_datos_transaccion():
    """Genera metadatos aleatorios coherentes de una transacción Nequi."""
    nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
    telefono = f"3{random.randint(0, 5)}{random.randint(0, 9)} {random.randint(100, 999)} {random.randint(1000, 9999)}"
    
    # Montos realistas en pesos colombianos (COP)
    montos = [10000, 20000, 35000, 50000, 75000, 100000, 150000, 200000, 350000, 500000, 1200000]
    monto_val = random.choice(montos)
    monto_str = f"$ {monto_val:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    
    # Fecha y hora reciente
    fecha_base = datetime.now() - timedelta(days=random.randint(0, 30), minutes=random.randint(1, 1440))
    meses_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    fecha_str = f"{fecha_base.day:02d} {meses_es[fecha_base.month - 1]} {fecha_base.year} - {fecha_base.strftime('%H:%M')}"
    
    # Referencia oficial típica de Nequi: Empieza con M y 7-8 dígitos
    referencia = f"M{random.randint(1000000, 9999999)}"
    
    return {
        "nombre": nombre,
        "telefono": telefono,
        "monto": monto_str,
        "monto_num": monto_val,
        "fecha": fecha_str,
        "referencia": referencia
    }

def crear_comprobante_base(datos, ancho=400, alto=700):
    """Dibuja la plantilla base limpia de un comprobante de Nequi."""
    img = Image.new("RGB", (ancho, alto), color=COLOR_BG_DARK)
    draw = ImageDraw.Draw(img)
    
    font_title = get_bold_font(20)
    font_large = get_bold_font(32)
    font_medium = get_default_font(18)
    font_small = get_default_font(14)
    
    # Barra superior con logo Nequi simulado y título
    draw.rectangle([(20, 25), (70, 50)], fill=COLOR_MAGENTA)
    draw.text((25, 27), "N", fill=COLOR_TEXT_WHITE, font=get_bold_font(20))
    draw.text((80, 28), "¡Enviaste plata!", fill=COLOR_TEXT_WHITE, font=font_title)
    
    # Círculo verde con check de confirmación exitosa
    centro_circulo = (ancho // 2, 120)
    radio = 30
    draw.ellipse([
        (centro_circulo[0] - radio, centro_circulo[1] - radio),
        (centro_circulo[0] + radio, centro_circulo[1] + radio)
    ], fill=COLOR_GREEN_CHECK)
    draw.text((centro_circulo[0] - 10, centro_circulo[1] - 15), "✓", fill=COLOR_TEXT_WHITE, font=get_bold_font(28))
    
    # Tarjeta central con la información del envío
    card_box = [(25, 175), (ancho - 25, 590)]
    draw.rectangle(card_box, fill=COLOR_CARD, outline=COLOR_MAGENTA, width=2)
    
    # Datos del destinatario
    draw.text((45, 200), "Para:", fill=COLOR_TEXT_GRAY, font=font_small)
    draw.text((45, 220), datos["nombre"], fill=COLOR_TEXT_WHITE, font=font_medium)
    draw.text((45, 245), datos["telefono"], fill=COLOR_TEXT_GRAY, font=font_small)
    
    # Línea divisoria sutil
    draw.line([(45, 280), (ancho - 45, 280)], fill=(70, 30, 80), width=1)
    
    # Monto de la transacción (Elemento crítico)
    draw.text((45, 300), "¿Cuánto?", fill=COLOR_TEXT_GRAY, font=font_small)
    draw.text((45, 325), datos["monto"], fill=COLOR_TEXT_WHITE, font=font_large)
    
    # Línea divisoria
    draw.line([(45, 385), (ancho - 45, 385)], fill=(70, 30, 80), width=1)
    
    # Fecha y Referencia
    draw.text((45, 410), "Fecha y hora", fill=COLOR_TEXT_GRAY, font=font_small)
    draw.text((45, 430), datos["fecha"], fill=COLOR_TEXT_WHITE, font=font_medium)
    
    draw.text((45, 480), "Referencia", fill=COLOR_TEXT_GRAY, font=font_small)
    draw.text((45, 500), datos["referencia"], fill=COLOR_TEXT_WHITE, font=font_medium)
    
    draw.text((45, 545), "Disponible en tu cuenta", fill=COLOR_MAGENTA, font=font_small)
    
    # Pie de página
    draw.text((ancho // 2 - 60, alto - 50), "Listo", fill=COLOR_TEXT_WHITE, font=font_medium)
    
    return img

def generar_comprobante_legitimo(datos, calidad_jpeg=92):
    """Genera un comprobante auténtico con compresión realista estándar."""
    img = crear_comprobante_base(datos)
    
    # Simula compresión homogénea de un screenshot original
    from io import BytesIO
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=calidad_jpeg)
    buffer.seek(0)
    return Image.open(buffer)

def generar_comprobante_fraudulento(datos, tipo_fraude=None):
    """
    Genera un comprobante falsificado simulando los 3 métodos más comunes:
    1. 'edicion_monto': Parche y sobreescritura del monto con editor (Photoshop/Canva).
    2. 'app_falsa': Inconsistencia en tipografías, colores desalineados y márgenes defectuosos.
    3. 'edicion_referencia_fecha': Modificación de la fecha o código para reutilizar el comprobante.
    """
    if tipo_fraude is None:
        tipo_fraude = random.choice(["edicion_monto", "app_falsa", "edicion_referencia_fecha"])
    
    img = crear_comprobante_base(datos)
    
    if tipo_fraude == "edicion_monto":
        # Primero se guarda como JPEG original
        from io import BytesIO
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=90)
        buf.seek(0)
        img_editada = Image.open(buf).convert("RGB")
        draw = ImageDraw.Draw(img_editada)
        
        # Simula tapar el monto original con un parche de color aproximado
        draw.rectangle([(40, 320), (350, 375)], fill=(45, 12, 55)) # Parche con tono ligeramente disparejo
        
        # Escribe un monto falso mucho mayor con fuente y alineación desfasada
        monto_falso_val = datos["monto_num"] * random.choice([5, 10, 20])
        monto_falso_str = f"$ {monto_falso_val:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
        
        font_editada = get_default_font(28) # Fuente diferente a la oficial
        draw.text((48, 328), monto_falso_str, fill=(245, 245, 255), font=font_editada)
        
        # Se vuelve a guardar (doble compresión localizada - clave para detección ELA)
        buf2 = BytesIO()
        img_editada.save(buf2, format="JPEG", quality=75)
        buf2.seek(0)
        return Image.open(buf2)
        
    elif tipo_fraude == "app_falsa":
        # Simula una app pirata con paleta de colores descalibrada y fuentes incorrectas
        ancho, alto = 400, 700
        color_bg_falso = (random.randint(40, 60), 0, random.randint(50, 70))
        img_falsa = Image.new("RGB", (ancho, alto), color=color_bg_falso)
        draw = ImageDraw.Draw(img_falsa)
        
        font_falsa = get_default_font(16)
        font_monto_falso = get_default_font(30)
        
        # Tarjeta con márgenes asimétricos
        draw.rectangle([(15, 160), (ancho - 35, 600)], fill=(50, 15, 60), outline=(255, 0, 100), width=1)
        draw.text((30, 210), f"Para: {datos['nombre']}", fill=COLOR_TEXT_WHITE, font=font_falsa)
        draw.text((30, 250), datos["telefono"], fill=COLOR_TEXT_GRAY, font=font_falsa)
        draw.text((30, 330), datos["monto"], fill=(255, 255, 200), font=font_monto_falso) # Color amarillento anómalo
        draw.text((30, 430), f"Fecha: {datos['fecha']}", fill=COLOR_TEXT_WHITE, font=font_falsa)
        draw.text((30, 500), f"Ref: {datos['referencia']}", fill=COLOR_TEXT_WHITE, font=font_falsa)
        
        return img_falsa

    else: # edicion_referencia_fecha
        draw = ImageDraw.Draw(img)
        # Tapa fecha y referencia
        draw.rectangle([(40, 425), (350, 460)], fill=COLOR_CARD)
        draw.rectangle([(40, 495), (350, 530)], fill=COLOR_CARD)
        
        # Escribe fecha adulterada
        draw.text((45, 428), "02 Ago 2026 - 17:15 (Adulterada)", fill=(230, 230, 255), font=get_default_font(15))
        draw.text((45, 498), "REF_INVALIDA_999", fill=(230, 230, 255), font=get_default_font(15))
        return img

def construir_dataset(directorio_raiz="dataset", n_entrenamiento=400, n_validacion=80, n_prueba=80):
    """Crea la estructura de carpetas y genera el dataset completo etiquetado."""
    splits = {
        "train": n_entrenamiento,
        "val": n_validacion,
        "test": n_prueba
    }
    
    clases = ["legitimo", "fraude"]
    
    print(f"🚀 Generando dataset sintético de comprobantes Nequi en: {directorio_raiz}")
    
    for split_name, total_samples in splits.items():
        n_por_clase = total_samples // 2
        for clase in clases:
            ruta_carpeta = os.path.join(directorio_raiz, split_name, clase)
            os.makedirs(ruta_carpeta, exist_ok=True)
            
            for i in range(n_por_clase):
                datos = generar_datos_transaccion()
                if clase == "legitimo":
                    img = generar_comprobante_legitimo(datos)
                else:
                    img = generar_comprobante_fraudulento(datos)
                
                nombre_archivo = f"{clase}_{split_name}_{i+1:04d}.jpg"
                img.save(os.path.join(ruta_carpeta, nombre_archivo), format="JPEG", quality=90)
                
        print(f"  ✓ Split '{split_name}': {n_por_clase} legítimos y {n_por_clase} fraudulentos generados.")
    
    print("✨ ¡Dataset generado exitosamente!")

if __name__ == "__main__":
    construir_dataset()
