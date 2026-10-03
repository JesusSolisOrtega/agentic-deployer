import os
import sys
import json

# Setup python path to find the 'app' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agent_layer.agent import AgentOrchestrator, OllamaLLMClient
from app.agent_layer.chat_app import SYSTEM_PROMPT

# pyrefly: ignore [unannotated-return]
def run_incremental_dialogue(orchestrator: AgentOrchestrator, mode: str):
    print(f"\n{'='*60}")
    print(f"=== EJECUCIÓN (MODO: {mode}) ===")
    print(f"{'='*60}")
    
    # Reset history
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Turn 1
    user_msg_1 = "Hola equipo del SIC, necesito desplegar un servicio web por favor."
    print(f"\n[Turno 1] Usuario: {user_msg_1}")
    response, history = orchestrator.run(user_msg_1, history)
    print(f"[Turno 1] IA:      {response}")
    
    # Turn 2
    user_msg_2 = "Se va a llamar proyecto-web"
    print(f"\n[Turno 2] Usuario: {user_msg_2}")
    response, history = orchestrator.run(user_msg_2, history)
    print(f"[Turno 2] IA:      {response}")
    
    # Turn 3
    user_msg_3 = "La imagen será nginx:latest y el puerto es el 80. Con eso ya lo tendríamos."
    print(f"\n[Turno 3] Usuario: {user_msg_3}")
    try:
        response, history = orchestrator.run(user_msg_3, history)
    except Exception as e:
        print(f"[Turno 3] IA:      [❌ FALLO CRÍTICO DE LLM]")
        print(f"                   El modelo colapsó intentando generar la estructura.")
        print(f"                   Excepción interna: {str(e)[:100]}...")
        return
        
    # Check if tool was called in the history
    last_assistant_msg = next((m for m in reversed(history) if m["role"] == "assistant"), None)
    
    if last_assistant_msg and last_assistant_msg.get("tool_calls"):
        print(f"[Turno 3] IA:      [🛠️  ¡ÉXITO! Se ha emitido el JSON de la herramienta]")
        print(f"                   JSON: {json.dumps(last_assistant_msg['tool_calls'], indent=2)}")
    else:
        print(f"[Turno 3] IA:      {response}")
        print(f"                   [❌ FALLO! El modelo ignoró el JSON y respondió con texto conversacional]")


if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5:7b"
    print(f"Inicializando {model} vía Ollama...")
    llm = OllamaLLMClient(model=model)
    orchestrator = AgentOrchestrator(llm=llm)
    
    # 1. Run without suffix (Standard ReAct - Should fail as documented)
    os.environ["USE_REINFORCEMENT_SUFFIX"] = "false"
    run_incremental_dialogue(orchestrator, "ESTÁNDAR (SIN SUFIJO)")
    
    # 2. Run with suffix (Reinforced ReAct - Should succeed)
    os.environ["USE_REINFORCEMENT_SUFFIX"] = "true"
    run_incremental_dialogue(orchestrator, "REFORZADO (CON SUFIJO DE MITIGACIÓN)")
    
    print("\nFin de la demo.")
