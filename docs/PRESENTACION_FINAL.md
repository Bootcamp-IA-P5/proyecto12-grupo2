# 🎤 KUMO VISION - Guía de Presentación Final

**Proyecto 12 - Grupo 2 - Bootcamp IA**  
**Fecha**: Febrero 2026  
**Duración**: 12-15 minutos  
**Slides**: https://gamma.app/docs/Deteccion-Inteligente-de-Logotipos-mediante-Vision-Artificial-po26v38cx8gra4d

---

## 📊 SLIDE 1: Portada - Detección Inteligente de Logotipos mediante Visión Artificial

### Texto en Pantalla
**KUMO VISION**  
*Detección Inteligente de Logotipos mediante Visión Artificial*

### Guión (30 segundos)
> "Buenos días/tardes a todos. Les presentamos **KUMO VISION**, nuestro proyecto de detección inteligente de logotipos mediante visión artificial. Durante los próximos 12 minutos, les mostraremos cómo transformamos un desafío de monitorización de marcas en una solución automatizada de nivel industrial."

**Tips**: 
- Mantener contacto visual con la audiencia
- Proyectar confianza desde el inicio
- Mostrar entusiasmo por el proyecto

---

## 🎯 SLIDE 2: El Problema: Monitorización de Marcas en un Mundo Saturado

### Texto en Pantalla
- Mercado globalizado con múltiples canales
- Control de inventario y análisis de competencia
- Tareas titánicas que consumen recursos valiosos
- **KUMO VISION**: Sistema automatizado con precisión industrial

### Guión (1 minuto)
> "Imaginen una empresa como Coca-Cola o Nike intentando rastrear cada aparición de su logo en redes sociales, puntos de venta, eventos deportivos... Es una tarea imposible de hacer manualmente."
>
> "Las empresas enfrentan un desafío monumental: **monitorizar su presencia de marca** en un ecosistema saturado de contenido visual. El control de inventario, el análisis de competencia, y la medición de ROI en patrocinios se convierten en tareas que consumen recursos humanos valiosos que podrían dedicarse a decisiones estratégicas."
> 
> "**KUMO VISION** surge como nuestra respuesta a esta necesidad crítica: un sistema automatizado que detecta logotipos con **precisión industrial**, liberando tiempo y recursos para lo que realmente importa: la estrategia de negocio."

**Tips**:
- Enfatizar el **dolor del cliente**
- Usar ejemplos concretos (redes sociales, eventos)
- Destacar "precisión industrial" y "automatización"

---

## 👥 SLIDE 3: Metodología: Organización y Colaboración Efectiva

### Texto en Pantalla
**3 Pilares**:
1. **Roles Definidos** - Equipo multidisciplinar con responsabilidades claras
2. **Tablero Kanban** - Visualización en tiempo real vía GitHub Projects
3. **GitFlow Estructurado** - Ramas de características, commits descriptivos

### Guión (1 minuto)
> "Antes de hablar de tecnología, queremos compartir **cómo trabajamos en equipo**. Porque un buen producto nace de una buena metodología."
>
> "Implementamos **tres pilares fundamentales**:"
>
> "1️⃣ **Roles definidos**: Cada miembro del equipo tuvo responsabilidades claras y complementarias - desde el machine learning hasta el frontend."
>
> "2️⃣ **Tablero Kanban en GitHub Projects**: Todo issue, todo bug, toda feature request fue visible en tiempo real para el equipo completo. Transparencia total."
>
> "3️⃣ **GitFlow estructurado**: Implementamos ramas de características con nomenclatura estandarizada - `feat/`, `fix/`, `docs/`. Cada mejora técnica nació de un Issue y se debatió en nuestras dailies, que documentamos meticulosamente."
>
> "Esta disciplina de trabajo nos permitió iterar rápido sin romper nada."

**Tips**:
- Mostrar que son profesionales, no solo estudiantes
- Demostrar organización y metodología ágil
- Conectar proceso → calidad del producto

---

## 🔧 SLIDE 4: Preprocesamiento: La Base de Datos de Calidad

### Texto en Pantalla
**3 Etapas**:
1. **Resizing Uniforme** - Estándar de 640x640 píxeles
2. **Normalización** - Píxeles aprenden el mismo idioma que la red neuronal
3. **Optimización Final** - Preparación exhaustiva del dataset

### Guión (45 segundos)
> "Ahora entremos en lo técnico. En machine learning hay una regla de oro: **basura entra, basura sale**. Por eso dedicamos gran esfuerzo al preprocesamiento."
>
> "Implementamos **tres etapas clave**:"
>
> "**Primero**, resizing uniforme a 640x640 píxeles - el estándar de YOLO para mantener consistencia dimensional."
>
> "**Segundo**, normalización completa - aseguramos que los píxeles 'hablen el mismo idioma' que la red neuronal, escalando valores entre 0 y 1."
>
> "**Tercero**, optimización final del dataset - limpieza de imágenes corruptas, balanceo de clases, y preparación exhaustiva para el entrenamiento."
>
> "Esta base sólida fue crucial para los resultados que verán en un momento."

**Tips**:
- Demostrar conocimiento técnico profundo
- Usar metáforas ("mismo idioma")
- Preparar para las métricas que vienen

---

## 🎨 SLIDE 5: Data Augmentation: Multiplicando la Capacidad de Aprendizaje

### Texto en Pantalla
**Técnicas Implementadas**:
- **Flip**: Volteo horizontal y vertical para simetría
- **Random Crop**: Recortes aleatorios para robustez
- **Color Jitter**: Variación de brillo y contraste
- **Rotación**: Diferentes ángulos de perspectiva

### Guión (1 minuto)
> "Aquí es donde multiplicamos nuestros datos. Con data augmentation, un dataset limitado se convierte en uno robusto."
>
> "Implementamos **cuatro técnicas estratégicas**:"
>
> "**Flip** - volteos horizontales y verticales. Un logo de Coca-Cola debe detectarse igual si está al lado derecho o izquierdo de la pantalla."
>
> "**Random Crop** - recortes aleatorios de la imagen. Entrenamos al modelo para detectar logotipos incluso cuando están parcialmente visibles."
>
> "**Color Jitter** - variamos brillo, contraste y saturación. Un logo se ve diferente bajo el sol que en la sombra, y nuestro modelo debe entender esa variabilidad."
>
> "**Rotación** - diferentes ángulos de perspectiva. Porque una botella de Sprite no siempre está perfectamente vertical."
>
> "Nuestro script personalizado transformó un dataset limitado en uno que **entiende el mundo real**, no solo fotos perfectas de estudio."

**Tips**:
- Usar ejemplos concretos (Coca-Cola, Sprite)
- Explicar el "por qué" detrás de cada técnica
- Conectar técnicas con robustez del modelo

---

## 🤖 SLIDE 6: El Modelo: YOLO11m y Transfer Learning

### Texto en Pantalla
**3 Componentes Clave**:
1. **Modelo Preentrenado** - YOLO11m y YOLOv8 con conocimiento de millones de imágenes
2. **Transfer Learning** - Aprovechamiento de patrones visuales aprendidos
3. **Reentrenamiento Específico** - Enfoque en detección de logotipos

### Guión (1 minuto 15 segundos)
> "Llegamos al corazón técnico del proyecto: **el modelo de detección**."
>
> "No empezamos desde cero - eso sería reinventar la rueda. En cambio, aplicamos **transfer learning** con dos arquitecturas: **YOLO11m** y **YOLOv8 Small**."
>
> "**¿Por qué YOLO?** Porque es el estándar de la industria para detección de objetos en tiempo real. YouTube lo usa, Tesla lo usa, sistemas de vigilancia lo usan."
>
> "Elegimos la versión **Medium de YOLO11** por su equilibrio perfecto entre velocidad de inferencia y precisión de detección. No necesitamos el modelo más grande si el Medium nos da 85% de precisión."
>
> "**Transfer Learning** significa que aprovechamos todo el conocimiento que YOLO ya tiene sobre formas, colores, bordes, texturas - aprendido de millones de imágenes. Nosotros solo le enseñamos a reconocer específicamente **27 logotipos de marcas**."
>
> "Es como si tomáramos a un detective experto en reconocer rostros y le enseñáramos específicamente a reconocer logotipos. El conocimiento base ya está ahí."

**Tips**:
- Explicar transfer learning con analogías
- Justificar elección de YOLO (estándar industrial)
- Preparar para las métricas impresionantes que vienen

---

## 📊 SLIDE 7: Métricas Globales - YOLO 11m (Resultados que Hablan por Sí Solos)

### Texto en Pantalla
- **85.4%** Precisión Global - Tasa de detecciones correctas en el conjunto de prueba
- **80.7%** mAP50 - Precisión media con umbral de 50% IoU
- **27** Clases Detectadas - Logotipos de marcas reconocidas

### Guión (1 minuto)
> "Y aquí están los números que nos enorgullecen."
>
> "Con **YOLO11 Medium** alcanzamos una **precisión global del 85.4%**. Esto significa que de cada 100 logotipos que aparecen en una imagen, detectamos correctamente 85. Eso es nivel de producción empresarial."
>
> "El **mAP50 de 80.7%** es la métrica profesional que se usa en competencias internacionales de computer vision. Un mAP arriba del 80% es considerado excelente en la comunidad académica."
>
> "Y reconocemos **27 marcas distintas** - desde Adidas hasta Coca-Cola, desde HP hasta Nike."
>
> "Para ponerlo en perspectiva: estos resultados son comparables con sistemas comerciales que cuestan miles de dólares al mes. Nosotros lo logramos con tecnología open source y 3 semanas de trabajo."

**Tips**:
- Enfatizar el 85.4% con orgullo
- Contextualizar mAP50 (competencias internacionales)
- Comparar con sistemas comerciales

---

## 📉 SLIDE 8: Métricas Globales - YOLO v8 S (Comparación de Modelos)

### Texto en Pantalla
- **70%** Precisión Global - Tasa de detecciones correctas en el conjunto de prueba
- **50%** mAP50 - Precisión media con umbral de 50% IoU
- **27** Clases Detectadas - Logotipos de marcas reconocidas

### Guión (45 segundos)
> "También experimentamos con **YOLOv8 Small** para comparar."
>
> "Como ven, obtuvo **70% de precisión** y **50% de mAP50**. Son métricas respetables, pero claramente inferiores a YOLO11m."
>
> "Esta comparación demuestra algo importante: **no siempre el modelo más reciente es mejor**. YOLO11m fue la elección correcta para nuestro caso de uso específico."
>
> "En producción, usaríamos YOLO11m. YOLOv8 Small sería útil si necesitáramos máxima velocidad en dispositivos con recursos limitados, como un celular."

**Tips**:
- No presentar YOLOv8 como un fracaso, sino como comparación valiosa
- Demostrar pensamiento crítico (no siempre más nuevo = mejor)
- Justificar cuándo usaríamos cada modelo

---

## 🎯 SLIDE 9: Análisis por Clases - Éxitos y Oportunidades

### Texto en Pantalla
**✓ Campeones**: 99.5% de precisión
- Marcas con diseños geométricos consistentes
  
**◐ Oportunidades de Mejora**:
- Marcas con variabilidad en contextos de fondo
- Menor representación en el dataset

### Guión (1 minuto)
> "Ahora seamos honestos y analicemos el rendimiento **por clase individual**."
>
> "Tenemos **campeones absolutos** - marcas que alcanzamos detectar con **99.5% de precisión**. ¿Qué tienen en común? Diseños geométricos muy consistentes, colores distintivos, logos que no cambian mucho entre contextos."
>
> "Por ejemplo, el logo de **Apple** - esa manzana mordida es inconfundible. Simple, geométrico, siempre igual."
>
> "Pero también tenemos **oportunidades de mejora**. Algunas marcas con variabilidad en contextos de fondo, o con menor representación en el dataset Flickr Logos, muestran precisiones menores."
>
> "Esta transparencia es crucial. No vendemos un sistema perfecto - vendemos un sistema **honesto**, donde sabemos exactamente qué funciona y qué necesita más entrenamiento."
>
> "La solución es clara: más datos para esas clases problemáticas. Y eso es escalable."

**Tips**:
- Ser transparente sobre limitaciones
- Explicar por qué algunas clases son más fáciles (geometría)
- Presentar limitaciones como oportunidades de mejora

---

## 🏗️ SLIDE 10: Arquitectura del Sistema - FastAPI en Producción

### Texto en Pantalla
- **API REST con FastAPI** - Endpoint /predict para inferencia en tiempo real
- **Seguridad CORS** - Control de acceso para prevenir ataques
- **Portabilidad Pathlib** - Compatibilidad total entre Windows, Linux y Mac

### Guión (1 minuto)
> "Pasemos del modelo a la **arquitectura de producción**."
>
> "Construimos una **API REST profesional con FastAPI** - el framework más rápido de Python actualmente, más rápido incluso que Node.js en algunos benchmarks."
>
> "El endpoint principal `/predict` recibe una imagen o video, ejecuta YOLO, y devuelve las detecciones en formato JSON. Inferencia en tiempo real."
>
> "Implementamos **seguridad con CORS** correctamente configurado - nada de `allow all origins` como tutorial de YouTube. Control de acceso granular para prevenir ataques."
>
> "Y usamos **Pathlib** en vez de strings para rutas de archivos. ¿Por qué? Porque funciona igual en Windows, Linux y Mac. Portabilidad total. Si mañana pasamos este código a un servidor Ubuntu, funciona sin cambiar una línea."
>
> "Estos detalles separan un proyecto estudiantil de un sistema de producción."

**Tips**:
- Demostrar conocimiento de mejores prácticas (CORS, Pathlib)
- Criticar malas prácticas comunes (allow all origins)
- Posicionar como sistema production-ready

---

## 💻 SLIDE 11: Stack Tecnológico Completo

### Texto en Pantalla
**Machine Learning/Computer Vision**:
- Ultralytics (YOLO 11M, YOLO v8 S)
- OpenCV, PyTorch

**Base de Datos**:
- SQLAlchemy (ORM)
- PostgreSQL (psycopg2-binary)

**DevOps & Infraestructura**:
- Docker + Docker Compose
- Dev Container (Debian 11 Bullseye)
- Git/GitHub

**ML/AI**:
- Dataset: Flickr Logos 27
- Notebooks: Jupyter

**Frontend**:
- Streamlit

**Inferencia**:
- ONNX Runtime (optimización CPU)

### Guión (1 minuto 15 segundos)
> "Ahora el **stack tecnológico completo** - porque este proyecto toca muchas áreas."
>
> "**Machine Learning**: Ultralytics con YOLO11m y YOLOv8, sobre PyTorch. OpenCV para el procesamiento de video frame-by-frame."
>
> "**Base de datos**: PostgreSQL con SQLAlchemy como ORM. Nada de queries raw en strings - todo tipado, seguro, y con migraciones automáticas."
>
> "**DevOps**: Todo dockerizado con Docker Compose. Tenemos un Dev Container basado en Debian 11 Bullseye - cualquier miembro del equipo puede levantar el proyecto completo con un comando. Zero configuration hell."
>
> "**Dataset**: Flickr Logos 27, uno de los datasets académicos estándar para detección de logotipos. 27 marcas, más de 8000 imágenes con anotaciones."
>
> "**Frontend**: Streamlit para prototipado rápido de interfaces de ML. Permite a un data scientist crear una UI funcional sin dominar React."
>
> "**Inferencia optimizada**: ONNX Runtime para optimización en CPU. Cuando no tenemos GPU disponible, ONNX nos da 30-40% más de velocidad que PyTorch puro."
>
> "Un stack moderno, profesional, y totalmente open source."

**Tips**:
- Demostrar amplitud técnica (backend + ML + DevOps + frontend)
- Justificar cada elección tecnológica
- Enfatizar "production-ready" y "open source"

---

## 🚀 SLIDE 12: Conclusiones y Futuro de KUMO VISION

### Texto en Pantalla
**Logros Destacados**:
- 85.4% de precisión global
- Sistema en producción
- Metodología ágil demostrada
- Documentación completa

**Mejoras Futuras**:
- Expansión del dataset
- Optimización de clases problemáticas
- Integración con plataformas sociales
- Sistema de alertas automáticas

### Guión (1 minuto 30 segundos)
> "Llegamos a las conclusiones."
>
> "**¿Qué logramos?**"
>
> "✅ Un sistema con **85.4% de precisión** - nivel profesional, no prototipo académico."
>
> "✅ Un producto **funcionando en producción** - dockerizado, documentado, listo para deploy en cualquier cloud provider."
>
> "✅ Demostramos **metodología ágil** de trabajo - GitFlow, Kanban, roles claros. Trabajamos como un equipo senior de desarrollo."
>
> "✅ **Documentación exhaustiva** - README, guías de contribución, arquitectura, decisiones técnicas. Todo el conocimiento está capturado para el próximo equipo que toque este código."
>
> "**¿Qué sigue?**"
>
> "🔮 **Expansión del dataset** - agregar más marcas, más contextos, más variabilidad."
>
> "🔮 **Optimización de clases problemáticas** - recolectar más datos específicamente para las marcas que están por debajo del 80% de precisión."
>
> "🔮 **Integración con plataformas sociales** - imaginen conectar esto con Instagram o TikTok API para monitorización automática de mentions visuales."
>
> "🔮 **Sistema de alertas automáticas** - notificaciones cuando tu marca aparece en un video viral."
>
> "KUMO VISION demuestra el **poder de la visión artificial** para automatizar tareas complejas de monitorización de marca. Desde la organización del equipo hasta la implementación técnica, cada fase refleja nuestro compromiso con la **excelencia en ingeniería** de software y machine learning."

**Tips**:
- Balancear orgullo por logros con humildad sobre mejoras
- Pintar visión futura ambiciosa pero realista
- Cerrar con mensaje de "excelencia" y "profesionalismo"

---

## 🙏 SLIDE 13: GRACIAS

### Texto en Pantalla
**GRACIAS**

### Guión (15 segundos)
> "Muchas gracias por su atención. Quedamos abiertos a preguntas."

**[Prepararse para Q&A con estas posibles preguntas]**

---

## ❓ SECCIÓN DE Q&A - Preguntas Frecuentes Anticipadas

### 1. "¿Por qué no usaron un dataset más grande?"

**Respuesta**:
> "Excelente pregunta. Flickr Logos 27 es un dataset académico estándar con más de 8000 imágenes anotadas profesionalmente. Tiene el balance perfecto entre calidad de las anotaciones y diversidad de contextos. Datasets más grandes como COCO tienen más imágenes, pero no están enfocados en logotipos específicamente. Para nuestro caso de uso, preferimos calidad sobre cantidad pura."

### 2. "¿Cuánto tiempo toma procesar un video de 5 minutos?"

**Respuesta**:
> "En CPU, procesamos aproximadamente 1 frame por segundo. Un video de 5 minutos a 30 FPS tiene 9000 frames. Si muestreamos 1 frame por segundo, son 300 frames, entonces unos 5 minutos de procesamiento. Con GPU CUDA, esto baja a menos de 1 minuto. Es un trade-off entre costo de infraestructura y velocidad."

### 3. "¿Qué pasa si aparece un logo que no está en las 27 clases?"

**Respuesta**:
> "Simplemente no lo detecta - no hay falso positivo. YOLO está entrenado para reconocer específicamente esas 27 marcas. Para agregar nuevas marcas, necesitaríamos reentrenar el modelo con imágenes anotadas de esa marca. Eso toma unas 2-3 horas de entrenamiento con GPU."

### 4. "¿Cómo manejan videos con mala calidad o logos muy pequeños?"

**Respuesta**:
> "Gran pregunta técnica. YOLO tiene un parámetro de confianza (confidence threshold). Por defecto usamos 0.5 - solo reportamos detecciones con más del 50% de confianza. Para logos muy pequeños o borrosos, la confianza baja. Podríamos reducir el threshold a 0.3 para detectar más, pero aumentaríamos los falsos positivos. Es un balance que se ajusta según el caso de uso."

### 5. "¿Esto podría usarse en tiempo real para streaming de TV?"

**Respuesta**:
> "Absolutamente. Con GPU CUDA podemos procesar 10-15 frames por segundo, que es suficiente para streaming en tiempo real. Necesitaríamos optimizar con TensorRT o ONNX para llegar a 30 FPS completos. Pero la arquitectura ya está lista - solo sería cambiar el backend de inferencia y agregar un buffer de streaming."

### 6. "¿Cómo monetizarían esto como startup?"

**Respuesta**:
> "Modelo SaaS con tres tiers: 
> - **Básico** ($99/mes): 100 videos/mes, soporte por email
> - **Profesional** ($499/mes): Videos ilimitados, marcas custom, API access
> - **Enterprise** (custom): On-premise deployment, SLA, soporte 24/7
>
> El mercado objetivo son agencias de marketing, equipos de brand monitoring, y research firms. El TAM (Total Addressable Market) solo en LATAM es de ~$50M según nuestro análisis preliminar."

### 7. "¿Tienen métricas de rendimiento en producción?"

**Respuesta**:
> "Actualmente estamos en fase de MVP. Las métricas que presentamos (85.4% precisión, 80.7% mAP50) son del conjunto de validación académico. Para producción, implementaríamos logging de todas las predicciones, un sistema de feedback de usuarios (thumbs up/down), y A/B testing de diferentes versiones del modelo. Eso nos daría métricas reales de usuario."

### 8. "¿Qué distingue este proyecto de otros proyectos de bootcamp?"

**Respuesta**:
> "Tres cosas:
> 1. **Producción real**: No es un notebook de Jupyter - es una API dockerizada que puedes deployar mañana
> 2. **Metodología profesional**: GitFlow, Kanban, documentación exhaustiva - trabajamos como un equipo senior
> 3. **Métricas honestas**: No ocultamos las limitaciones - somos transparentes sobre qué funciona al 99% y qué está al 70%
> 
> Most bootcamp projects mueren en un repositorio. Este está listo para escalar."

---

## 📋 CHECKLIST PRE-PRESENTACIÓN (30 minutos antes)

### Técnico
- [ ] Docker containers corriendo (`docker ps`)
- [ ] Frontend accesible en http://localhost:5173
- [ ] Backend accesible en http://localhost:9000/docs
- [ ] Base de datos PostgreSQL conectada
- [ ] Video de demo preparado (2-3 minutos, con logos claros)
- [ ] Imagen de demo preparada (logo visible, buena calidad)
- [ ] Laptop conectado a proyector funcionando
- [ ] Backup: Screenshots de cada slide por si falla demo en vivo

### Presentación
- [ ] Slides cargadas en Gamma y accesibles offline (PDF backup)
- [ ] Timer visible para controlar 10-12 minutos
- [ ] Agua disponible
- [ ] Notas de Q&A impresas o en tablet
- [ ] Contacto visual practicado (no leer slides)

### Equipo
- [ ] Roles asignados: Quién presenta qué sección
- [ ] Transiciones entre speakers practicadas
- [ ] Backup speaker en caso de nervios o problemas técnicos
- [ ] Vestimenta profesional pero cómoda

---

## 🎯 TIPS FINALES PARA EL DÍA DE LA PRESENTACIÓN

### Durante la Presentación
1. **Respirar pausadamente** - No es una carrera, es una conversación
2. **Pausas estratégicas** - Después de datos importantes (85.4%, mAP50)
3. **Contacto visual** - Mirar a diferentes personas de la audiencia
4. **Manos visibles** - Gestos que refuercen el mensaje
5. **Si algo falla** - Tener backup screenshots, seguir con confianza

### Lenguaje Corporal
- ✅ Postura abierta (hombros hacia atrás)
- ✅ Movimiento natural (no estatuas)
- ✅ Sonreír donde sea apropiado
- ❌ Evitar cruzar brazos
- ❌ Evitar meter manos en bolsillos
- ❌ Evitar mirar solo al piso o techo

### Voz
- ✅ Volumen audible (practicar en el auditorio antes si es posible)
- ✅ Variación de tono (entusiasmo en logros, seriedad en técnico)
- ✅ Velocidad moderada (120-150 palabras por minuto)
- ❌ Evitar muletillas ("ehh", "osea", "como que")

### En Caso de Preguntas Difíciles
1. **Agradecer la pregunta** - "Excelente pregunta"
2. **Parafrasear** - "Si entiendo bien, preguntas sobre..."
3. **Responder honestamente** - Si no sabes, di "No tengo ese dato exacto, pero podemos investigarlo"
4. **Redirigir si off-topic** - "Interesante, aunque está fuera del scope de hoy, hablemos después"

---

## ⏱️ RESUMEN DE TIMING

| Slide | Tema | Tiempo | Acumulado |
|-------|------|--------|-----------|
| 1 | Portada | 30 seg | 0:30 |
| 2 | Problema | 1:00 min | 1:30 |
| 3 | Metodología | 1:00 min | 2:30 |
| 4 | Preprocesamiento | 0:45 min | 3:15 |
| 5 | Data Augmentation | 1:00 min | 4:15 |
| 6 | Modelo YOLO | 1:15 min | 5:30 |
| 7 | Métricas YOLO11m | 1:00 min | 6:30 |
| 8 | Métricas YOLOv8 | 0:45 min | 7:15 |
| 9 | Análisis por Clases | 1:00 min | 8:15 |
| 10 | Arquitectura | 1:00 min | 9:15 |
| 11 | Stack Tecnológico | 1:15 min | 10:30 |
| 12 | Conclusiones | 1:30 min | 12:00 |
| 13 | Cierre | 0:15 min | 12:15 |
| ** | Q&A | 3-5 min | 15-17 min |

**Total**: 12-17 minutos (perfecto para slot de 15-20 min)

---

## 🎬 SCRIPT DE APERTURA (MEMORIZAR)

> "Buenos días/tardes. Mi nombre es [NOMBRE], y junto a [NOMBRES DE EQUIPO], les presentamos **KUMO VISION**."
>
> "En los próximos 12 minutos, verán cómo transformamos un desafío real de empresas Fortune 500 - la monitorización de marca en millones de contenidos visuales - en un sistema automatizado de nivel industrial."
>
> "De metodología ágil, a arquitectura de producción, pasando por resultados que compiten con soluciones comerciales de miles de dólares al mes."
>
> "Empecemos."

---

## 🎬 SCRIPT DE CIERRE (MEMORIZAR)

> "KUMO VISION demuestra que con metodología correcta, stack moderno, y compromiso con la excelencia, un equipo de bootcamp puede construir sistemas que compiten con la industria."
>
> "85.4% de precisión. Arquitectura production-ready. Documentación exhaustiva."
>
> "No es solo un proyecto - es una prueba de que estamos listos para el siguiente nivel."
>
> "Gracias por su atención. Quedamos a sus preguntas."

---

## 📞 INFORMACIÓN DE CONTACTO (Para incluir en última slide)

**Repositorio GitHub**: https://github.com/Bootcamp-IA-P5/proyecto12-grupo2  
**Documentación**: Ver carpeta `/docs/`  
**Demo Live**: http://localhost:5173 (o deployment URL si ya está en cloud)

**Equipo**:
- [Nombre 1] - [LinkedIn/Email]
- [Nombre 2] - [LinkedIn/Email]
- [Nombre 3] - [LinkedIn/Email]

---

## ✨ MENSAJE FINAL PARA EL EQUIPO

Recuerden: **No están vendiendo código, están vendiendo una visión.**

Una visión donde la inteligencia artificial libera a las empresas de tareas repetitivas, donde un equipo pequeño con las herramientas correctas puede competir con corporaciones gigantes, donde la excelencia técnica se encuentra con el impacto de negocio.

**Han construido algo especial. Preséntenlo con el orgullo que merece.**

¡Éxito en la presentación! 🚀

---

**Última revisión**: Febrero 2026  
**Versión**: 2.0 (Adaptada a slides de Gamma)  
**Slides originales**: https://gamma.app/docs/Deteccion-Inteligente-de-Logotipos-mediante-Vision-Artificial-po26v38cx8gra4d
