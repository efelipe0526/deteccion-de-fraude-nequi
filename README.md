# 📱 Detección de Falsificación de Comprobantes de Pago Digital (Nequi)
### Asignatura: Inteligencia Artificial Avanzada | Metodología: Aprendizaje Basado en Retos (ABR)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/efelipe0526/deteccion-de-fraude-nequi/blob/main/Deteccion_Fraude_Nequi_IA_Avanzada.ipynb)

---

## 🚀 Ejecución Inmediata en Google Colab

Puedes abrir y ejecutar todo el proyecto con un solo clic presionando el botón superior **"Open In Colab"** o siguiendo estos pasos:

1. Ingresa a [Google Colab](https://colab.research.google.com/).
2. Ve a la pestaña **GitHub**.
3. Ingresa la URL del repositorio: `https://github.com/efelipe0526/deteccion-de-fraude-nequi`
4. Selecciona el archivo `Deteccion_Fraude_Nequi_IA_Avanzada.ipynb`.
5. En el menú superior de Colab:
   * **Entorno de ejecución > Cambiar tipo de entorno de ejecución** y selecciona **T4 GPU**.
   * **Entorno de ejecución > Ejecutar todas las celdas (Ctrl + F9)**.

---

## 📂 Estructura del Repositorio

* 📓 **`Deteccion_Fraude_Nequi_IA_Avanzada.ipynb`**: Cuaderno completo autocontenido para Google Colab con visualizaciones, entrenamiento, matriz de confusión, curva ROC, análisis de equidad y widget interactivo para subir comprobantes.
* 🐍 **`data_generator.py`**: Generador estocástico de comprobantes sintéticos legítimos y fraudulentos (Photoshop, Nequi Fake, etc.).
* 🔬 **`ela_processor.py`**: Algoritmo de Error Level Analysis (ELA) para forense digital de compresión JPEG.
* 🧠 **`model.py`**: Arquitectura de Red Neuronal Convolucional (CNN / MobileNetV3) en PyTorch.
* 📈 **`train_evaluate.py`**: Script de entrenamiento, validación y generación de gráficas en alta resolución para el informe académico.
* 🔍 **`inference_demo.py`**: Evaluador de comprobantes individuales en tiempo real.
* 🛡️ **`.gitignore`**: Exclusión de archivos temporales y checkpoints pesados.

---

## 🎯 Arquitectura del Modelo de IA

El sistema utiliza un enfoque híbrido de dos etapas:
1. **Análisis Forense Digital (ELA):** Detecta discontinuidades en la matriz de cuantización JPEG producidas al alterar campos de texto (monto, fecha, referencia).
2. **Clasificación Profunda (MobileNetV3 + Head Densa):** Red neuronal convolucional ajustada (*Fine-Tuning*) con capas de Batch Normalization y Dropout para clasificar entre comprobante legítimo y fraudulento con alta resiliencia al ruido.

---

## 📝 Mapeo con los Criterios de Evaluación Universitaria

| Sección del Informe Escrito | Celda / Módulo del Proyecto |
| :--- | :--- |
| **1. Introducción y Justificación** | Sección 1 del cuaderno: Impacto del fraude en pagos móviles y comercios. |
| **2. Revisión de Literatura** | Sección 3: Fundamento matemático de ELA, CNNs y forense digital. |
| **3. Diseño del Modelo y Metodología** | Sección 2 y 4: Pipeline generador de datos y MobileNetV3 con Transfer Learning. |
| **4. Resultados y Evaluación** | Sección 5 y 6: Curvas Loss/Acc, Matriz de Confusión, ROC-AUC, F1-Score. |
| **5. Discusión sobre Equidad y Ética** | Sección 7: Prueba de estrés bajo compresión de WhatsApp y *Habeas Data* (Ley 1581). |
| **6. Conclusiones y Recomendaciones** | Sección 8: Factibilidad de despliegue en punto de venta y trabajo futuro. |
