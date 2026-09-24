import os

files = [
    "0_Indices.md",
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
output_file = "/home/jesus/projects/TFM/TFM_Completo.md"

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write("# Memoria del Trabajo de Fin de Máster\n\n")
    for fname in files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write("\n\n<div style='page-break-after: always;'></div>\n\n")
            print(f"Añadido: {fname}")
        else:
            print(f"No encontrado: {fname}")

print(f"\nGenerado exitosamente: {output_file}")
