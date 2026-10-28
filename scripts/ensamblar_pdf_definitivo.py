#!/usr/bin/env python3
"""
ensamblar_pdf_definitivo.py
===========================
Ensambla el PDF definitivo del TFM sustituyendo o anteponiendo la portada
oficial vectorial (memoria/portada_oficial.pdf) generada con WeasyPrint
sobre el PDF exportado desde Typora o Pandoc (TFM_JesusSolisOrtega.pdf).

Uso:
    python scripts/ensamblar_pdf_definitivo.py
    python scripts/ensamblar_pdf_definitivo.py --input TFM_JesusSolisOrtega.pdf --output TFM_JesusSolisOrtega_FINAL.pdf
"""

import os
import sys
import argparse
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def resolve_default_input() -> str:
    """Selecciona el PDF más reciente entre TFM_Completo.pdf y TFM_JesusSolisOrtega.pdf."""
    c1 = os.path.join(ROOT_DIR, "TFM_Completo.pdf")
    c2 = os.path.join(ROOT_DIR, "TFM_JesusSolisOrtega.pdf")
    if os.path.exists(c1) and os.path.exists(c2):
        return c1 if os.path.getmtime(c1) >= os.path.getmtime(c2) else c2
    elif os.path.exists(c1):
        return c1
    return c2

DEFAULT_COVER = os.path.join(ROOT_DIR, "memoria", "portada_oficial.pdf")
DEFAULT_OUTPUT = os.path.join(ROOT_DIR, "TFM_JesusSolisOrtega_DEFINITIVO.pdf")

def main():
    parser = argparse.ArgumentParser(description="Ensambla el PDF definitivo del TFM con portada oficial.")
    parser.add_argument("--cover", default=DEFAULT_COVER, help="Ruta al PDF de la portada")
    parser.add_argument("--input", default=None, help="Ruta al PDF exportado desde Typora")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Ruta de salida del PDF definitivo")
    parser.add_argument("--replace-page1", action="store_true", default=True,
                        help="Reemplaza la página 1 del input por la portada oficial (por defecto: True si el input ya incluía portada)")
    args = parser.parse_args()

    input_pdf = args.input if args.input else resolve_default_input()

    if not os.path.exists(args.cover):
        print(f"[!] Error: No se encuentra la portada oficial en: {args.cover}")
        print("    Ejecuta primero: python scripts/generar_portada_pdf.py")
        sys.exit(1)

    if not os.path.exists(input_pdf):
        print(f"[!] Error: No se encuentra el PDF de entrada en: {input_pdf}")
        print("    Abre 'TFM_Completo.md' en Typora y expórtalo como PDF")
        sys.exit(1)

    # Detectar número de páginas del input
    try:
        page_count_out = subprocess.check_output(
            ["pdftotext", input_pdf, "-"], stderr=subprocess.DEVNULL
        ).decode("utf-8", errors="ignore")
        num_pages = page_count_out.count("\x0c")
    except Exception:
        num_pages = 0

    print(f"[*] PDF de entrada detectado: {input_pdf} (~{num_pages} páginas)")
    print(f"[*] Portada oficial: {args.cover}")

    # Verificar si la primera página del input ya es una portada
    first_page_text = ""
    try:
        out = subprocess.check_output(["pdftotext", "-f", "1", "-l", "1", input_pdf, "-"]).decode("utf-8")
        first_page_text = out.lower()
    except Exception:
        pass

    has_cover_already = "trabajo fin de m" in first_page_text or "universidad de sevilla" in first_page_text

    temp_body = os.path.join(ROOT_DIR, ".temp_cuerpo.pdf")

    try:
        if has_cover_already and num_pages > 1:
            print("    -> La página 1 del PDF ya contiene una portada de Typora. Se sustituirá por la portada oficial vectorial.")
            cmd_extract = [
                "gs", "-dBATCH", "-dNOPAUSE", "-q", "-sDEVICE=pdfwrite",
                "-dFirstPage=2", f"-sOutputFile={temp_body}", input_pdf
            ]
            subprocess.check_call(cmd_extract)
            body_to_join = temp_body
        else:
            print("    -> Se antepone la portada oficial al inicio del documento.")
            body_to_join = input_pdf

        # Unir portada oficial + cuerpo usando pdfunite
        cmd_unite = ["pdfunite", args.cover, body_to_join, args.output]
        subprocess.check_call(cmd_unite)

        print(f"\n✓ ¡Éxito! PDF definitivo generado con portada institucional vectorial:")
        print(f"  → {args.output}")

    finally:
        if os.path.exists(temp_body):
            os.remove(temp_body)

if __name__ == "__main__":
    main()

