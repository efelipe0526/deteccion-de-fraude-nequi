"""
Arquitectura del Modelo de Inteligencia Artificial para Detección de Fraude
Implementa una Red Neuronal Convolucional (CNN) adaptada para señales forenses de compresión y patrones visuales.
"""

import torch
import torch.nn as nn
import torchvision.models as models

class DetectorFraudeNequi(nn.Module):
    """
    Modelo de clasificación binaria basado en Transfer Learning (EfficientNet-B0 / MobileNetV3)
    optimizado para analizar características de compresión ELA y geometría de comprobantes.
    """
    def __init__(self, backbone="mobilenet_v3_small", pretrained=True, num_clases=1):
        super(DetectorFraudeNequi, self).__init__()
        
        self.backbone_name = backbone
        
        if backbone == "mobilenet_v3_small":
            weights = models.MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
            self.extractor = models.mobilenet_v3_small(weights=weights)
            in_features = self.extractor.classifier[0].in_features
            
            # Reemplazar la cabeza clasificadora
            self.extractor.classifier = nn.Sequential(
                nn.Linear(in_features, 256),
                nn.BatchNorm1d(256),
                nn.ReLU(inplace=True),
                nn.Dropout(p=0.4),
                nn.Linear(256, 64),
                nn.ReLU(inplace=True),
                nn.Dropout(p=0.2),
                nn.Linear(64, num_clases)
            )
            
        elif backbone == "efficientnet_b0":
            weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
            self.extractor = models.efficientnet_b0(weights=weights)
            in_features = self.extractor.classifier[1].in_features
            
            self.extractor.classifier = nn.Sequential(
                nn.Linear(in_features, 256),
                nn.BatchNorm1d(256),
                nn.SiLU(inplace=True),
                nn.Dropout(p=0.4),
                nn.Linear(256, num_clases)
            )
            
        elif backbone == "custom_cnn":
            # Arquitectura convolucional propia para análisis forense directo
            self.extractor = nn.Sequential(
                nn.Conv2d(3, 32, kernel_size=3, padding=1),
                nn.BatchNorm2d(32),
                nn.ReLU(),
                nn.MaxPool2d(2, 2),
                
                nn.Conv2d(32, 64, kernel_size=3, padding=1),
                nn.BatchNorm2d(64),
                nn.ReLU(),
                nn.MaxPool2d(2, 2),
                
                nn.Conv2d(64, 128, kernel_size=3, padding=1),
                nn.BatchNorm2d(128),
                nn.ReLU(),
                nn.MaxPool2d(2, 2),
                
                nn.Conv2d(128, 256, kernel_size=3, padding=1),
                nn.BatchNorm2d(256),
                nn.ReLU(),
                nn.AdaptiveAvgPool2d((1, 1)),
                nn.Flatten(),
                
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Dropout(0.4),
                nn.Linear(128, num_clases)
            )

    def forward(self, x):
        return self.extractor(x)

def obtener_modelo(nombre_arquitectura="mobilenet_v3_small", pretrained=True, device="cpu"):
    """Instancia el modelo y lo transfiere al dispositivo especificado (CPU o CUDA)."""
    modelo = DetectorFraudeNequi(backbone=nombre_arquitectura, pretrained=pretrained)
    modelo = modelo.to(device)
    return modelo
