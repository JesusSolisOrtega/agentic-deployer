# Mutation Testing Report — Agentic Deployer
# Generated: 2026-09-27
# Tool: mutmut 4.x
# Config: test_mutmut.ini
# Scope: app/application/ + app/domain/

## Summary

| Módulo | Supervivientes | Causa | Criticidad |
|---|---|---|---|
| `domain.exceptions` | 2 | Mutaciones en `__init__` de la clase de excepción | Baja (mensaje de error, no lógica) |
| `security_validator._parse_cpu/_parse_ram` | 24 | Funciones de conversión de strings sin tests unitarios directos | Media |
| `security_validator.validate` | 3 | Condiciones límite en reglas compuestas | Media |
| `use_cases.execute` | 1 | Rama alternativa de acción DELETE | Baja |
| `agent.FakeLLMClient` | 54 | Módulo de demo sin tests (by design) | No aplicable |
| `agent.AgentOrchestrator` | 45 | Agente cognitivo: testar LLM-dependent code es Out-of-Scope para mutmut | No aplicable |
| `agent_layer.tools` | 14 | Herramientas MCP: requieren mocks de red | Baja-Media |
| **TOTAL** | **143** | | |

## Análisis de Pertinencia

Los módulos **`agent.FakeLLMClient`** (54) y **`agent.AgentOrchestrator`** (45) acumulan el 69,9% de los supervivientes.
Ambos quedan fuera del alcance de auditoría por diseño:
- `FakeLLMClient` es código de demostración, no de producción.
- `AgentOrchestrator` encapsula la lógica de interacción con el LLM, cuyo testeo mediante mutmut no es significativo
  (el LLM es un sistema externo no determinista que no puede auditarse con aserciones deterministas).

## Núcleo Hexagonal (Scope Principal)

El alcance declarado en `test_mutmut.ini` es `app/application/` + `app/domain/`.
Sobre este scope, los supervivientes relevantes son:

| Módulo | Supervivientes |
|---|---|
| `domain.exceptions` | 2 |
| `security_validator._parse_cpu/_parse_ram` | 24 |
| `security_validator.validate` (regla engine) | 3 |
| `use_cases.execute` | 1 |
| **Subtotal núcleo hexagonal** | **30** |

Los 30 supervivientes del núcleo hexagonal identifican brechas en la cobertura de las
funciones de conversión de recursos (`_parse_cpu`, `_parse_ram`) que convierten strings
como `"500m"` o `"1024Mi"` a valores normalizados.
Estas brechas son candidatas directas a T3-followup: añadir tests parametrizados
para cada variante de formato de recursos.

## Archivos de Referencia

- `mutmut_results_raw.txt` — Salida completa del comando `mutmut results`
- Este archivo — Análisis categorizado
