"""
Descargador y verificador robusto de plantillas oficiales
"""
import urllib.request
import os
from PIL import Image

URL_AUTENTICO = "https://raw.githubusercontent.com/efelipe0526/deteccion-de-fraude-nequi/main/templates/comprobante_autentico.jpg"
URL_FALSO = "https://raw.githubusercontent.com/efelipe0526/deteccion-de-fraude-nequi/main/templates/comprobante_falso_app.png"

os.makedirs("templates", exist_ok=True)

def asegurar_plantillas():
    ruta_aut = "templates/comprobante_autentico.jpg"
    ruta_fal = "templates/comprobante_falso_app.png"
    
    if not os.path.exists(ruta_aut) or os.path.getsize(ruta_aut) < 1000:
        print("Descargando plantilla auténtica oficial desde GitHub...")
        urllib.request.urlretrieve(URL_AUTENTICO, ruta_aut)
        
    if not os.path.exists(ruta_fal) or os.path.getsize(ruta_fal) < 1000:
        print("Descargando plantilla de app falsa desde GitHub...")
        urllib.request.urlretrieve(URL_FALSO, ruta_fal)
        
    print(f"✓ Plantilla auténtica cargada: {ruta_aut} ({os.path.getsize(ruta_aut)} bytes)")
    print(f"✓ Plantilla falsa cargada: {ruta_fal} ({os.path.getsize(ruta_fal)} bytes)")
    
if __name__ == "__main__":
    asegurar_plantillas()
