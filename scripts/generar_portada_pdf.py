"""
generar_portada_pdf.py
======================
Genera el PDF de la portada oficial institucional del TFM para la Escuela Técnica
Superior de Ingeniería Informática (ETSII) / Universidad de Sevilla con los datos reales.

Uso:
    python scripts/generar_portada_pdf.py
"""
import os
import weasyprint

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOGO_PATH = os.path.join(ROOT_DIR, "memoria", "img", "logo_uni.png")
OUTPUT_PDF = os.path.join(ROOT_DIR, "memoria", "portada_oficial.pdf")

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @page {{
    size: A4;
    margin: 2.5cm 3cm 2.5cm 3cm;
  }}
  body {{
    font-family: "Latin Modern Roman", "Computer Modern Roman", "Times New Roman", serif;
    color: #111;
    text-align: center;
    margin: 0;
    padding: 0;
    line-height: 1.3;
  }}
  .logo {{
    width: 140px;
    height: auto;
    margin-bottom: 25px;
  }}
  .institution {{
    font-size: 13pt;
    font-weight: bold;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
    text-transform: uppercase;
  }}
  .center-name {{
    font-size: 12pt;
    font-weight: bold;
    letter-spacing: 0.5px;
    margin-bottom: 45px;
    text-transform: uppercase;
  }}
  .work-type {{
    font-size: 13pt;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 25px;
  }}
  .title {{
    font-size: 17pt;
    font-weight: bold;
    line-height: 1.35;
    margin: 0 auto 35px auto;
    max-width: 95%;
  }}
  .subtitle {{
    font-size: 13pt;
    font-weight: normal;
    font-style: italic;
    margin-top: 8px;
  }}
  .field-label {{
    font-size: 10.5pt;
    color: #333;
    margin-bottom: 3px;
  }}
  .field-value {{
    font-size: 12pt;
    font-weight: bold;
    margin-bottom: 22px;
  }}
  .field-value-normal {{
    font-size: 11pt;
    margin-bottom: 22px;
  }}
  .footer-date {{
    position: absolute;
    bottom: 20px;
    left: 0;
    right: 0;
    font-size: 11.5pt;
    font-weight: bold;
  }}
</style>
</head>
<body>
  <img class="logo" src="file://{LOGO_PATH}" alt="Universidad de Sevilla">
  
  <div class="institution">Universidad de Sevilla</div>
  <div class="center-name">Escuela Internacional de Posgrado</div>
  
  <div class="work-type">Trabajo Fin de Máster</div>
  
  <div class="title">
    Diseño e implementación de una Plataforma Interna de Despliegue (IDP) en Openshift controlada por Agentes IA mediante el protocolo MCP
    <div class="subtitle">(Agentic Deployer)</div>
  </div>
  
  <div class="field-label">Realizado por</div>
  <div class="field-value">Jesús Solís Ortega</div>
  
  <div class="field-label">Para la obtención del título de</div>
  <div class="field-value-normal">Máster en Ingeniería del Software: Cloud, Datos y Gestión TI</div>
  
  <div class="field-label">Dirigido por</div>
  <div class="field-value">Manuel Resinas Arias de Reyna</div>
  
  <div class="footer-date">Convocatoria de Noviembre, curso 2025/26</div>
</body>
</html>
"""

def main():
    weasyprint.HTML(string=html_content, base_url=ROOT_DIR).write_pdf(OUTPUT_PDF)
    print(f"✓ Portada oficial generada con éxito en: {OUTPUT_PDF}")

if __name__ == "__main__":
    main()

