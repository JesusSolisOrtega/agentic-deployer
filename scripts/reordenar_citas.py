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

    files = [
        "00_Portada.md",
        "00_Declaracion_Agradecimientos.md",
        "00_Resumen_Abstract.md",
        "00_Acronimos.md",
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
        "Anexo_A_YAML.md",
        "Anexo_B_Planificacion.md",
        "Anexo_C_Manual_Despliegue_y_Usuario.md"
    ]

    code_splitter = re.compile(r"(```.*?```|`[^`\n]+`)", re.DOTALL)
    cit_regex = re.compile(r'\[(\d+(?:,\s*\d+)*)\](?!\()')

    # PASO 1: Recolectar el orden estricto de primera aparición
    old_to_new = {}
    order_list = []

    for fname in files:
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        parts = code_splitter.split(content)
        for i, part in enumerate(parts):
            # Sólo procesar texto fuera de código (índices pares)
            if i % 2 == 0:
                for match in cit_regex.finditer(part):
                    raw_nums = match.group(1).split(',')
                    for n in raw_nums:
                        num_str = n.strip()
                        if num_str in valid_bib_entries and num_str not in old_to_new:
                            new_id = len(old_to_new) + 1
                            old_to_new[num_str] = new_id
                            order_list.append((num_str, new_id, fname))

    print(f"Total citas únicas detectadas en el texto: {len(old_to_new)}")
    for old_id, new_id, fname in order_list:
        if old_id != str(new_id):
            print(f"  Cambio: [{old_id}] -> [{new_id}] (primera aparición en {fname})")

    # Identificar huérfanas si las hubiera
    for old_id in valid_bib_entries.keys():
        if old_id not in old_to_new:
            new_id = len(old_to_new) + 1
            old_to_new[old_id] = new_id
            print(f"Aviso: La referencia [{old_id}] no se cita en el texto. Se asigna [{new_id}].")

    # PASO 2: Reemplazar en los archivos Markdown
    def replace_citation_group(match):
        raw_nums = match.group(1).split(',')
        replaced_nums = []
        is_cit = False
        for n in raw_nums:
            s = n.strip()
            if s in old_to_new:
                replaced_nums.append(str(old_to_new[s]))
                is_cit = True
            else:
                replaced_nums.append(s)
        if is_cit:
            return '[' + ', '.join(replaced_nums) + ']'
        return match.group(0)

    for fname in files:
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        parts = code_splitter.split(content)
        modified = False
        for i in range(0, len(parts), 2):
            new_part = cit_regex.sub(replace_citation_group, parts[i])
            if new_part != parts[i]:
                parts[i] = new_part
                modified = True

        if modified:
            new_content = "".join(parts)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Actualizado: {fname}")

    # PASO 3: Reconstruir la bibliografía en el nuevo orden
    new_to_old = {v: k for k, v in old_to_new.items()}
    new_bib_content = preamble
    for new_id in sorted(new_to_old.keys()):
        old_id = new_to_old[new_id]
        text = valid_bib_entries[old_id]
        new_bib_content += f"**[{new_id}]**{text}"

    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(new_bib_content)
    print("Bibliografía reordenada con éxito.")

    # PASO 4: Verificación estricta de orden
    print("\n--- Verificación de secuencia ---")
    verification_seen = []
    strictly_sequential = True
    last_val = 0
    for fname in files:
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        parts = code_splitter.split(content)
        for i in range(0, len(parts), 2):
            for match in cit_regex.finditer(parts[i]):
                for n in match.group(1).split(','):
                    s = n.strip()
                    if not s.isdigit():
                        continue
                    val = int(s)
                    if val in new_to_old: # es una cita válida
                        if val not in verification_seen:
                            if val != last_val + 1:
                                print(f"ERROR: En {fname}, apareció [{val}] pero se esperaba [{last_val + 1}]")
                                strictly_sequential = False
                            last_val = val
                            verification_seen.append(val)

    if strictly_sequential and len(verification_seen) == len(valid_bib_entries):
        print(f"ÉXITO: Las {len(verification_seen)} citas aparecen en orden estrictamente creciente de 1 a {len(valid_bib_entries)}.")
    else:
        print(f"ATENCIÓN: Citas vistas: {len(verification_seen)} de {len(valid_bib_entries)}. Secuencial: {strictly_sequential}")

if __name__ == "__main__":
    main()
