# 📱 Detección de Falsificación de Comprobantes de Pago Digital (Nequi)
### Asignatura: Inteligencia Artificial Avanzada | Metodología: Aprendizaje Basado en Retos (ABR)

---

## 🚀 Cómo Subir y Ejecutar el Proyecto en Google Colab

1. **Abre tu navegador** e ingresa a [Google Colab](https://colab.research.google.com/).
2. Haz clic en la pestaña **Subir / Upload**.
3. Selecciona el archivo:
   👉 `Deteccion_Fraude_Nequi_IA_Avanzada.ipynb`
4. En el menú superior de Google Colab:
   * Ve a **Entorno de ejecución (Runtime) > Cambiar tipo de entorno de ejecución**.
   * Selecciona aceleración por hardware: **T4 GPU** (o CPU, ambas funcionan perfectamente).
5. Haz clic en **Entorno de ejecución > Ejecutar todas las celdas (Ctrl + F9)**.

---

## 📂 Estructura de Archivos del Proyecto

* 📓 **`Deteccion_Fraude_Nequi_IA_Avanzada.ipynb`**: Cuaderno completo autocontenido para Google Colab con visualizaciones, entrenamiento, matriz de confusión, curva ROC, análisis de equidad y widget interactivo para subir comprobantes.
* 🐍 **`data_generator.py`**: Generador estocástico de comprobantes sintéticos legítimos y fraudulentos (Photoshop, Nequi Fake, etc.).
* 🔬 **`ela_processor.py`**: Algoritmo de Error Level Analysis (ELA) para forense digital de compresión JPEG.
* 🧠 **`model.py`**: Arquitectura de Red Neuronal Convolucional (CNN / MobileNetV3) en PyTorch.
* 📈 **`train_evaluate.py`**: Script de entrenamiento, validación y generación de gráficas en alta resolución para el informe escrito.
* 🔍 **`inference_demo.py`**: Evaluador de comprobantes individuales en tiempo real.

---

## 📝 Mapeo con los Entregables de la Actividad

| Sección del Informe Escrito | Celda / Módulo del Proyecto |
| :--- | :--- |
| **1. Introducción y Justificación** | Sección 1 del cuaderno: Impacto del fraude en pagos móviles y comercios. |
| **2. Revisión de Literatura** | Sección 3: Fundamento matemático de ELA, CNNs y forense digital. |
| **3. Diseño del Modelo y Metodología** | Sección 2 y 4: Pipeline generador de datos y MobileNetV3 con Transfer Learning. |
| **4. Resultados y Evaluación** | Sección 5 y 6: Curvas Loss/Acc, Matriz de Confusión, ROC-AUC, F1-Score. |
| **5. Discusión sobre Equidad y Ética** | Sección 7: Prueba de estrés bajo compresión de WhatsApp y *Habeas Data* (Ley 1581). |
| **6. Conclusiones y Recomendaciones** | Sección 8: Factibilidad de despliegue en punto de venta y trabajo futuro. |
