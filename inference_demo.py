"""
Script de Inferencia y Demostración en Tiempo Real
Permite evaluar cualquier imagen de comprobante y emitir un diagnóstico forense con visualización ELA.
"""

import os
import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt

from ela_processor import calcular_ela
from model import obtener_modelo

def cargar_detector(modelo_path="mejor_modelo_fraude_nequi.pth", device=None):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    modelo = obtener_modelo("mobilenet_v3_small", pretrained=False, device=device)
    if os.path.exists(modelo_path):
        modelo.load_state_dict(torch.load(modelo_path, map_location=device))
        print(f"✓ Pesos del modelo cargados exitosamente desde: {modelo_path}")
    else:
        print(f"⚠️ Advertencia: No se encontró {modelo_path}. Ejecuta train_evaluate.py primero.")
        
    modelo.eval()
    return modelo, device

def evaluar_comprobante(ruta_imagen, modelo, device, mostrar_grafica=True):
    """
    Analiza una imagen sospechosa y devuelve el veredicto de autenticidad.
    """
    if not os.path.exists(ruta_imagen):
        print(f"❌ Error: La imagen {ruta_imagen} no existe.")
        return None
        
    img_orig = Image.open(ruta_imagen).convert("RGB")
    img_ela = calcular_ela(img_orig, factor_escala=15)
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    tensor_ela = transform(img_ela).unsqueeze(0).to(device)
    
    with torch.no_grad():
        salida = modelo(tensor_ela)
        prob_fraude = torch.sigmoid(salida).item()
        
    es_fraude = prob_fraude >= 0.5
    prob_legitimo = 1.0 - prob_fraude
    
    print("\n" + "="*55)
    print("🔍 REPORTE DE ANÁLISIS FORENSE DIGITAL (NEQUI)")
    print("="*55)
    print(f"Archivo analizado: {os.path.basename(ruta_imagen)}")
    
    if es_fraude:
        print(f"🚨 RESULTADO: [POSIBLE FRAUDE DETECTADO]")
        print(f"   Confianza de Fraude / Manipulación: {prob_fraude*100:.2f}%")
        print("   Diagnóstico: Se detectaron anomalías en la tasa de compresión ELA")
        print("   o desajustes en los patrones visuales de la plantilla.")
    else:
        print(f"✅ RESULTADO: [COMPROBANTE AUTÉNTICO]")
        print(f"   Confianza de Autenticidad: {prob_legitimo*100:.2f}%")
        print("   Diagnóstico: Patrón de ruido homogéneo y coherente con plantilla Nequi.")
    print("="*55)
    
    if mostrar_grafica:
        plt.figure(figsize=(9, 4.5))
        
        plt.subplot(1, 2, 1)
        plt.imshow(img_orig)
        plt.title("Imagen Recibida")
        plt.axis("off")
        
        plt.subplot(1, 2, 2)
        plt.imshow(img_ela)
        color_titulo = "red" if es_fraude else "green"
        veredicto = "ALERTA FRAUDE" if es_fraude else "AUTÉNTICO"
        plt.title(f"Análisis ELA ({veredicto})", color=color_titulo, fontweight="bold")
        plt.axis("off")
        
        plt.tight_layout()
        plt.show()
        
    return {
        "es_fraude": es_fraude,
        "probabilidad_fraude": prob_fraude,
        "probabilidad_legitimo": prob_legitimo
    }

if __name__ == "__main__":
    modelo, device = cargar_detector()
    # Prueba de demostración con una muestra del dataset
    ejemplo_test = "dataset/test/fraude/fraude_test_0001.jpg"
    if os.path.exists(ejemplo_test):
        evaluar_comprobante(ejemplo_test, modelo, device)
