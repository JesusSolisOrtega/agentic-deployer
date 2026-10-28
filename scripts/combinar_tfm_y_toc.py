"""
combinar_tfm_y_toc.py
=====================
Genera TFM_Completo.md (Markdown combinado listo para abrir en Typora y exportar a PDF).
Alineado con la estructura institucional de la ETSII / Universidad de Sevilla (Diverso Lab).

Uso:
    python scripts/combinar_tfm_y_toc.py
"""
import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = os.path.join(ROOT_DIR, "memoria")
OUTPUT_MD = os.path.join(ROOT_DIR, "TFM_Completo.md")

# ---------------------------------------------------------------------------
# Estructura documental de la memoria
# ---------------------------------------------------------------------------
preliminary_files = [
    "00_Portada.md",
    "00_Declaracion_Agradecimientos.md",
    "00_Resumen_Abstract.md",
]

# Lista de acrónimos se sitúa como elemento preliminar previo a Cap. 1
acronimos_file = "00_Acronimos.md"

# Capítulos del cuerpo, bibliografía y anexos
chapter_files = [
    "1_Introduccion.md",
    "2_Estado_del_Arte.md",
    "3_Metodologia_y_Stack.md",
    "4_Planificacion_y_Costes.md",
    "5_Diseno_del_Sistema.md",
    "6_Agente_y_MCP.md",
    "7_Interfaz_HITL.md",
    "8_QA_y_Testing.md",
    "9_Resultados.md",
    "10_Conclusiones_y_Futuro.md",
    "11_Bibliografia.md",
    "Anexo_A_YAML.md",
    "Anexo_B_Planificacion.md",
    "Anexo_C_Manual_Despliegue_y_Usuario.md",
]

# ---------------------------------------------------------------------------
# 1. Generar índice general (TOC) y capturar dinámicamente figuras/tablas
# ---------------------------------------------------------------------------
toc_lines = [
    "# Índice General\n\n",
    "- **Declaración de Autoría**\n",
    "- **Agradecimientos**\n",
    "- **Resumen y Abstract**\n",
    "- **Índice de Tablas**\n",
    "- **Índice de Figuras, Algoritmos y Listados**\n",
    "- **Lista de Acrónimos y Términos**\n",
]

figuras = []
tablas = []
algoritmos = []
listados = []

# Patrón para detectar los títulos de figuras, tablas, algoritmos y listados
caption_pattern = re.compile(r'<p align="center"><i><b>(Figura|Tabla|Algoritmo|Listado)\s+(\d+):</b>\s*(.*?)</i></p>')

# Escanear también 00_Acronimos.md para capturar las tablas de acrónimos si procede
scan_files = [acronimos_file] + chapter_files

for fname in scan_files:
    fpath = os.path.join(BASE_DIR, fname)
    is_anexo = fname.startswith("Anexo")
    is_acronimo = fname.startswith("00_Acronimos")
    
    if is_acronimo:
        ubicacion = "Preliminares"
    elif is_anexo:
        ubicacion = f"Anexo {fname.split('_')[1]}"
    else:
        num = fname.split('_')[0]
        ubicacion = f"Capítulo {num}"
    
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            in_code_block = False
            for line in f:
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    
                # TOC processing (solo capítulos y anexos)
                if not is_acronimo and not in_code_block and line.startswith("#"):
                    level = len(line) - len(line.lstrip("#"))
                    if level <= 2:
                        title = line.strip("# \n")
                        if level == 1:
                            toc_lines.append(f"- **{title}**\n")
                        elif level == 2:
                            toc_lines.append(f"  - {title}\n")
                
                # Figuras / Tablas / Algoritmos / Listados
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
                        elif tipo == "Listado":
                            listados.append(item)

# Ordenar por número
figuras.sort(key=lambda x: x[0])
tablas.sort(key=lambda x: x[0])
algoritmos.sort(key=lambda x: x[0])
listados.sort(key=lambda x: x[0])

# ---------------------------------------------------------------------------
# 2. Generar o preservar 0_Indices.md
# ---------------------------------------------------------------------------
indices_path = os.path.join(BASE_DIR, "0_Indices.md")

# Si 0_Indices.md ya tiene números de página mapeados, preservarlos a menos que no exista
indices_exist_with_pages = False
if os.path.exists(indices_path):
    with open(indices_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "....." in content or "...." in content or "toc-dots" in content or "toc-row" in content:
            indices_exist_with_pages = True

if not indices_exist_with_pages:
    with open(indices_path, "w", encoding="utf-8") as f:
        # 2.1. Índice General
        f.write("".join(toc_lines))
        f.write("\n\n<div style='page-break-after: always;'></div>\n\n")
        
        # 2.2. Índice de Tablas (sección independiente)
        f.write("# Índice de Tablas\n\n")
        for _, linea in tablas:
            f.write(linea)
        f.write("\n\n<div style='page-break-after: always;'></div>\n\n")
        
        # 2.3. Índice de Figuras, Algoritmos y Listados (sección independiente)
        f.write("# Índice de Figuras, Algoritmos y Listados\n\n")
        f.write("### Figuras\n\n")
        for _, linea in figuras:
            f.write(linea)
        f.write("\n")
        
        f.write("### Algoritmos (Pseudocódigo)\n\n")
        for _, linea in algoritmos:
            f.write(linea)
        f.write("\n")

        f.write("### Listados de Código / Manifiestos\n\n")
        for _, linea in listados:
            f.write(linea)
        f.write("\n")
else:
    print("ℹ Preservando números de página existentes en '0_Indices.md'.")

# ---------------------------------------------------------------------------
# 3. Combinar todos los ficheros en TFM_Completo.md
# ---------------------------------------------------------------------------
all_files = preliminary_files + ["0_Indices.md", acronimos_file] + chapter_files
parts = []

for fname in all_files:
    fpath = os.path.join(BASE_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            parts.append(f.read())
    else:
        print(f"[!] Advertencia: archivo no encontrado: {fpath}")

combined = "\n\n<div style='page-break-after: always;'></div>\n\n".join(parts)

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(combined)

print(f"✓ Estructura de preliminares e índices generada con éxito.")
print(f"✓ Fichero combinado actualizado: {OUTPUT_MD}")
print(f"  → Listo para abrir en Typora · File > Export > PDF")
