# Mutation Testing Report — Agentic Deployer

<p align="center">
  <b>English Version</b> | <b><a href="mutmut_report.es.md">Versión en Español</a></b>
</p>

# Generated: 2026-09-27  
# Tool: mutmut 4.x  
# Config: test_mutmut.ini  
# Scope: app/application/ + app/domain/  

## Summary

| Module | Surviving Mutants | Root Cause | Criticality |
|---|---|---|---|
| `domain.exceptions` | 2 | Mutations in exception class `__init__` | Low (error message formatting, not domain logic) |
| `security_validator._parse_cpu/_parse_ram` | 24 | String conversion utility functions lacking direct unit tests | Medium |
| `security_validator.validate` | 3 | Boundary conditions in compound validation rules | Medium |
| `use_cases.execute` | 1 | Alternative execution branch for DELETE action | Low |
| `agent.FakeLLMClient` | 54 | Demonstration mock without dedicated test suite (by design) | Not applicable |
| `agent.AgentOrchestrator` | 45 | Cognitive agent: testing LLM-dependent stochastic code is out of scope for mutation testing | Not applicable |
| `agent_layer.tools` | 14 | MCP tools: require network client mocks | Low-Medium |
| **TOTAL** | **143** | | |

## Relevance Analysis

Modules **`agent.FakeLLMClient`** (54) and **`agent.AgentOrchestrator`** (45) account for 69.9% of all surviving mutants. Both remain outside the formal audit boundary by architectural design:
- `FakeLLMClient` represents demonstration test double code rather than production logic.
- `AgentOrchestrator` encapsulates interactions with the LLM inference engine; mutation testing on stochastic model prompts is methodologically unsound and cannot be validated with deterministic assertions.

## Hexagonal Core (Primary Target Scope)

The formal audit scope defined in `test_mutmut.ini` covers `app/application/` and `app/domain/`. Within this scope, relevant surviving mutants are distributed as follows:

| Module | Surviving Mutants |
|---|---|
| `domain.exceptions` | 2 |
| `security_validator._parse_cpu/_parse_ram` | 24 |
| `security_validator.validate` (rule engine) | 3 |
| `use_cases.execute` | 1 |
| **Hexagonal Core Subtotal** | **30** |

The 30 surviving mutants within the hexagonal core reveal test coverage gaps in resource conversion utility functions (`_parse_cpu`, `_parse_ram`), which parse declarative resource strings such as `"500m"` or `"1024Mi"` into normalized numerical values. These gaps represent direct opportunities for subsequent testing improvements via parameterized test cases covering diverse resource format permutations.

## Reference Files

- `mutmut_results_raw.txt` — Full raw stdout from the `mutmut results` command
- This document — Categorized structural analysis

