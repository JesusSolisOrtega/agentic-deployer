# Capítulo 9. Gestión y Viabilidad del Proyecto

> Este capítulo condensa el análisis ejecutivo de la viabilidad técnica y económica del *Agentic Deployer*, así como las métricas globales de esfuerzo. El desglose exhaustivo de los *sprints*, retrospectivas ágiles, y cálculo de costes pormenorizado se encuentra documentado en el **Anexo B (Planificación Detallada del Proyecto y Costes)**.

---

## 9.1. Esfuerzo de Desarrollo y Desviaciones

El proyecto se estructuró bajo una metodología ágil iterativa-incremental orientada al dominio (*Domain-First*), distribuyendo el esfuerzo en 5 *Sprints* técnicos y 2 fases de redacción y cierre de excelencia. 

Frente a la estimación inicial de ~300 horas, el cierre empírico del proyecto arrojó un esfuerzo total de **~340 horas**, lo que representa una desviación del **+13%**. Esta inversión adicional se encuadra holgadamente dentro del margen de contingencia previsto (±15%) y se asumió de manera deliberada en la recta final para elevar el MVP a un estándar de excelencia ingenieril (implementación de persistencia ACID en SQLite, ampliación de 4 a 7 herramientas MCP, y consecución del 100% de letalidad en *Mutation Testing*).

La adopción de asistentes de Inteligencia Artificial (Google Gemini Advanced) demostró actuar como un multiplicador de productividad esencial. Permitió absorber esta densidad arquitectónica dentro de un cronograma manejable para un único ingeniero, validando de forma recursiva la hipótesis de investigación del TFM sobre la utilidad de los agentes LLM en ciclos de vida de software.

## 9.2. Análisis Económico del Desarrollo

El proyecto fue desarrollado utilizando recursos de código abierto e infraestructura personal, por lo que el coste material directo fue marginal. No obstante, al calcular el **coste de oportunidad equivalente** (la inversión que requeriría el proyecto si se externalizara en el mercado tecnológico español a tarifas de 2026), los resultados son los siguientes:

*   **Coste de Recursos Humanos (Investigador + Tutoría):** ~9.280 €
*   **Coste de Infraestructura (Amortización hardware + Licencias IA):** ~261 €
*   **Coste Total del Proyecto:** **~9.541 €**
*   **Coste Promedio por Hora Efectiva:** ~26,2 €/h

## 9.3. Coste de Adopción Corporativa y ROI

La viabilidad comercial del prototipo se evaluó proyectando su implantación en diferentes tamaños de Servicios de Informática y Comunicaciones (SIC). Para una universidad u organización mediana (5.000 – 30.000 usuarios con una carga promedio de 500 solicitudes de infraestructura al año):

1.  **Modelo de Coste Cero Operativo (Ollama):** Aprovechando la modularidad de la Arquitectura Hexagonal, la organización puede prescindir de APIs de pago y enrutar la lógica cognitiva a través de un servidor *on-premise* con LLMs *open-source* (ej. `Llama-3.1` o `Qwen-2.5`). Esto reduce el coste operativo de la IA a **0 €/año**, al tiempo que blinda al 100% la privacidad del dato institucional (*Zero Data Retention*).
2.  **Rentabilidad (ROI):** 
    *   La inversión inicial (*CAPEX*) de adaptación e integración con el clúster físico se estima en ~8.100 €.
    *   El ahorro operativo anual (reducción del tiempo de negociación, modelado YAML y auditoría manual de políticas de 24h a 2 minutos por solicitud) se cifra en ~20.320 €/año.
    *   El **período de recuperación de la inversión (Payback Period)** se alcanza a los **5,4 meses**.
    *   El **Retorno de la Inversión (ROI) acumulado a 3 años** supera el **460%**.

*Para acceder al desglose de los diagramas de Gantt, las tablas forenses por Sprint y los cálculos de OPEX/CAPEX detallados, véase el **Anexo B**.*
