# 📱 Guía Sencilla y Detallada: ¿Cómo Funciona la Detección de Fraude en Nequi con Inteligencia Artificial?
### *Explicación para cualquier persona (sin tecnicismos difíciles, con ejemplos de la vida real)*

---

## 🧭 Resumen en 1 Minuto: La Idea Central
Imagina que tienes una **tienda de barrio o un restaurante**. Un cliente compra algo por **$500.000 pesos**, saca su celular, te muestra la pantalla de Nequi durante 3 segundos con el mensaje *"¡Envío exitoso!"* y se va. 

Minutos después revisas tu cuenta y... **la plata nunca entró**. El cliente te engañó con un **comprobante falso**.

👉 **¿Qué hace nuestro proyecto?**  
Creamos un **sistema inteligente (como un detective digital con una súper lupa)** que mira la foto del comprobante y en **menos de 1 segundo (en milisegundos)** te dice con certeza total:  
*«¡Cuidado! Este comprobante fue editado en Photoshop»* o *«Tranquilo, este comprobante es 100% auténtico»*.

---

## 🔍 Parte 1: ¿Cómo engañan los estafadores hoy en día?

Existen principalmente **dos formas** en las que los delincuentes engañan a las personas:

### 1. Las "Apps Clonadas" (Nequi Fake)
* **¿Qué es?:** Los estafadores instalan una aplicación pirata en su celular que imita los colores morados y la apariencia de Nequi.
* **El truco:** Escriben el nombre del comerciante, le dan al botón y la app pirata dibuja una pantalla idéntica diciendo *"Envío Exitoso"*, pero nunca se conectó con el banco ni transfirió un solo peso.

### 2. La Foto Retocada en Photoshop (La más peligrosa)
* **¿Qué es?:** El estafador hace una transferencia real por solo **$5.000 pesos**. Le toma una captura de pantalla al comprobante original.
* **El truco:** Abre la foto en un programa de edición, borra el número $5.000 y escribe encima **$500.000**, imitando el tipo de letra. A simple vista en la pantalla del celular, el comerciante no nota la diferencia porque los números se ven casi idénticos.

---

## 🕵️‍♂️ Parte 2: El Secreto Forense: ¿Por qué la foto "delata" al mentiroso?

Aquí viene la magia del proyecto. Para entenderlo, usemos una **analogía sencilla**:

### La analogía de la "Pared recién pintada" 🎨
> Imagina una pared blanca que se pintó hace 5 años. Toda la pintura ha envejecido de forma uniforme con el sol y el polvo.  
> Si alguien viene hoy y tapa un hueco con pintura blanca fresca, a 10 metros de distancia la pared se ve blanca... **pero si le pones una lámpara de luz ultravioleta o la tocas con la mano, el parche fresco resalta de inmediato.**

### ¿Qué pasa dentro de un archivo de imagen (JPEG)?
Cuando un celular guarda una imagen (formato JPEG), la comprime en pequeños bloquecitos microscópicos. Toda la foto tiene el mismo "nivel de envejecimiento digital".

Pero si alguien abre la foto, pega números falsos y la vuelve a guardar:
1. Toda la foto original sufre una **compresión**.
2. Los números nuevos sufren una **compresión diferente**.

Nosotros aplicamos una técnica llamada **ELA (Error Level Analysis - Análisis de Nivel de Error)**. Esta técnica actúa exactamente como una **luz ultravioleta**:
* Lo que es original se ve oscuro y parejo.
* **Los números editados BRILLAN como si fueran fluorescentes en la oscuridad.**

---

## 🧠 Parte 3: ¿Cómo funciona el "Cerebro" de Inteligencia Artificial que creamos?

Para no depender de que una persona tenga que mirar la imagen con luz ultravioleta, creamos una **Red Neuronal de Dos Ojos (Dual-Branch)**.

Imagina que tienes a dos expertos trabajando juntos en equipo:

```
                  ┌─────────────────────────────────────────────────┐
                  │          FOTO DEL COMPROBANTE DE PAGO           │
                  └───────────────────────┬─────────────────────────┘
                                          │
                  ┌───────────────────────┴─────────────────────────┐
                  ▼                                                 ▼
     ┌────────────────────────┐                        ┌────────────────────────┐
     │      OJO 1 (VISUAL)    │                        │     OJO 2 (FORENSE)    │
     │  "El Diseñador Gráfico"│                        │   "El Perito Químico"  │
     │                        │                        │                        │
     │ Mira la foto normal:   │                        │ Mira la foto con luz UV│
     │ • Colores morados      │                        │ (Filtro ELA):          │
     │ • Tipografía y logos   │                        │ • ¿Brillan los números?│
     │ • Marco verde del QR   │                        │ • ¿Hay parches ocultos?│
     │ • Márgenes oficiales   │                        │ • ¿Manipularon montos? │
     └────────────┬───────────┘                        └────────────┬───────────┘
                  │                                                 │
                  └───────────────────────┬─────────────────────────┘
                                          ▼
                         ┌─────────────────────────────────┐
                         │       MESA DE DECISIÓN (IA)     │
                         │   Junta las dos opiniones       │
                         └────────────────┬────────────────┘
                                          ▼
                         ┌─────────────────────────────────┐
                         │       DICTAMEN FINAL            │
                         │  🟢 AUTÉNTICO / 🔴 FRAUDE       │
                         │      (En 45 milisegundos)       │
                         └─────────────────────────────────┘
```

1. **Ojo 1 (El Diseñador):** Revisa la imagen a color. Descubre de inmediato las aplicaciones clonadas porque no tienen el código QR oficial o los colores están ligeramente corridos.
2. **Ojo 2 (El Perito Forense):** Revisa el mapa espectral (ELA). Descubre si los números fueron sobreescritos.
3. **El Juez:** Combina la información de ambos ojos y da un porcentaje de seguridad.

---

## 📊 Parte 4: ¿Qué tan buenos fueron los resultados? (En números claros)

Probamos el modelo con **80 comprobantes nuevos** que la IA nunca antes había visto (40 reales y 40 con trampas de diferente tipo):

| Pregunta Clave | Resultado Obtenido | ¿Qué significa en la vida real? |
| :--- | :---: | :--- |
| **¿Cuántos fraudes se le escaparon?** | **0 de 40 (0%)** | **Sensibilidad del 100%**. Ningún estafador logró meter un comprobante falso sin ser atrapado. Cero pérdidas para el comerciante. |
| **¿Cuántas veces se equivocó en total?** | **1 sola vez de 80** | **Exactitud del 98.75%**. Solo en 1 caso dudó de un comprobante real por exceso de precaución. |
| **¿Cuánto se demora en responder?** | **0.045 segundos** | Es tan rápido que el comerciante no tiene que esperar nada en la fila. |
| **¿Cuánto pesa el programa?** | **11 Megabytes** | Pesa menos que una canción de Spotify, cabe en cualquier celular barato o datáfono. |

---

## 🛡️ Parte 5: Equidad y Protección de la Privacidad (Ética)

### 1. No discrimina celulares baratos ni fotos de WhatsApp
* Muchas personas en Colombia usan celulares económicos con cámaras sencillas o envían los comprobantes por WhatsApp (lo que hace que la foto pierda calidad y se vea borrosa).
* Si hubiéramos entrenado a la IA solo con fotos perfectas de iPhone, rechazaría injustamente a la gente humilde.
* Por eso, **entrenamos a la IA con fotos borrosas, comprimidas y de baja calidad**, logrando que distinga perfectamente entre una foto de WhatsApp y una estafa real.

### 2. Privacidad Total (Ley de Habeas Data)
* La IA no guarda fotos, nombres, números de cédula ni cuentas bancarias en ningún servidor.
* La foto entra a la memoria del celular, la IA la analiza en milésimas de segundo, da el resultado y **la borra al instante**.

---

## 🚀 Conclusión: ¿Por qué es un proyecto valioso?
Porque le devuelve la tranquilidad a los tenderos, taxistas, restaurantes y emprendedores colombianos. Con esta tecnología en su propio celular o datáfono, **nunca más perderán el fruto de su trabajo por culpa de un comprobante falso**.
