import os
import re

def main():
    base_dir = "memoria"
    bib_path = os.path.join(base_dir, "11_Bibliografia.md")
    
    if not os.path.exists(bib_path):
        print("No se encuentra 11_Bibliografia.md")
        return

    with open(bib_path, "r", encoding="utf-8") as f:
        bib_content = f.read()

    # 1. Parsear la bibliografía actual para saber qué números son citas reales
    # Formato esperado: **[X]** Texto...
    bib_blocks = re.split(r'\*\*\[(\d+)\]\*\*', bib_content)
    preamble = bib_blocks[0]
    
    valid_bib_entries = {}
    for i in range(1, len(bib_blocks), 2):
        old_id = bib_blocks[i]
        text = bib_blocks[i+1]
        valid_bib_entries[old_id] = text

    print(f"Encontradas {len(valid_bib_entries)} referencias en la bibliografía.")

    # 2. Reemplazar secuencialmente en los capítulos
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
        "10_Conclusiones_y_Futuro.md"
    ]

    old_to_new = {}
    next_id = 1

    def replace_citation(match):
        nonlocal next_id
        old_id = match.group(1)
        
        # Si el número no está en la bibliografía (ej. array[0]), lo ignoramos
        if old_id not in valid_bib_entries:
            return match.group(0)
        
        # Si es la primera vez que vemos esta cita, le asignamos el siguiente ID
        if old_id not in old_to_new:
            old_to_new[old_id] = next_id
            next_id += 1
            
        new_id = old_to_new[old_id]
        return f"[{new_id}]"

    for fname in files:
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath):
            continue
            
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Buscar todos los [X] en el texto
        new_content = re.sub(r'\[(\d+)\]', replace_citation, content)
        
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Actualizado: {fname}")

    # 3. Identificar citas huérfanas (que están en bibliografía pero no se citan en el texto)
    # Las añadiremos al final para no perderlas
    for old_id in valid_bib_entries.keys():
        if old_id not in old_to_new:
            old_to_new[old_id] = next_id
            next_id += 1
            print(f"Aviso: La referencia [{old_id}] no se cita en el texto. Se añade al final como [{old_to_new[old_id]}].")

    # 4. Reconstruir la bibliografía en el nuevo orden
    # Invertir el diccionario para mapear new_id -> old_id
    new_to_old = {v: k for k, v in old_to_new.items()}
    
    new_bib_content = preamble
    for new_id in sorted(new_to_old.keys()):
        old_id = new_to_old[new_id]
        text = valid_bib_entries[old_id]
        new_bib_content += f"**[{new_id}]**{text}"

    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(new_bib_content)
        
    print("Bibliografía reordenada con éxito.")

if __name__ == "__main__":
    main()
