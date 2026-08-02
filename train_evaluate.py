"""
Pipeline de Entrenamiento y Evaluación Rigurosa del Modelo de IA
Calcula métricas clave para el informe académico: F1-Score, Precisión, Recall, ROC-AUC y Matriz de Confusión.
"""

import os
import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_fscore_support

from ela_processor import calcular_ela
from model import obtener_modelo

# Configuración del Dataset con Preprocesamiento ELA integrado
class NequiDataset(Dataset):
    def __init__(self, root_dir, split="train", transform=None, usar_ela=True):
        self.rutas_imagenes = []
        self.etiquetas = [] # 0: Legítimo, 1: Fraude
        self.transform = transform
        self.usar_ela = usar_ela
        
        carpeta_legitimo = os.path.join(root_dir, split, "legitimo")
        carpeta_fraude = os.path.join(root_dir, split, "fraude")
        
        for f in glob.glob(os.path.join(carpeta_legitimo, "*.jpg")):
            self.rutas_imagenes.append(f)
            self.etiquetas.append(0.0)
            
        for f in glob.glob(os.path.join(carpeta_fraude, "*.jpg")):
            self.rutas_imagenes.append(f)
            self.etiquetas.append(1.0)
            
    def __len__(self):
        return len(self.rutas_imagenes)
        
    def __getitem__(self, idx):
        ruta = self.rutas_imagenes[idx]
        etiqueta = self.etiquetas[idx]
        
        img = Image.open(ruta).convert("RGB")
        
        if self.usar_ela:
            img = calcular_ela(img, factor_escala=15)
            
        if self.transform:
            img = self.transform(img)
            
        return img, torch.tensor(etiqueta, dtype=torch.float32)

def entrenar_y_evaluar(dataset_dir="dataset", epochs=12, batch_size=16, lr=0.001):
    # Selección de dispositivo (GPU si está en Colab / CUDA, de lo contrario CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🔧 Utilizando dispositivo: {device}")
    
    # Transformaciones de datos
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.2),
        transforms.RandomRotation(degrees=3),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Cargar Datasets
    train_dataset = NequiDataset(dataset_dir, split="train", transform=train_transform)
    val_dataset = NequiDataset(dataset_dir, split="val", transform=val_test_transform)
    test_dataset = NequiDataset(dataset_dir, split="test", transform=val_test_transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    print(f"📊 Muestras cargadas: Train={len(train_dataset)}, Val={len(val_dataset)}, Test={len(test_dataset)}")
    
    # Instanciar Modelo, Función de Pérdida y Optimizador
    modelo = obtener_modelo("mobilenet_v3_small", pretrained=True, device=device)
    criterio = nn.BCEWithLogitsLoss()
    optimizador = torch.optim.AdamW(modelo.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizador, mode="min", patience=2, factor=0.5)
    
    historial = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
    mejor_val_loss = float("inf")
    mejor_modelo_path = "mejor_modelo_fraude_nequi.pth"
    
    print("\n🧠 Iniciando ciclo de entrenamiento...")
    for epoch in range(epochs):
        # Fase de Entrenamiento
        modelo.train()
        running_loss = 0.0
        correctos = 0
        total = 0
        
        for imagenes, etiquetas in train_loader:
            imagenes = imagenes.to(device)
            etiquetas = etiquetas.to(device).unsqueeze(1)
            
            optimizador.zero_grad()
            salidas = modelo(imagenes)
            loss = criterio(salidas, etiquetas)
            loss.backward()
            optimizador.step()
            
            running_loss += loss.item() * imagenes.size(0)
            preds = (torch.sigmoid(salidas) >= 0.5).float()
            correctos += (preds == etiquetas).sum().item()
            total += etiquetas.size(0)
            
        epoch_train_loss = running_loss / total
        epoch_train_acc = correctos / total
        
        # Fase de Validación
        modelo.eval()
        val_running_loss = 0.0
        val_correctos = 0
        val_total = 0
        
        with torch.no_grad():
            for imagenes, etiquetas in val_loader:
                imagenes = imagenes.to(device)
                etiquetas = etiquetas.to(device).unsqueeze(1)
                
                salidas = modelo(imagenes)
                loss = criterio(salidas, etiquetas)
                
                val_running_loss += loss.item() * imagenes.size(0)
                preds = (torch.sigmoid(salidas) >= 0.5).float()
                val_correctos += (preds == etiquetas).sum().item()
                val_total += etiquetas.size(0)
                
        epoch_val_loss = val_running_loss / val_total
        epoch_val_acc = val_correctos / val_total
        
        scheduler.step(epoch_val_loss)
        
        historial["train_loss"].append(epoch_train_loss)
        historial["val_loss"].append(epoch_val_loss)
        historial["train_acc"].append(epoch_train_acc)
        historial["val_acc"].append(epoch_val_acc)
        
        print(f"Época [{epoch+1:02d}/{epochs:02d}] - Train Loss: {epoch_train_loss:.4f} (Acc: {epoch_train_acc*100:.1f}%) | Val Loss: {epoch_val_loss:.4f} (Acc: {epoch_val_acc*100:.1f}%)")
        
        # Guardar mejor modelo
        if epoch_val_loss < mejor_val_loss:
            mejor_val_loss = epoch_val_loss
            torch.save(modelo.state_dict(), mejor_modelo_path)
            
    print(f"\n💾 Mejor modelo guardado en: {mejor_modelo_path}")
    
    # -------------------------------------------------------------
    # FASE DE EVALUACIÓN FINAL EN CONJUNTO DE PRUEBA (TEST SET)
    # -------------------------------------------------------------
    print("\n🎯 Evaluando en conjunto de prueba independiente (Test Set)...")
    modelo.load_state_dict(torch.load(mejor_modelo_path))
    modelo.eval()
    
    todas_etiquetas = []
    todas_predicciones = []
    todas_probabilidades = []
    
    with torch.no_grad():
        for imagenes, etiquetas in test_loader:
            imagenes = imagenes.to(device)
            salidas = modelo(imagenes)
            probabilidades = torch.sigmoid(salidas).squeeze(1).cpu().numpy()
            predicciones = (probabilidades >= 0.5).astype(int)
            
            todas_etiquetas.extend(etiquetas.numpy())
            todas_predicciones.extend(predicciones)
            todas_probabilidades.extend(probabilidades)
            
    todas_etiquetas = np.array(todas_etiquetas)
    todas_predicciones = np.array(todas_predicciones)
    todas_probabilidades = np.array(todas_probabilidades)
    
    # Generar Reporte de Clasificación
    print("\n" + "="*50)
    print("📈 REPORTE DE CLASIFICACIÓN Y MÉTRICAS FORENSES")
    print("="*50)
    print(classification_report(todas_etiquetas, todas_predicciones, target_names=["Legítimo (0)", "Fraude (1)"]))
    
    # Matriz de Confusión
    cm = confusion_matrix(todas_etiquetas, todas_predicciones)
    tn, fp, fn, tp = cm.ravel()
    
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
    print(f"👉 Tasa de Falsos Positivos (FPR): {fpr*100:.2f}% (Riesgo de acusar cliente inocente)")
    print(f"👉 Tasa de Falsos Negativos (FNR): {fnr*100:.2f}% (Riesgo de aceptar comprobante falso)")
    
    # Curva ROC y AUC
    fpr_vals, tpr_vals, _ = roc_curve(todas_etiquetas, todas_probabilidades)
    roc_auc = auc(fpr_vals, tpr_vals)
    print(f"👉 Área Bajo la Curva ROC (ROC-AUC): {roc_auc:.4f}")
    
    # Graficar y guardar resultados para el informe
    os.makedirs("graficas_informe", exist_ok=True)
    
    # 1. Curvas de Entrenamiento
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(historial["train_loss"], label="Pérdida Entrenamiento", color="#DA0081")
    plt.plot(historial["val_loss"], label="Pérdida Validación", color="#280A32")
    plt.title("Evolución de la Función de Pérdida (Loss)")
    plt.xlabel("Época")
    plt.ylabel("BCE Loss")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.subplot(1, 2, 2)
    plt.plot(historial["train_acc"], label="Exactitud Entrenamiento", color="#00C873")
    plt.plot(historial["val_acc"], label="Exactitud Validación", color="#1C0422")
    plt.title("Evolución de la Exactitud (Accuracy)")
    plt.xlabel("Época")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("graficas_informe/curvas_entrenamiento.png", dpi=300)
    plt.close()
    
    # 2. Matriz de Confusión
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Purples", cbar=False,
                xticklabels=["Legítimo", "Fraude"],
                yticklabels=["Legítimo", "Fraude"])
    plt.title("Matriz de Confusión en Conjunto de Prueba")
    plt.xlabel("Predicción del Modelo")
    plt.ylabel("Etiqueta Real")
    plt.tight_layout()
    plt.savefig("graficas_informe/matriz_confusion.png", dpi=300)
    plt.close()
    
    # 3. Curva ROC
    plt.figure(figsize=(6, 5))
    plt.plot(fpr_vals, tpr_vals, color="#DA0081", lw=2, label=f"Curva ROC (AUC = {roc_auc:.3f})")
    plt.plot([0, 1], [0, 1], color="gray", lw=1, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("Tasa de Falsos Positivos (FPR)")
    plt.ylabel("Tasa de Verdaderos Positivos (TPR - Sensibilidad)")
    plt.title("Curva ROC - Detección de Fraude Nequi")
    plt.legend(loc="lower right")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("graficas_informe/curva_roc.png", dpi=300)
    plt.close()
    
    print("\n📊 Gráficas para el informe académico guardadas en la carpeta 'graficas_informe/':")
    print("  - graficas_informe/curvas_entrenamiento.png")
    print("  - graficas_informe/matriz_confusion.png")
    print("  - graficas_informe/curva_roc.png")

if __name__ == "__main__":
    from data_generator import construir_dataset
    if not os.path.exists("dataset"):
        construir_dataset()
    entrenar_y_evaluar()
