"""
Arquitectura Dual-Branch (RGB + ELA) para Clasificación Robusta de Comprobantes Nequi
Aprende características visuales (diseño, QR, layout) y forenses (compresión ELA) de forma end-to-end
sin depender de umbrales rígidos de color o coordenadas fijas.
"""

import torch
import torch.nn as nn
from torchvision import models

class NequiDualBranchCNN(nn.Module):
    """
    Red Neuronal Siamesa/Dual-Branch:
    - Rama 1: Analiza la imagen RGB original (estructura visual, QR, tiquete, logos).
    - Rama 2: Analiza el mapa ELA (artefactos forenses, parches de compresión).
    """
    def __init__(self, pretrained=True):
        super(NequiDualBranchCNN, self).__init__()
        
        weights = models.MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
        
        # Rama Visual (RGB)
        base_rgb = models.mobilenet_v3_small(weights=weights)
        self.branch_rgb = base_rgb.features
        self.pool_rgb = nn.AdaptiveAvgPool2d((1, 1))
        
        # Rama Forense (ELA)
        base_ela = models.mobilenet_v3_small(weights=weights)
        self.branch_ela = base_ela.features
        self.pool_ela = nn.AdaptiveAvgPool2d((1, 1))
        
        # Dimensión de características de MobileNetV3 Small = 576
        feat_dim = 576 * 2
        
        # Clasificador de Fusión
        self.classifier = nn.Sequential(
            nn.Linear(feat_dim, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.3),
            nn.Linear(256, 64),
            nn.ReLU(inplace=True),
            nn.Linear(64, 1)
        )
        
    def forward(self, x_rgb, x_ela):
        f_rgb = self.branch_rgb(x_rgb)
        f_rgb = self.pool_rgb(f_rgb).flatten(1)
        
        f_ela = self.branch_ela(x_ela)
        f_ela = self.pool_ela(f_ela).flatten(1)
        
        fused = torch.cat([f_rgb, f_ela], dim=1)
        out = self.classifier(fused)
        return out
