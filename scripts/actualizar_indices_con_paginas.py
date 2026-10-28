#!/usr/bin/env python3
"""
actualizar_indices_con_paginas.py
=================================
Extrae automáticamente los números de página físicos del PDF generado del TFM
(mediante 'pdftotext -layout') y actualiza 'memoria/0_Indices.md' y 'TFM_Completo.md'
incorporando los números de página en:
  1. Índice General (Preliminares, Capítulos 1..10, Bibliografía, Anexos A..C)
  2. Índice de Tablas
  3. Índice de Figuras, Algoritmos y Listados

Uso:
    python scripts/actualizar_indices_con_paginas.py
    python scripts/actualizar_indices_con_paginas.py --pdf TFM_Completo.pdf
    python scripts/actualizar_indices_con_paginas.py --dry-run
"""

import os
import sys
import re
import argparse
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MEMORIA_DIR = os.path.join(ROOT_DIR, "memoria")
INDICES_MD = os.path.join(MEMORIA_DIR, "0_Indices.md")
TFM_COMPLETO_MD = os.path.join(ROOT_DIR, "TFM_Completo.md")

PRELIMINARY_FILES = [
    "00_Portada.md",
    "00_Declaracion_Agradecimientos.md",
    "00_Resumen_Abstract.md",
]

ACRONIMOS_FILE = "00_Acronimos.md"

CHAPTER_FILES = [
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


def resolve_default_pdf() -> str:
    """Selecciona el PDF más reciente entre TFM_Completo.pdf y TFM_JesusSolisOrtega.pdf."""
    c1 = os.path.join(ROOT_DIR, "TFM_Completo.pdf")
    c2 = os.path.join(ROOT_DIR, "TFM_JesusSolisOrtega.pdf")
    if os.path.exists(c1) and os.path.exists(c2):
        return c1 if os.path.getmtime(c1) >= os.path.getmtime(c2) else c2
    elif os.path.exists(c1):
        return c1
    return c2


def extract_pages_from_pdf(pdf_path: str):
    """Extrae el texto página por página usando pdftotext -layout."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No se encontró el fichero PDF: {pdf_path}")

    cmd = ["pdftotext", "-layout", pdf_path, "-"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    raw_pages = res.stdout.decode("utf-8", errors="ignore").split("\x0c")
    # Limpiar espacios horizontales duplicados pero manteniendo layout
    pages = [re.sub(r"[ \t]+", " ", p) for p in raw_pages]
    return pages


def detect_content_start_page(pages):
    """
    Detecta en qué página física empieza el cuerpo del Capítulo 1 (tras los índices y preliminares).
    Busca la página que contenga 'Capítulo 1' junto con '1.1.' y texto del cuerpo,
    descartando las páginas que sean de los índices preliminares.
    """
    for i, p in enumerate(pages):
        p_lower = p.lower()
        if "capítulo 1" in p_lower and "1.1." in p and "contexto y motivación" in p_lower:
            # Descartar si es una línea del índice
            if "índice" not in p_lower and "acrónimo" not in p_lower:
                return i + 1
    # Fallback si no coincide exactamente
    for i, p in enumerate(pages):
        if i >= 10 and "capítulo 1" in p.lower():
            return i + 1
    return 15


def match_preliminaries(pages, start_page):
    """
    Localiza las páginas físicas de las secciones preliminares (anteriores al Capítulo 1).
    Cada sección preliminar empieza con su título en la cabecera (primera línea significativa).
    """
    prelim_targets = {
        "Declaración de Autoría": "declaración de autoría",
        "Agradecimientos": "agradecimientos",
        "Resumen y Abstract": "resumen",
        "Índice General": "índice general",
        "Índice de Tablas": "índice de tablas",
        "Índice de Figuras, Algoritmos y Listados": "índice de figuras",
        "Lista de Acrónimos y Términos": "lista de acrónimos",
    }

    results = {}
    for name, target in prelim_targets.items():
        found = None
        for p_num in range(1, min(start_page, len(pages) + 1)):
            lines = [l.strip().lower() for l in pages[p_num - 1].split("\n") if l.strip()]
            if lines and target in lines[0]:
                found = p_num
                break
        results[name] = found
    return results


def extract_toc_items():
    """Extrae títulos H1 y H2 de los capítulos, bibliografía y anexos."""
    items = []
    for fname in CHAPTER_FILES:
        fpath = os.path.join(MEMORIA_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            in_code = False
            for line in f:
                if line.strip().startswith("```"):
                    in_code = not in_code
                if not in_code and line.startswith("#"):
                    level = len(line) - len(line.lstrip("#"))
                    if level <= 2:
                        title = line.strip("# \n")
                        items.append((level, title, fname))
    return items


def extract_visual_items():
    """Extrae figuras, tablas, algoritmos y listados con su ubicación y descripción."""
    caption_pattern = re.compile(
        r'<p align="center"><i><b>(Figura|Tabla|Algoritmo|Listado)\s+(\d+):</b>\s*(.*?)</i></p>'
    )
    figuras = []
    tablas = []
    algoritmos = []
    listados = []

    for fname in CHAPTER_FILES:
        fpath = os.path.join(MEMORIA_DIR, fname)
        is_anexo = fname.startswith("Anexo")
        if is_anexo:
            ubicacion = f"Anexo {fname.split('_')[1]}"
        else:
            num = fname.split("_")[0]
            ubicacion = f"Capítulo {num}"

        if not os.path.exists(fpath):
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            in_code = False
            for line in f:
                if line.strip().startswith("```"):
                    in_code = not in_code
                if not in_code:
                    m = caption_pattern.search(line)
                    if m:
                        tipo = m.group(1)
                        numero = int(m.group(2))
                        desc = m.group(3).strip()
                        entry = (numero, tipo, desc, ubicacion)
                        if tipo == "Figura":
                            figuras.append(entry)
                        elif tipo == "Tabla":
                            tablas.append(entry)
                        elif tipo == "Algoritmo":
                            algoritmos.append(entry)
                        elif tipo == "Listado":
                            listados.append(entry)

    figuras.sort(key=lambda x: x[0])
    tablas.sort(key=lambda x: x[0])
    algoritmos.sort(key=lambda x: x[0])
    listados.sort(key=lambda x: x[0])
    return figuras, tablas, algoritmos, listados


def match_toc_pages(toc_items, pages, start_page):
    """Empareja cada sección del TOC con su número de página real en el PDF."""
    results = []
    last_page = start_page

    for level, title, fname in toc_items:
        clean_title = re.sub(r"[*_`]", "", title).strip()
        words = clean_title.split()
        search_terms = []
        if len(words) >= 4:
            search_terms.append(" ".join(words[:4]).lower())
        if len(words) >= 3:
            search_terms.append(" ".join(words[:3]).lower())
        if len(words) >= 2:
            search_terms.append(" ".join(words[:2]).lower())
        search_terms.append(words[0].lower())

        found_page = None
        # Búsqueda secuencial hacia adelante desde la última página detectada
        for term in search_terms:
            for p_num in range(last_page, len(pages) + 1):
                page_text = pages[p_num - 1].lower()
                if term in page_text:
                    found_page = p_num
                    break
            if found_page:
                break

        # Fallback: búsqueda global en el cuerpo
        if not found_page:
            for term in search_terms:
                for p_num in range(start_page, len(pages) + 1):
                    page_text = pages[p_num - 1].lower()
                    if term in page_text:
                        found_page = p_num
                        break
                if found_page:
                    break

        if found_page:
            last_page = found_page
            results.append((level, title, found_page))
        else:
            results.append((level, title, None))

    return results


def match_visual_pages(items, pages, start_page):
    """Empareja cada figura/tabla/algoritmo/listado con su página real (solo en el cuerpo)."""
    results = []
    for numero, tipo, desc, ubicacion in items:
        target = f"{tipo} {numero}:".lower()
        found_page = None
        # Buscar estrictamente a partir de start_page para no emparejar con el propio índice preliminar
        for p_num in range(start_page, len(pages) + 1):
            if target in pages[p_num - 1].lower():
                found_page = p_num
                break

        # Fallback de conveniencia para Listados
        if not found_page and tipo == "Listado":
            if numero == 1:
                for p_num in range(start_page, len(pages) + 1):
                    p_text = pages[p_num - 1].lower()
                    if "2.3." in pages[p_num - 1] and "declarativa" in p_text:
                        found_page = p_num
                        break
            elif numero == 2:
                for p_num in range(start_page, len(pages) + 1):
                    p_text = pages[p_num - 1].lower()
                    if "a.2." in p_text and "manifiesto" in p_text:
                        found_page = p_num
                        break

        results.append((numero, tipo, desc, ubicacion, found_page))
    return results


def format_academic_toc_row(title: str, page: int | None, level: int = 1) -> str:
    """Formatea una fila del índice con flexbox y puntos guía dinámicos alineados al margen derecho."""
    page_str = str(page) if page is not None else "?"
    is_bold = (level == 1)
    pad_left = "22px" if level == 2 else "0"
    font_weight = "bold" if is_bold else "normal"
    margin_top = "9px" if is_bold else "0"
    page_weight = "bold" if is_bold else "normal"
    clean_title = re.sub(r"[*_`]", "", title).strip()

    return (
        f'<div class="toc-row level-{level}" style="display: flex; align-items: baseline; justify-content: space-between; '
        f'margin-bottom: 4px; margin-top: {margin_top}; padding-left: {pad_left}; font-weight: {font_weight}; line-height: 1.45;">'
        f'<span class="toc-title" style="flex-shrink: 1;">{clean_title}</span>'
        f'<span class="toc-dots" style="flex-grow: 1; border-bottom: 1.5px dotted #666; margin: 0 8px 3px 8px; min-width: 15px;"></span>'
        f'<span class="toc-page" style="flex-shrink: 0; text-align: right; min-width: 25px; font-variant-numeric: tabular-nums; font-weight: {page_weight};">{page_str}</span>'
        f'</div>\n'
    )


def format_academic_visual_row(tipo: str, numero: int, desc: str, ubicacion: str, page: int | None) -> str:
    """Formatea una fila de elemento visual (figura/tabla) alineada al margen derecho."""
    page_str = str(page) if page is not None else "?"
    title_html = f"<strong>{tipo} {numero}:</strong> {desc} <em>({ubicacion})</em>"
    return (
        f'<div class="toc-row visual-row" style="display: flex; align-items: baseline; justify-content: space-between; '
        f'margin-bottom: 5px; margin-top: 4px; font-size: 10.5pt; line-height: 1.45;">'
        f'<span class="toc-title" style="flex-shrink: 1;">{title_html}</span>'
        f'<span class="toc-dots" style="flex-grow: 1; border-bottom: 1.5px dotted #666; margin: 0 8px 3px 8px; min-width: 15px;"></span>'
        f'<span class="toc-page" style="flex-shrink: 0; text-align: right; min-width: 25px; font-variant-numeric: tabular-nums; font-weight: normal;">{page_str}</span>'
        f'</div>\n'
    )


def format_toc_line(title: str, page: int | None, is_bold: bool = False, indent: int = 0) -> str:
    """Formatea una línea de índice con puntos guía de texto plano."""
    page_str = str(page) if page is not None else "?"
    prefix = "  " * indent + "- "
    bullet = f"**{title}**" if is_bold else title
    
    visual_len = len(prefix) + len(bullet)
    dots_count = max(4, 76 - visual_len - len(page_str) - 2)
    dots = "." * dots_count
    return f"{prefix}{bullet} {dots} {page_str}\n"


def format_visual_line(tipo: str, numero: int, desc: str, ubicacion: str, page: int | None) -> str:
    """Formatea una línea visual con puntos guía de texto plano."""
    page_str = str(page) if page is not None else "?"
    item_header = f"- **{tipo} {numero}:** {desc} *({ubicacion})*"
    dots_count = max(4, 80 - len(item_header) - len(page_str) - 2)
    dots = "." * dots_count
    return f"{item_header} {dots} {page_str}\n"


def generate_indices_md(prelim_pages, toc_results, fig_results, tab_results, alg_results, list_results, style: str = "academic") -> str:
    """
    Construye el contenido completo y definitivo de memoria/0_Indices.md
    siguiendo la estructura oficial:
      1. Índice General (Preliminares + Capítulos 1..10 + Bibliografía + Anexos)
      2. Índice de Tablas
      3. Índice de Figuras, Algoritmos y Listados
    """
    prelim_items = [
        ("Declaración de Autoría", prelim_pages.get("Declaración de Autoría", 2)),
        ("Agradecimientos", prelim_pages.get("Agradecimientos", 3)),
        ("Resumen y Abstract", prelim_pages.get("Resumen y Abstract", 4)),
        ("Índice de Tablas", prelim_pages.get("Índice de Tablas", 8)),
        ("Índice de Figuras, Algoritmos y Listados", prelim_pages.get("Índice de Figuras, Algoritmos y Listados", 10)),
        ("Lista de Acrónimos y Términos", prelim_pages.get("Lista de Acrónimos y Términos", 12)),
    ]

    lines = []

    if style == "academic":
        # Inyectar estilos CSS para Typora y renderizadores HTML
        lines.append("<style>\n")
        lines.append("  .toc-container { width: 100%; margin: 10px 0; font-family: inherit; }\n")
        lines.append("  .toc-row { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 4px; line-height: 1.45; }\n")
        lines.append("  .toc-row.level-1 { font-weight: bold; margin-top: 9px; }\n")
        lines.append("  .toc-row.level-2 { padding-left: 22px; font-weight: normal; }\n")
        lines.append("  .toc-row.visual-row { font-weight: normal; margin-top: 4px; margin-bottom: 4px; font-size: 10.5pt; }\n")
        lines.append("  .toc-title { flex-shrink: 1; }\n")
        lines.append("  .toc-dots { flex-grow: 1; border-bottom: 1.5px dotted #666; margin: 0 8px 3px 8px; min-width: 15px; }\n")
        lines.append("  .toc-page { flex-shrink: 0; text-align: right; min-width: 25px; font-variant-numeric: tabular-nums; }\n")
        lines.append("</style>\n\n")

        # 1. Índice General
        lines.append("# Índice General\n\n<div class=\"toc-container\">\n\n")
        for p_title, p_num in prelim_items:
            lines.append(format_academic_toc_row(p_title, p_num, level=1))

        for level, title, page in toc_results:
            lines.append(format_academic_toc_row(title, page, level=level))

        lines.append("\n</div>\n\n<div style='page-break-after: always;'></div>\n\n")

        # 2. Índice de Tablas
        lines.append("# Índice de Tablas\n\n<div class=\"toc-container\">\n\n")
        for num, tipo, desc, ubi, page in tab_results:
            lines.append(format_academic_visual_row(tipo, num, desc, ubi, page))
        lines.append("\n</div>\n\n<div style='page-break-after: always;'></div>\n\n")

        # 3. Índice de Figuras, Algoritmos y Listados
        lines.append("# Índice de Figuras, Algoritmos y Listados\n\n<div class=\"toc-container\">\n\n")

        lines.append("### Figuras\n\n")
        for num, tipo, desc, ubi, page in fig_results:
            lines.append(format_academic_visual_row(tipo, num, desc, ubi, page))
        lines.append("\n")

        lines.append("### Algoritmos (Pseudocódigo)\n\n")
        for num, tipo, desc, ubi, page in alg_results:
            lines.append(format_academic_visual_row(tipo, num, desc, ubi, page))
        lines.append("\n")

        lines.append("### Listados de Código / Manifiestos\n\n")
        for num, tipo, desc, ubi, page in list_results:
            lines.append(format_academic_visual_row(tipo, num, desc, ubi, page))
        lines.append("\n</div>\n\n")

    else:
        # Estilo dots clásico en Markdown
        lines.append("# Índice General\n\n")
        for p_title, p_num in prelim_items:
            lines.append(format_toc_line(p_title, p_num, is_bold=True, indent=0))

        for level, title, page in toc_results:
            is_bold = (level == 1)
            indent = 0 if level == 1 else 1
            lines.append(format_toc_line(title, page, is_bold=is_bold, indent=indent))

        lines.append("\n\n<div style='page-break-after: always;'></div>\n\n")

        lines.append("# Índice de Tablas\n\n")
        for num, tipo, desc, ubi, page in tab_results:
            lines.append(format_visual_line(tipo, num, desc, ubi, page))

        lines.append("\n\n<div style='page-break-after: always;'></div>\n\n")

        lines.append("# Índice de Figuras, Algoritmos y Listados\n\n")
        lines.append("### Figuras\n\n")
        for num, tipo, desc, ubi, page in fig_results:
            lines.append(format_visual_line(tipo, num, desc, ubi, page))
        lines.append("\n")

        lines.append("### Algoritmos (Pseudocódigo)\n\n")
        for num, tipo, desc, ubi, page in alg_results:
            lines.append(format_visual_line(tipo, num, desc, ubi, page))
        lines.append("\n")

        lines.append("### Listados de Código / Manifiestos\n\n")
        for num, tipo, desc, ubi, page in list_results:
            lines.append(format_visual_line(tipo, num, desc, ubi, page))
        lines.append("\n")

    return "".join(lines)


def update_tfm_completo():
    """Regenera TFM_Completo.md concatenando los capítulos en el orden oficial canónico."""
    all_files = PRELIMINARY_FILES + ["0_Indices.md", ACRONIMOS_FILE] + CHAPTER_FILES
    parts = []

    for fname in all_files:
        fpath = os.path.join(MEMORIA_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                parts.append(f.read())
        else:
            print(f"[!] Advertencia: archivo no encontrado: {fpath}")

    combined = "\n\n<div style='page-break-after: always;'></div>\n\n".join(parts)
    with open(TFM_COMPLETO_MD, "w", encoding="utf-8") as f:
        f.write(combined)


def main():
    parser = argparse.ArgumentParser(
        description="Extrae páginas de un PDF maquetado e inyecta números de página en los índices del TFM."
    )
    parser.add_argument(
        "--pdf",
        type=str,
        default=None,
        help="Ruta al PDF compilado previamente desde Typora (por defecto: el más reciente entre TFM_Completo.pdf y TFM_JesusSolisOrtega.pdf)",
    )
    parser.add_argument(
        "--style",
        type=str,
        choices=["academic", "dots"],
        default="academic",
        help="Estilo visual: 'academic' (puntos guía dinámicos alineados al margen derecho mediante flexbox) o 'dots' (puntos de texto plano en markdown).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra las páginas detectadas sin modificar los ficheros markdown",
    )
    parser.add_argument(
        "--no-combinar",
        action="store_true",
        help="No regenerar TFM_Completo.md tras actualizar 0_Indices.md",
    )
    args = parser.parse_args()

    pdf_to_use = args.pdf if args.pdf else resolve_default_pdf()
    print(f"==> Analizando PDF: {pdf_to_use}")
    pages = extract_pages_from_pdf(pdf_to_use)
    start_page = detect_content_start_page(pages)
    print(f"    Total de páginas en PDF: {len(pages)}")
    print(f"    Capítulo 1 (cuerpo) detectado en página física: {start_page}")

    prelim_pages = match_preliminaries(pages, start_page)
    print("    Preliminares detectados:")
    for k, v in prelim_pages.items():
        print(f"      - {k}: pág. {v}")

    print("==> Extrayendo estructura de secciones y elementos visuales...")
    toc_items = extract_toc_items()
    figuras, tablas, algoritmos, listados = extract_visual_items()

    print(f"    Títulos de contenido detectados: {len(toc_items)}")
    print(f"    Figuras: {len(figuras)} | Tablas: {len(tablas)} | Algoritmos: {len(algoritmos)} | Listados: {len(listados)}")

    print("==> Mapeando cada elemento con su página física en el PDF...")
    toc_results = match_toc_pages(toc_items, pages, start_page)
    fig_results = match_visual_pages(figuras, pages, start_page)
    tab_results = match_visual_pages(tablas, pages, start_page)
    alg_results = match_visual_pages(algoritmos, pages, start_page)
    list_results = match_visual_pages(listados, pages, start_page)

    # Validar que no falte ninguno
    missing_toc = [t for l, t, p in toc_results if p is None]
    missing_fig = [f"{t} {n}" for n, t, d, u, p in fig_results if p is None]
    missing_tab = [f"{t} {n}" for n, t, d, u, p in tab_results if p is None]
    missing_alg = [f"{t} {n}" for n, t, d, u, p in alg_results if p is None]
    missing_list = [f"{t} {n}" for n, t, d, u, p in list_results if p is None]

    total_missing = len(missing_toc) + len(missing_fig) + len(missing_tab) + len(missing_alg) + len(missing_list)

    if total_missing > 0:
        print(f"\n[!] Advertencia: {total_missing} elementos no pudieron localizarse automáticamente:")
        for m in missing_toc:
            print(f"    - Sección: {m}")
        for m in missing_fig + missing_tab + missing_alg + missing_list:
            print(f"    - Visual: {m}")
    else:
        print("    ✓ Todos los elementos (100%) fueron mapeados exitosamente con su número de página.")

    if args.dry_run:
        print("\n--- Vista previa (primeros 10 elementos del TOC) ---")
        for level, title, page in toc_results[:10]:
            print(f"  [{page or '?'}] {title}")
        print("\n--- Vista previa (primeras 5 figuras) ---")
        for num, tipo, desc, ubi, page in fig_results[:5]:
            print(f"  [{page or '?'}] {tipo} {num}: {desc[:50]}...")
        print("\n[Dry-run] No se modificó ningún archivo.")
        return

    print(f"==> Generando '{INDICES_MD}' (estilo '{args.style}')...")
    new_indices_content = generate_indices_md(
        prelim_pages, toc_results, fig_results, tab_results, alg_results, list_results, style=args.style
    )
    with open(INDICES_MD, "w", encoding="utf-8") as f:
        f.write(new_indices_content)
    print(f"    ✓ '{INDICES_MD}' actualizado.")

    if not args.no_combinar:
        print(f"==> Regenerando '{TFM_COMPLETO_MD}'...")
        update_tfm_completo()
        print(f"    ✓ '{TFM_COMPLETO_MD}' actualizado.")

    print("\n" + "=" * 60)
    print("✓ Índices y documento completo actualizados con éxito.")
    print("=" * 60)


if __name__ == "__main__":
    main()
