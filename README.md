# Middleware Orquestador de Despliegues (HITL + MCP)

MVP de un Middleware para la orquestación de despliegues que integra "Human-in-the-Loop" (HITL) y el protocolo "Model Context Protocol" (MCP).

## 🚀 Instalación y Configuración

Se recomienda utilizar Python 3.11 o superior.

### 1. Entorno Virtual y Dependencias

```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno
source .venv/bin/activate

# Instalar dependencias base
pip install -r requirements.txt
```

### 2. Configuración de Playwright (para tests E2E)
El proyecto utiliza Playwright para las pruebas de interfaz de usuario de la vista HITL.
```bash
pip install pytest-playwright
playwright install chromium
```

---

## ⚙️ Ejecución del Proyecto

Para levantar el servidor FastAPI localmente (que incluye la API y sirve el panel estático HITL):

```bash
uvicorn app.infrastructure.main:app --reload --port 8000
```

- **Panel HITL**: [http://localhost:8000/frontend/index.html](http://localhost:8000/frontend/index.html)
- **Documentación API (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Pruebas y Aseguramiento de Calidad (QA)

El proyecto cuenta con un script de bash que ejecuta de forma automática toda la suite de validación como un pipeline de CI local.

### Ejecutar todo el Pipeline (Recomendado)
```bash
chmod +x run_tests.sh
./run_tests.sh
```
Este script ejecutará secuencialmente:
1. **Análisis estático** (Linter con Ruff)
2. **Análisis de tipado** (Mypy)
3. **Tests E2E de Interfaz** (Playwright) *(levanta servidor efímero)*
4. **Property-Based Testing y Tests Unitarios** con análisis de cobertura (Pytest + Hypothesis)
5. **Pruebas de Carga** (Locust)

### Ejecutar Pruebas Individualmente

- **Tests Unitarios y PBT**: 
  ```bash
  python -m pytest app/tests/ -v
  ```
- **Tests E2E (UI)** *(Requiere que el servidor de FastAPI esté levantado)*: 
  ```bash
  python -m pytest tests/test_ui.py -v
  ```
- **Pruebas de Carga**: 
  ```bash
  locust -f locustfile.py --headless -u 10 -r 2 --run-time 5s --host=http://127.0.0.1:8000
  ```

---

## 🧬 Tests de Mutación (Mutation Testing)

> **¿Qué son los tests de mutación?**
> A diferencia de los unit tests, **no se diseñan ni se programan**. La herramienta (`mutmut`) lee tu código de producción, le introduce fallos intencionados o "mutantes" (como cambiar un `>` por `<`, eliminar un `if`, alterar una cadena) y luego ejecuta tus tests existentes sobre ese código roto. 
> - Si tus tests **pasan** ❌: El mutante sobrevive (tus tests no son suficientemente exhaustivos).
> - Si tus tests **fallan** ✅: El mutante muere (tus tests están detectando el fallo correctamente).

Para lanzar un análisis de mutación a **TODO el proyecto** (`app/`) y generar el informe:

### 1. Ejecutar las mutaciones en todo el directorio
*(Atención: esto puede tardar un poco dependiendo de la cantidad de archivos y de cuánto tarden tus tests en ejecutarse).*

```bash
# Activa tu entorno virtual (si no lo está)
source .venv/bin/activate

# Asegúrate de tener mutmut instalado
pip install mutmut

# (Opcional) La configuración de mutmut se encuentra en el archivo setup.cfg
# Ejecuta mutmut contra toda la carpeta (leerá la configuración de setup.cfg)
mutmut run
```

### 2. Generar y Visualizar el Informe
La versión 3 de mutmut ha sustituido los antiguos informes HTML por una interfaz interactiva de terminal (TUI) y comandos directos.

Para abrir el explorador interactivo en tu terminal:
```bash
mutmut browse
```

*(En esta interfaz podrás navegar con las flechas y el teclado por todos los archivos y ver qué líneas exactas han sobrevivido a tus tests).*

Si prefieres ver un listado resumido en la consola de cuántos mutantes sobrevivieron en cada archivo:
```bash
mutmut results
```

Y para ver el código exacto de un mutante específico (por ejemplo, el mutante número 3):
```bash
mutmut show 3
```

---

## 🧹 Limpieza del Repositorio

A medida que ejecutas tests, linters y pruebas de mutación, se generarán diversas cachés y archivos temporales (`__pycache__`, `.pytest_cache`, `mutants/`, `.mutmut-cache`, reportes de cobertura, etc.). 

Para dejar el repositorio completamente limpio y en su estado original, puedes ejecutar el script preparado para ello:

```bash
./clean.sh
```
