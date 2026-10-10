"""
combinar_tfm_y_toc.py
=====================
Genera TFM_Completo.md (Markdown combinado listo para abrir en Typora y exportar a PDF).

Uso:
    python combinar_tfm_y_toc.py
"""
import os
import re

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
# 1. Generar índice de contenidos (TOC) y capturar dinámicamente figuras/tablas
# ---------------------------------------------------------------------------
toc_source_files = [f for f in files if f != "00_Resumen_Abstract.md"]

toc_lines = ["# Índice de Contenidos\n\n"]
figuras = []
tablas = []
algoritmos = []

# Patrón para detectar los títulos de figuras, tablas y algoritmos
# Ejemplo: <p align="center"><i><b>Tabla 1:</b> Descripción.</i></p>
caption_pattern = re.compile(r'<p align="center"><i><b>(Figura|Tabla|Algoritmo)\s+(\d+):</b>\s+(.*?)</i></p>')

for fname in toc_source_files:
    fpath = os.path.join(BASE_DIR, fname)
    is_anexo = fname.startswith("Anexo")
    if is_anexo:
        ubicacion = f"Anexo {fname.split('_')[1]}"
    else:
        num = fname.split('_')[0]
        ubicacion = f"Capítulo {num}"
    
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            in_code_block = False
            for line in f:
                # TOC processing
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                if not in_code_block and line.startswith("#"):
                    level = len(line) - len(line.lstrip("#"))
                    if level <= 2:
                        title = line.strip("# \n")
                        if level == 1:
                            toc_lines.append(f"- **{title}**\n")
                        elif level == 2:
                            toc_lines.append(f"  - {title}\n")
                
                # Figures/Tables/Algorithms processing
                if not in_code_block:
                    match = caption_pattern.search(line)
                    if match:
                        tipo = match.group(1)
                        numero = int(match.group(2))
                        desc = match.group(3).strip()
                        item = (numero, f"- **{tipo} {numero}:** {desc} *({ubicacion})*\n")
                        
                        if tipo == "Figura":
                            figuras.append(item)
                        elif tipo == "Tabla":
                            tablas.append(item)
                        elif tipo == "Algoritmo":
                            algoritmos.append(item)

# Ordenar por número
figuras.sort(key=lambda x: x[0])
tablas.sort(key=lambda x: x[0])
algoritmos.sort(key=lambda x: x[0])

indices_path = os.path.join(BASE_DIR, "0_Indices.md")
with open(indices_path, "w", encoding="utf-8") as f:
    # Escribir TOC
    f.write("".join(toc_lines))
    f.write("\n\n<div style='page-break-after: always;'></div>\n\n")
    
    # Escribir Índices Visuales
    f.write("# Índice de Figuras y Algoritmos\n\n")
    f.write("El presente Trabajo de Fin de Máster hace uso intensivo de modelado visual y pseudocódigo para formalizar las decisiones arquitectónicas. A continuación se listan las figuras y algoritmos referenciados a lo largo de la memoria:\n\n")
    
    f.write("### Índice de Figuras\n\n")
    for _, linea in figuras:
        f.write(linea)
    f.write("\n")
    
    f.write("### Índice de Tablas\n\n")
    for _, linea in tablas:
        f.write(linea)
    f.write("\n")
        
    f.write("### Índice de Algoritmos (Pseudocódigo)\n\n")
    for _, linea in algoritmos:
        f.write(linea)
    f.write("\n")

# ---------------------------------------------------------------------------
# 2. Combinar todos los Markdown en TFM_Completo.md
# ---------------------------------------------------------------------------
all_files = ["00_Resumen_Abstract.md", "0_Indices.md"] + toc_source_files
parts = []

for fname in all_files:
    fpath = os.path.join(BASE_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            parts.append(f.read())

combined = "\n\n<div style='page-break-after: always;'></div>\n\n".join(parts)

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(combined)

print(f"✓ Markdown generado dinámicamente: {OUTPUT_MD}")
print(f"  → Ábrelo en Typora · File > Export > PDF")
print(f"  → Pie de página: File > Page Setup > Footer > escribe: ${{pageNo}} / ${{pageCount}}")
