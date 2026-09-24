import os

files = [
    "1_Introduccion.md",
    "2_Estado_del_Arte.md",
    "3_Metodologia_y_Stack.md",
    "4_Diseno_del_Sistema.md",
    "5_Agente_y_MCP.md",
    "6_Interfaz_HITL.md",
    "7_QA_y_Testing.md",
    "8_Resultados.md",
    "9_Conclusiones_y_Futuro.md",
    "10_Bibliografia.md"
]

base_dir = "/home/jesus/projects/TFM/memoria"
toc_lines = ["# Índice de Contenidos\n\n"]

for fname in files:
    fpath = os.path.join(base_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("#"):
                    # Solo H1 y H2
                    level = len(line) - len(line.lstrip("#"))
                    if level > 2:
                        continue
                    
                    title = line.strip("# \n")
                    if level == 1:
                        toc_lines.append(f"- **{title}**\n")
                    elif level == 2:
                        toc_lines.append(f"  - {title}\n")

toc_text = "".join(toc_lines)

indices_path = os.path.join(base_dir, "0_Indices.md")
with open(indices_path, 'w', encoding='utf-8') as f:
    f.write(toc_text)
    f.write("\n\n<div style='page-break-after: always;'></div>\n\n")
    f.write("""# Índice de Figuras y Algoritmos

El presente Trabajo de Fin de Máster hace uso intensivo de modelado visual y pseudocódigo para formalizar las decisiones arquitectónicas. A continuación se listan las figuras y algoritmos referenciados a lo largo de la memoria:

### Índice de Figuras

- **Figura 1:** Diagrama de componentes del *Stack* Tecnológico empleado. *(Sección 3.2)*
- **Figura 2:** Diagrama de Contenedores (Nivel 2) del Modelo C4 para el sistema Agentic Deployer. *(Sección 4.1)*
- **Figura 3:** Diagrama de Secuencia End-to-End modelando las tres fases de aislamiento temporal. *(Sección 4.5)*
- **Figura 4:** Diagrama de flujo del bucle cognitivo ReAct (Reasoning and Acting). *(Sección 5.3)*
- **Figura 5:** Grafo Dirigido Acíclico (DAG) que rige la Máquina de Estados Finita (FSM) del sistema. *(Sección 6.2)*

### Índice de Algoritmos (Pseudocódigo)

- **Algoritmo 1:** Validación Estricta de Entidades de Dominio Hexagonal. *(Sección 4.3.1)*
- **Algoritmo 2:** Introspección Dinámica de Contratos de Herramientas. *(Sección 5.1.1)*
- **Algoritmo 3:** Bucle de Orquestación Cognitiva (ReAct Loop). *(Sección 5.3.1)*
- **Algoritmo 4:** Transición Inmutable de la Máquina de Estados (FSM_Transition). *(Sección 6.2.2)*
- **Algoritmo 5:** Property-Based Test para Invariantes Hexagonales (Fuzzing). *(Sección 7.2.1)*
""")

all_files = ["0_Indices.md"] + files
output_file = "/home/jesus/projects/TFM/TFM_Completo.md"

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write("<style>\n.mermaid svg { max-width: 100%; margin: 0 auto; display: block; height: auto; }\n</style>\n\n")
    outfile.write("# Memoria del Trabajo de Fin de Máster\n\n<div style='page-break-after: always;'></div>\n\n")
    for fname in all_files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write("\n\n<div style='page-break-after: always;'></div>\n\n")

print(f"Generado exitosamente: {output_file}")
