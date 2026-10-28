# Anexo C. Manual de Instalación, Despliegue y Operación

El presente anexo constituye la guía técnica operativa para la replicación experimental, instalación, despliegue y uso del sistema *Agentic Deployer*. Su estructura responde a las directrices de reproducibilidad científica y manuales de ingeniería de software.

---

## C.1. Manual de Instalación y Despliegue

### C.1.1. Requisitos Previos del Sistema

Para el correcto despliegue del sistema en un entorno anfitrión local o servidor dedicado, se requieren los siguientes componentes:

* **Sistema Operativo:** GNU/Linux (probado en distribuciones basadas en Debian/Ubuntu) o macOS. Compatible con Windows mediante WSL2.
* **Entorno de Ejecución:** Python 3.11 o superior.
* **Gestor de Paquetes:** `pip` y soporte nativo para entornos virtuales (`python3-venv`).
* **Navegador Web:** Chrome, Firefox o Edge para interactuar con las interfaces de usuario.
* **Motor de Inferencia Local (Opcional para modo on-premise):** Ollama (v0.3.0 o superior) con soporte para aceleración por GPU (CUDA / Metal) o ejecución en CPU.

### C.1.2. Obtención del Código Fuente y Preparación del Entorno

1. **Clonación del repositorio e ingreso al directorio raíz:**
   ```bash
   git clone <url-del-repositorio>/TFM.git
   cd TFM
   ```

2. **Creación y activación del entorno virtual de Python:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalación de dependencias de producción y calidad:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Instalación de binarios de navegación para pruebas E2E (Playwright):**
   ```bash
   playwright install chromium
   ```

### C.1.3. Configuración de Variables de Entorno

El sistema se parametriza mediante un archivo de configuración `.env`. Se incluye una plantilla base preconfigurada (`.env.example`):

```bash
cp .env.example .env
```

Los parámetros fundamentales configurables en dicho archivo comprenden:
* `LLM_PROVIDER`: Proveedor de inferencia cognitivo (`ollama`, `openai` o `fake`).
* `OLLAMA_BASE_URL`: Dirección de escucha del servidor local de Ollama (por defecto `http://localhost:11434`).
* `OLLAMA_MODEL`: Identificador del modelo local a cargar (por defecto `qwen2.5-coder:7b`).
* `OPENAI_API_KEY`: Clave de autenticación en caso de seleccionar el proveedor cloud comercial.
* `DATABASE_PATH`: Ruta al fichero de persistencia SQLite (`agentic_deployer.db`).

*(Nota: Se provee el script ejecutable `scripts/install.sh`, el cual automatiza todos los pasos anteriores e inicializa la descarga del modelo local en entornos compatibles).*

### C.1.4. Verificación de la Instalación

Antes de iniciar los servicios en producción, se recomienda ejecutar la suite de verificación automatizada:

```bash
pytest -v
```

La superación de las pruebas unitarias y de integración confirma que los contratos de dominio, la máquina de estados FSM y el validador de seguridad se encuentran operativos.

---

## C.2. Ejecución de los Subsistemas

La arquitectura desacoplada requiere la ejecución simultánea de dos componentes independientes:

### C.2.1. Backend de Operaciones y Servidor MCP (FastAPI)

En una primera terminal con el entorno virtual activado, se inicia el servidor de aplicaciones:

```bash
uvicorn app.infrastructure.main:app --host 0.0.0.0 --port 8000 --reload
```

* **Panel de Control HITL:** [http://localhost:8000/frontend/index.html](http://localhost:8000/frontend/index.html)
* **Documentación interactiva OpenAPI (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

### C.2.2. Interfaz Conversacional del Agente (Streamlit)

En una segunda terminal independiente con el entorno virtual activo, se lanza la aplicación de chat:

* **Modo On-Premise (Soberanía del Dato con Ollama):**
  ```bash
  # En terminal auxiliar, arrancar el servicio de modelos si no estuviera activo:
  ollama serve
  
  # Lanzar la interfaz agéntica:
  LLM_PROVIDER=ollama OLLAMA_MODEL=qwen2.5-coder:7b streamlit run app/agent_layer/chat_app.py
  ```

* **Modo Demostración Rápida (Determinista, sin consumo de GPU ni API Keys):**
  ```bash
  streamlit run app/agent_layer/chat_app.py
  ```

* **Punto de acceso web:** [http://localhost:8501](http://localhost:8501)

---

## C.3. Manual de Usuario y Operación HITL

### C.3.1. Formulación de Solicitudes en Lenguaje Natural

1. El usuario accede a la interfaz conversacional en el puerto `8501`.
2. En la caja de texto inferior, introduce una petición de servicio en lenguaje libre. Ejemplos válidos:
   * *«Necesito desplegar una API en Python para publicar los datos del proyecto de investigación.»*
   * *«Quiero instalar un gestor de contenidos WordPress para el congreso del departamento.»*
   * *«Despliega un portal web estático con Nginx para documentación.»*
3. **Interacción y negociación:** Si la petición omite detalles obligatorios o infringe políticas de seguridad, el agente razona sobre las observaciones devueltas por el validador y formula preguntas asistidas para consensuar parámetros seguros.
4. **Registro de la intención:** Una vez acordados los parámetros válidos, el agente invoca la herramienta MCP y registra la intención de despliegue en la base de datos en estado de cuarentena (`PENDING_APPROVAL`), proporcionando al usuario el identificador único del despliegue (ej. `dep-7f3a2c1b`).

### C.3.2. Supervisión Técnica en el Dashboard HITL

1. El operador técnico del SIC accede al Dashboard de Aprobación en [http://localhost:8000/frontend/index.html](http://localhost:8000/frontend/index.html).
2. En la sección **«Solicitudes Pendientes»**, inspecciona la tarjeta técnica generada por la IA:
   * Parámetros de cómputo (límites de CPU y memoria).
   * Imagen de contenedor auditada y puerto de servicio.
   * Manifiesto declarativo generado y resultado del análisis de seguridad.
3. **Decisión del operador:**
   * **Aprobar:** Al pulsar el botón de confirmación, la FSM transiciona al estado `DEPLOYED`, invocando la provisión de infraestructura y archivando la traza criptográfica de auditoría.
   * **Rechazar:** Si el operador detecta alguna anomalía administrativa, pulsa rechazar, pasando la solicitud al estado terminal inmutable `REJECTED`.

### C.3.3. Notificación Asíncrona y Canal de Retorno

El investigador puede consultar en todo momento el avance de su solicitud desde el panel lateral de la interfaz de chat en Streamlit o mediante el endpoint REST:

```bash
curl -X GET "http://localhost:8000/hitl/status/dep-7f3a2c1b"
```

El sistema responderá con el estado actual de la Máquina de Estados (`PENDING_APPROVAL`, `DEPLOYED` o `REJECTED`) junto con las marcas temporales de validación, garantizando la trazabilidad integral del servicio.

