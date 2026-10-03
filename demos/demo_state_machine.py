import json
import ollama
import sys

def extract_entities(user_message: str, model_name: str) -> dict:
    """Fase 1: El LLM actúa únicamente como Extractor de Entidades (Comprensión lectora)"""
    prompt = f"""
    Extrae las siguientes entidades del mensaje del usuario y devuélvelas en formato JSON estricto.
    Las claves del JSON deben ser obligatoriamente: "name", "image", "port".
    Si el usuario no menciona alguna de ellas, su valor debe ser null.
    
    Mensaje del usuario: "{user_message}"
    """
    
    response = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': prompt}],
        format='json'
    )
    
    try:
        # pyrefly: ignore [no-any-return-explicit]
        return json.loads(response['message']['content'])
    except:
        return {"name": None, "image": None, "port": None}

def generate_response(state: dict, model_name: str) -> str:
    """Fase 3: El LLM genera texto para pedir los datos que faltan basándose en la plantilla"""
    missing = [k for k, v in state.items() if v is None]
    
    prompt = f"""
    Eres un asistente de despliegues. El usuario quiere desplegar un servicio.
    Actualmente te faltan estos datos obligatorios: {', '.join(missing)}.
    Pídele al usuario educadamente que te proporcione los datos que faltan. 
    NO inventes los datos. Sé breve.
    """
    
    response = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': prompt}]
    )
    # pyrefly: ignore [no-any-return-implicit]
    return response['message']['content']

# pyrefly: ignore [unannotated-return]
def run_stateful_demo(model_name: str):
    print(f"\n{'='*60}")
    print(f"=== MODO ESTADO DESTILADO (STATEFUL SLOT FILLING) ===")
    print(f"=== Modelo: {model_name} ===")
    print(f"{'='*60}")
    
    # 1. Nuestra plantilla (Estado)
    state = {"name": None, "image": None, "port": None}
    print(f"[ESTADO INICIAL] {state}")
    
    dialogue = [
        "Hola equipo del SIC, necesito desplegar un servicio web por favor.",
        "Se va a llamar proyecto-web",
        "La imagen será nginx:latest y el puerto es el 80. Con eso ya lo tendríamos."
    ]
    
    for turn, user_msg in enumerate(dialogue, 1):
        print(f"\n[Turno {turn}] Usuario: {user_msg}")
        
        # 1. Extraer datos (LLM)
        extracted = extract_entities(user_msg, model_name)
        
        # 2. Actualizar el estado en Python (Control determinista)
        for key in state:
            if state[key] is None and extracted.get(key) is not None:
                state[key] = extracted[key]
                
        print(f"          [ESTADO INTERNO ACTUALIZADO]: {state}")
        
        # 3. Lógica de Negocio (Python puro, no el LLM)
        if all(v is not None for v in state.values()):
            print(f"[Turno {turn}] Python:  ¡Plantilla completa! Ejecutando herramienta de despliegue...")
            print(f"          [🛠️  JSON ENVIADO AL SISTEMA]: {json.dumps(state, indent=2)}")
            print(f"[Turno {turn}] IA:      ¡El servicio {state['name']} se ha desplegado correctamente!")
            break
        else:
            # Si faltan datos, pedimos al LLM que pregunte
            response = generate_response(state, model_name)
            print(f"[Turno {turn}] IA:      {response}")

if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else 'qwen2.5:7b'
    print(f"Inicializando {model} vía Ollama...")
    run_stateful_demo(model)
    print("\nFin de la demo.")
