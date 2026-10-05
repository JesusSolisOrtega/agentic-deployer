"""
combinar_tfm_y_toc.py
=====================
Genera TFM_Completo.md (Markdown combinado listo para abrir en Typora y exportar a PDF).

Uso:
    python combinar_tfm_y_toc.py
"""
import os

# ---------------------------------------------------------------------------
# Archivos que componen la memoria (en orden)
# ---------------------------------------------------------------------------
files = [
    "00_Resumen_Abstract.md",
    "1_Introduccion.md",
    "2_Estado_del_Arte.md",
    "3_Metodologia_y_Stack.md",
    "4_Diseno_del_Sistema.md",
    "5_Agente_y_MCP.md",
    "6_Interfaz_HITL.md",
    "7_QA_y_Testing.md",
    "8_Resultados.md",
    "9_Planificacion_y_Costes.md",
    "10_Conclusiones_y_Futuro.md",
    "11_Bibliografia.md",
    "Anexo_A_YAML.md",
    "Anexo_B_Planificacion.md",
    "Anexo_C_Glosario.md",
]

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = os.path.join(ROOT_DIR, "memoria")
OUTPUT_MD = os.path.join(ROOT_DIR, "TFM_Completo.md")

# ---------------------------------------------------------------------------
# 1. Generar índice de contenidos (TOC)
#    Se construye automáticamente a partir de los encabezados H1 y H2
#    de los capítulos (excluyendo el Resumen/Abstract que va antes del TOC).
# ---------------------------------------------------------------------------
# Solo usamos los capítulos 1-11 + Anexos para el TOC (no el Resumen)
toc_source_files = [f for f in files if f != "00_Resumen_Abstract.md"]

toc_lines = ["# Índice de Contenidos\n\n"]

for fname in toc_source_files:
    fpath = os.path.join(BASE_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            in_code_block = False
            for line in f:
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                if not in_code_block and line.startswith("#"):
                    level = len(line) - len(line.lstrip("#"))
                    if level > 2:
                        continue
                    title = line.strip("# \n")
                    if level == 1:
                        toc_lines.append(f"- **{title}**\n")
                    elif level == 2:
                        toc_lines.append(f"  - {title}\n")

indices_path = os.path.join(BASE_DIR, "0_Indices.md")
with open(indices_path, "w", encoding="utf-8") as f:
    f.write("".join(toc_lines))
    f.write("\n\n<div style='page-break-after: always;'></div>\n\n")
    f.write(
        """# Índice de Figuras y Algoritmos

El presente Trabajo de Fin de Máster hace uso intensivo de modelado visual y pseudocódigo para formalizar las decisiones arquitectónicas. A continuación se listan las figuras y algoritmos referenciados a lo largo de la memoria:

### Índice de Figuras

- **Figura 1:** Contraste arquitectónico entre el problema de integración N×M (acoplamiento propietario) y la topología de Bus Universal propuesta por el protocolo MCP. *(Capítulo 2)*
- **Figura 2:** Diagrama de componentes del Stack Tecnológico empleado, evidenciando la segregación entre las capas de interfaz, razonamiento cognitivo, backend restrictivo y las herramientas de validación de calidad continua. *(Capítulo 3)*
- **Figura 3:** Diagrama de Contenedores (Nivel 2) del Modelo C4 para el sistema Agentic Deployer. *(Capítulo 4)*
- **Figura 4:** Diagrama de despliegue a nivel de proceso. Los cuatro componentes coexisten en la misma máquina; el servidor MCP se comunica por `stdio` sin exponer ningún puerto TCP. *(Capítulo 4)*
- **Figura 5:** Diagrama de Clases (UML) resumiendo las principales entidades y contratos del núcleo lógico, destacando el uso del polimorfismo para la inyección de dependencias. *(Capítulo 4)*
- **Figura 6:** Topología de la Arquitectura Hexagonal. El flujo de control penetra desde los Adaptadores Primarios, pero la dependencia de código siempre fluye hacia el centro (Regla de Dependencia de Inversión). *(Capítulo 4)*
- **Figura 7:** Árbol de decisión del `SecurityContextValidator`. Cada rama de rechazo lanza un `SecurityViolationError` que el bucle ReAct captura como Observación para auto-corregirse. *(Capítulo 4)*
- **Figura 8:** Diagrama de Secuencia E2E (Fase 1). Negociación cognitiva entre el Investigador y el LLM hasta alcanzar una intención. *(Capítulo 4)*
- **Figura 9:** Diagrama de Secuencia E2E (Fase 2). El Backend procesa la petición, aplicando reglas de negocio estrictas. *(Capítulo 4)*
- **Figura 10:** Diagrama de Secuencia E2E (Fase 3). Decisión asíncrona del técnico humano, separando la inferencia de la ejecución. *(Capítulo 4)*
- **Figura 11:** Ciclo de vida completo de un mensaje MCP. El protocolo JSON-RPC define tres fases: inicialización, ejecución y observación. *(Capítulo 5)*
- **Figura 12:** Diagrama de flujo del bucle cognitivo ReAct (Reasoning and Acting). *(Capítulo 5)*
- **Figura 13:** Grafo Dirigido Acíclico (DAG) que rige la Máquina de Estados Finita (FSM) del sistema. *(Capítulo 6)*
- **Figura 14:** Diagrama de Secuencia del flujo HITL: polling del Dashboard, vector de aprobación (PENDING → APPROVED → DEPLOYED) y vector de rechazo (PENDING → REJECTED). *(Capítulo 6)*
- **Figura 15:** Arquitectura de la Pirámide Híbrida de Testing implementada en el Agentic Deployer, adaptando el modelo clásico a las exigencias de la Inteligencia Artificial Generativa. *(Capítulo 7)*
- **Figura 16:** Diagrama de Gantt (Parte 1). Planificación orientativa de los Sprints 1 a 4 (núcleo y agente). *(Capítulo 9)*
- **Figura 17:** Diagrama de Gantt (Parte 2). Planificación orientativa del QA avanzado y las fases de cierre/consolidación. *(Capítulo 9)*

### Índice de Tablas

- **Tabla 1:** Comparativa de herramientas declarativas vs imperativas. *(Capítulo)*
- **Tabla 2:** Posicionamiento del sistema respecto al estado del arte. *(Capítulo)*
- **Tabla 3:** Vectores de mutación REST del Dashboard de Operaciones. *(Capítulo)*
- **Tabla 4:** Cobertura de pruebas unitarias por componente. *(Capítulo)*
- **Tabla 5:** Resultados del Mutation Testing por módulo. *(Capítulo)*
- **Tabla 6:** Resultados de las Pruebas Metamórficas por Relación. *(Capítulo)*
- **Tabla 7:** Métricas globales de la batería metamórfica. *(Capítulo)*
- **Tabla 8:** Impacto temporal operativo (ITSM tradicional vs Agentic Deployer). *(Capítulo)*
- **Tabla 9:** Traza de ejecución: Análisis de contexto y herramienta (Paso 1). *(Capítulo)*
- **Tabla 10:** Traza de ejecución: Validación en el núcleo hexagonal (Paso 5). *(Capítulo)*
- **Tabla 11:** Métricas de rendimiento del walkthrough completo (Escenario 1). *(Capítulo)*
- **Tabla 12:** Traza de ejecución: Intento de Prompt Injection (Escenario 2). *(Capítulo)*
- **Tabla 13:** Desglose de latencias por componente en el ciclo de vida. *(Capítulo)*
- **Tabla 14:** Comparativa E2E de métricas operativas (multi-escenario). *(Capítulo)*
- **Tabla 15:** Rendimiento comparativo real de modelos alternativos. *(Capítulo)*
- **Tabla 16:** Resultados de los Experimentos de Arquitectura Cognitiva. *(Capítulo)*
- **Tabla 17:** Módulos de desarrollo y jerarquía de prioridades. *(Capítulo)*
- **Tabla 18:** Estimación de esfuerzo neto por Sprint. *(Capítulo)*
- **Tabla 19:** Resumen de desviaciones de tiempo por fase. *(Capítulo)*
- **Tabla 20:** Costes de Recursos Humanos (CAPEX equivalente). *(Capítulo)*
- **Tabla 21:** Costes de Infraestructura y Herramientas (Fase de Desarrollo). *(Capítulo)*
- **Tabla 22:** Subtotal y costes totales de la fase de desarrollo. *(Capítulo)*
- **Tabla 23:** Perfiles de Organización Adoptante (Casos A, B y C). *(Capítulo)*
- **Tabla 24:** Costes de Implantación (CAPEX - Inversión Inicial). *(Capítulo)*
- **Tabla 25:** Costes Operativos Anuales de Infraestructura (OPEX). *(Capítulo)*
- **Tabla 26:** Costes Operativos Anuales de Motor LLM (Local vs Cloud). *(Capítulo)*
- **Tabla 27:** OPEX Total Anual consolidado por Perfil de Adopción. *(Capítulo)*
- **Tabla 28:** Cálculo del ahorro anual operativo (Escenario de Perfil B). *(Capítulo)*
- **Tabla 29:** Retorno de Inversión (ROI) a 3 años (Perfil B con Ollama). *(Capítulo)*
- **Tabla 30:** Contexto de Generación del Manifiesto YAML (Escenario 1). *(Anexo)*
- **Tabla 31:** Retrospectiva del Sprint 1 (Núcleo Hexagonal). *(Anexo)*
- **Tabla 32:** Retrospectiva del Sprint 2 (Backend HITL y FSM). *(Anexo)*
- **Tabla 33:** Retrospectiva del Sprint 3 (Golden Paths y FakeK8s). *(Anexo)*
- **Tabla 34:** Retrospectiva del Sprint 4 (Agente ReAct y MCP SDK). *(Anexo)*
- **Tabla 35:** Retrospectiva del Sprint 5 (QA Avanzado). *(Anexo)*
- **Tabla 36:** Retrospectiva de la Fase 6 (Redacción y Cierre). *(Anexo)*
- **Tabla 37:** Retrospectiva de la Fase 7 (Consolidación de Excelencia Técnica). *(Anexo)*
- **Tabla 38:** Glosario completo de Acrónimos y Términos Técnicos. *(Anexo)*

### Índice de Algoritmos (Pseudocódigo)

- **Algoritmo 1:** Validación Estricta de Entidades de Dominio Hexagonal. *(Sección 4.3.1)*
- **Algoritmo 2:** Introspección Dinámica de Contratos de Herramientas. *(Sección 5.1.1)*
- **Algoritmo 3:** Bucle de Orquestación Cognitiva (ReAct Loop). *(Sección 5.3.1)*
- **Algoritmo 4:** Transición Inmutable de la Máquina de Estados (FSM_Transition). *(Sección 6.2.2)*
- **Algoritmo 5:** Property-Based Test para Invariantes Hexagonales (Fuzzing). *(Sección 7.2.1)*
"""
    )

# ---------------------------------------------------------------------------
# 2. Combinar todos los Markdown en TFM_Completo.md
#    Orden: Resumen → TOC + Índice de Figuras → Capítulos 1-11 → Anexos
# ---------------------------------------------------------------------------
all_files = ["00_Resumen_Abstract.md", "0_Indices.md"] + [
    f for f in files if f != "00_Resumen_Abstract.md"
]
parts = []

for fname in all_files:
    fpath = os.path.join(BASE_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            parts.append(f.read())

combined = "\n\n<div style='page-break-after: always;'></div>\n\n".join(parts)

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(combined)

print(f"✓ Markdown generado: {OUTPUT_MD}")
print(f"  → Ábrelo en Typora · File > Export > PDF")
print(f"  → Pie de página: File > Page Setup > Footer > escribe: ${{pageNo}} / ${{pageCount}}")
