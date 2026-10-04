# Capítulo 11. Bibliografía y Referencias

A continuación, se detalla la literatura académica, especificaciones técnicas y documentación oficial que fundamentan las decisiones arquitectónicas, metodológicas y algorítmicas expuestas en este Trabajo de Fin de Máster. Las referencias se han estructurado para abarcar tanto el paradigma de la Inteligencia Artificial Generativa como la Ingeniería de Confiabilidad del Sitio (SRE) y los Patrones de Diseño de Software.

**[1]** Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv preprint arXiv:2210.03629. Recuperado de https://arxiv.org/abs/2210.03629
*(Referencia principal para la fundamentación del Bucle Cognitivo y la orquestación agéntica detallada en el Capítulo 5).*

**[2]** Cockburn, A. (2005). *Hexagonal Architecture (Ports and Adapters Pattern)*. Alistair.cockburn.us. Recuperado de https://alistair.cockburn.us/hexagonal-architecture/
*(Documento fundacional para el diseño del Backend Core restrictivo, el aislamiento de dependencias y el modelado del Dominio expuesto en el Capítulo 4).*

**[3]** Anthropic PBC. (2024). *Model Context Protocol (MCP) Specification*. GitHub Open Source Repository. Recuperado de https://github.com/modelcontextprotocol/specification
*(Estándar tecnológico empleado para resolver el problema del 'Vendor Lock-in' y aislar la definición de herramientas JSON-RPC, documentado en la Sección 5.1).*

**[4]** The Kubernetes Authors. (2024). *Kubernetes Documentation: Concepts and Architecture*. Cloud Native Computing Foundation (CNCF). Recuperado de https://kubernetes.io/docs/concepts/
*(Base teórica para la materialización física del código declarativo y el patrón de 'Golden Paths' aplicado en la orquestación de clústeres).*

**[5]** Brown, S. (2018). *The C4 model for visualising software architecture*. C4model.com. Recuperado de https://c4model.com/
*(Metodología de modelado empleada en la Sección 4.1 para la segmentación del sistema en Contexto, Contenedores y Componentes).*

**[6]** MacIver, D. R., Hatfield-Dodds, Z., et al. (2019). *Hypothesis: A new approach to property-based testing*. Journal of Open Source Software, 4(43), 1891.
*(Herramienta y fundamento teórico para la inyección de entropía y la minimización de fallos [Shrinking] documentada en la evaluación de QA del Capítulo 7).*

**[7]** OWASP Foundation. (2023). *OWASP Top 10 for Large Language Model Applications*. Open Worldwide Application Security Project. Recuperado de https://owasp.org/www-project-top-10-for-large-language-model-applications/
*(Marco de referencia para la mitigación de vectores de ataque como la Inyección de Prompt [Prompt Injection], abordada en el Caso de Estudio del Capítulo 8).*

**[8]** AXELOS. (2019). *ITIL Foundation: ITIL 4 Edition*. TSO (The Stationery Office).
*(Marco de gobernanza y buenas prácticas para la gestión de servicios TI, utilizado para justificar las responsabilidades legales y la implementación del patrón Human-In-The-Loop en el Capítulo 6).*

**[9]** Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley Professional.
*(Literatura clásica para la justificación de los patrones Factory y Abstract Adapter utilizados en la conmutación entre OpenAI y Ollama en la Sección 5.2).*

**[10]** Richards, T. (2023). *Streamlit for Data Science: Create interactive data apps in Python* (2nd ed.). Packt Publishing.
*(Referencia metodológica para el diseño de la interfaz gráfica asíncrona tolerante a la ambigüedad empleada por los investigadores).*

**[11]** Pydantic / Colvin, S. (2024). *Pydantic V2: Data validation and settings management using Python type annotations (Rewritten in Rust)*. Recuperado de https://docs.pydantic.dev/
*(Librería core utilizada para la validación estricta de invariantes y la protección contra la deriva de configuración en el núcleo hexagonal).*

**[12]** Segura, S., Fraser, G., Sanchez, A. B., & Ruiz-Cortés, A. (2016). *A survey on metamorphic testing*. IEEE Transactions on Software Engineering, 42(9), 805-824.
*(Estudio fundacional utilizado para diseñar la evaluación cualitativa de la Inteligencia Artificial [Problema del Oráculo y Ruido Léxico] en la Sección 7.4).*

**[13]** Mell, P., & Grance, T. (2011). *The NIST Definition of Cloud Computing*. National Institute of Standards and Technology (NIST) Special Publication 800-145.
*(Definición académica del paradigma de computación en la nube que fundamenta el contexto tecnológico introductorio del TFM).*

**[14]** Newman, S. (2015). *Building Microservices: Designing Fine-Grained Systems*. O'Reilly Media.
*(Referencia principal para la adopción de topologías distribuidas y el desacoplamiento de componentes frente a arquitecturas monolíticas).*

**[15]** Docker Inc. (2024). *Docker Documentation: Container Runtime and Architecture*. Recuperado de https://docs.docker.com/
*(Fundamentación técnica de la contenerización estandarizada de aplicaciones mencionada en el Estado del Arte).*

**[16]** Open Container Initiative (OCI). (2024). *OCI Image Format and Runtime Specification*. Recuperado de https://opencontainers.org/
*(Estándar abierto de la industria para la interoperabilidad de imágenes de contenedores, previniendo el 'vendor lock-in' en orquestación).*

**[17]** Bass, L., Clements, P., & Kazman, R. (2012). *Software Architecture in Practice* (3rd ed.). Addison-Wesley Professional.
*(Literatura base para la formulación de tácticas de disponibilidad, latencia y resiliencia en la capa hexagonal).*

**[18]** Richardson, C. (2018). *Microservices Patterns: With examples in Java*. Manning Publications.
*(Referencia teórica extendida para los patrones de transaccionalidad, API Composition y observabilidad en arquitecturas distribuidas).*

**[19]** Encode OSS. (2024). *HTTPX: A next-generation HTTP client for Python*. Recuperado de https://www.python-httpx.org/
*(Librería utilizada en la implementación del `OllamaLLMClient` nativo para comunicación HTTP/1.1 y HTTP/2 sin dependencias de terceros en la API de Ollama, documentado en la Sección 5.2.1).*

**[20]** Ollama. (2024). *Ollama: Get up and running with large language models locally*. Recuperado de https://ollama.com/
*(Servidor de inferencia local de código abierto que habilita la ejecución de modelos como Llama 3, Mistral y Qwen2.5 en infraestructura propia, garantizando la soberanía del dato institucional. Referenciado en las Secciones 3.3.3, 5.2.1 y 5.2.2).*

**[21]** Chase, H. (2022). *LangChain: Building applications with LLMs through composability*. GitHub Open Source Repository. Recuperado de https://github.com/langchain-ai/langchain
*(Framework de orquestación de agentes LLM analizado en la Sección 2.5.3 como alternativa descartada por su acoplamiento al framework y la ausencia de protocolo de interoperabilidad estándar).*

**[22]** Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., ... & Wang, C. (2023). *AutoGen: Enabling next-generation LLM applications via multi-agent conversation*. arXiv preprint arXiv:2308.08155. Recuperado de https://arxiv.org/abs/2308.08155
*(Framework multi-agente de Microsoft analizado en la Sección 2.5.3, cuya comparativa fundamenta la elección del estándar MCP frente a abstracciones propietarias de orquestación).*

**[23]** Open Policy Agent (OPA). (2024). *OPA: Policy-based control for cloud native environments*. Cloud Native Computing Foundation (CNCF). Recuperado de https://www.openpolicyagent.org/
*(Motor de Policy-as-Code propuesto como evolución del `SecurityContextValidator` en el horizonte a largo plazo del Trabajo Futuro [Sección 10.3.3], permitiendo externalizar y actualizar reglas de validación sin redespliegue del backend).*

**[24]** Kyverno Authors. (2024). *Kyverno: Kubernetes Native Policy Management*. Cloud Native Computing Foundation (CNCF). Recuperado de https://kyverno.io/
*(Alternativa nativa de Kubernetes a OPA para la gestión declarativa de políticas de seguridad como recursos del clúster. Referenciada en la Sección 10.3.3 como mecanismo de gobernanza en el horizonte de madurez del sistema).*

**[25]** Winters, T., Manshreck, T., & Wright, H. (2020). *Software Engineering at Google: Lessons Learned from Programming Over Time*. O'Reilly Media.
*(Citado en la Sección 7.1.4 para respaldar el umbral pragmático del 80% de cobertura de código frente a la falacia del 100%).*

**[26]** McCabe, T. J. (1976). *A Complexity Measure*. IEEE Transactions on Software Engineering, SE-2(4), 308-320.
*(Referencia fundacional de la Complejidad Ciclomática, cuyo umbral moderno estandarizado en la industria [ej. SonarSource / SonarQube] fundamenta el límite de `max-complexity = 15` adoptado en la canalización CI/CD, Sección 7.1.4).*

**[27]** Cohn, M. (2009). *Succeeding with Agile: Software Development Using Scrum*. Addison-Wesley Professional.
*(Obra seminal donde se propone el modelo conceptual de la Pirámide de Pruebas Automáticas, adaptado en el Capítulo 7 para jerarquizar el QA de IA).*

**[28]** Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS), 30, 5998–6008. Recuperado de https://doi.org/10.48550/arXiv.1706.03762
*(Arquitectura fundacional de los Transformers, sobre la que se construyen todos los Modelos de Lenguaje de Gran Escala referenciados en este trabajo, incluyendo GPT, Llama y Qwen).*

**[29]** Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... & Amodei, D. (2020). *Language Models are Few-Shot Learners*. Advances in Neural Information Processing Systems (NeurIPS), 33, 1877–1901. Recuperado de https://doi.org/10.48550/arXiv.2005.14165
*(Estudio seminal que demostró las capacidades emergentes de generalización zero-shot y few-shot en LLMs a gran escala, fundamentando el marco teórico de la Sección 2.1).*

**[30]** Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. Advances in Neural Information Processing Systems (NeurIPS), 35, 24824–24837. Recuperado de https://doi.org/10.48550/arXiv.2201.11903
*(Técnica de prompting que precede conceptualmente al paradigma ReAct, analizada en la Sección 2.1 como antecedente directo del razonamiento intercalado con acción).*

**[31]** Gartner. (2023). *Top Strategic Technology Trends for 2024: Platform Engineering*. Gartner Research.
*(Informe industrial utilizado para justificar el viraje del mercado hacia la Ingeniería de Plataformas y los Portales IDP referenciados en la Sección 1.1).*

**[32]** Google. (2025). *Agent-to-Agent (A2A) Protocol Specification*. Google Open Source.
*(Especificación del protocolo de comunicación entre agentes autónomos mencionado en la Sección 2.2.3 como estándar complementario al MCP).*

**[33]** Mrkšić, N., Séaghdha, D. O., Wen, T. H., Thomson, B., & Young, S. (2017). *Neural Belief Tracker: Data-Driven Dialogue State Tracking*. Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL). Recuperado de https://arxiv.org/abs/1606.03777
*(Literatura fundacional sobre el rastreo del estado del diálogo y la extracción de entidades "Slot-Filling", citado en la Sección 10.3.6 como base teórica para la evolución del Agente hacia un modelo de estado destilado).*

**[34]** LangChain Contributors. (2024). *Memory Management in LLM Applications (ConversationSummaryMemory & Context Distillation)*. LangChain Documentation. Recuperado de https://python.langchain.com/v0.2/docs/concepts/#memory
*(Referencia industrial actual sobre técnicas arquitectónicas para la compresión del historial conversacional y la prevención de la dilución de atención en modelos acotados, mencionada en la Sección 10.3.6).*

**[35]** Hipp, D. R. (2024). *SQLite: A small, fast, reliable, self-contained, SQL database engine*. Recuperado de https://www.sqlite.org/
*(Base de datos transaccional ACID embebida utilizada para la persistencia del estado de la Máquina de Estados Finita).*

**[36]** Kim, G., Humble, J., Debois, P., & Willis, J. (2016). *The DevOps Handbook: How to Create World-Class Agility, Reliability, and Security in Technology Organizations*. IT Revolution Press.
*(Obra fundacional del movimiento DevOps utilizada en la Sección 1.1 para referenciar el concepto del "muro de la confusión" entre desarrollo y operaciones).*

**[37]** Anthropic. (2024). *Claude 3.5 Sonnet: Intelligent, fast, and secure*. Recuperado de https://www.anthropic.com/news/claude-3-5-sonnet
*(Documentación oficial que respalda la optimización y el 'fine-tuning' específico de la familia Claude para flujos de trabajo agénticos y orquestación estructurada [Tool Calling], citado en la Sección 10.1.9).*

**[38]** OpenAI. (2024). *Hello GPT-4o*. Recuperado de https://openai.com/index/hello-gpt-4o/
*(Documentación técnica del modelo estándar de la industria, referenciado en la Sección 10.1.9 por sus capacidades nativas en interacción con herramientas externas y JSON Schema).*
