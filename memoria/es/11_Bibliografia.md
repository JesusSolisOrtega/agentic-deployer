# Capítulo 11. Bibliografía y Referencias

A continuación, se detalla la literatura académica, especificaciones técnicas y documentación oficial que fundamentan las decisiones arquitectónicas, metodológicas y algorítmicas expuestas en este Trabajo de Fin de Máster.

**[1]** Newman, S. (2015). *Building Microservices: Designing Fine-Grained Systems*. O'Reilly Media.
*(Referencia principal para la adopción de topologías distribuidas y el desacoplamiento de componentes frente a arquitecturas monolíticas).*

**[2]** Mell, P., & Grance, T. (2011). *The NIST Definition of Cloud Computing*. National Institute of Standards and Technology (NIST) Special Publication 800-145. https://doi.org/10.6028/NIST.SP.800-145
*(Definición académica del paradigma de computación en la nube que fundamenta el contexto tecnológico introductorio del TFM).*

**[3]** Docker Inc. (2024). *Docker Documentation: Container Runtime and Architecture*. Recuperado el 15/09/2026 de https://docs.docker.com/
*(Fundamentación técnica de la contenerización estandarizada de aplicaciones mencionada en el Estado del Arte).*

**[4]** Open Container Initiative (OCI). (2024). *OCI Image Format and Runtime Specification*. Recuperado el 15/09/2026 de https://opencontainers.org/
*(Estándar abierto de la industria para la interoperabilidad de imágenes de contenedores, previniendo el 'vendor lock-in' en orquestación).*

**[5]** The Kubernetes Authors. (2024). *Kubernetes Documentation: Concepts and Architecture*. Cloud Native Computing Foundation (CNCF). Recuperado el 15/09/2026 de https://kubernetes.io/docs/concepts/
*(Base teórica para la materialización física del código declarativo y el patrón de 'Golden Paths' aplicado en la orquestación de clústeres).*

**[6]** Kim, G., Humble, J., Debois, P., & Willis, J. (2016). *The DevOps Handbook: How to Create World-Class Agility, Reliability, and Security in Technology Organizations*. IT Revolution Press.
*(Referencia del movimiento DevOps utilizada en la Sección 1.1 respecto a la desconexión operativa entre desarrollo y operaciones).*

**[7]** Gartner. (2023). *Top Strategic Technology Trends for 2024: Platform Engineering*. Gartner Research.
*(Informe industrial utilizado para justificar el viraje del mercado hacia la Ingeniería de Plataformas y los Portales IDP referenciados en la Sección 1.1).*

**[8]** Spotify Engineering. (2020). *How We Use Golden Paths to Solve Fragmentation in our Software Ecosystem*. Recuperado el 15/09/2026 de https://engineering.atspotify.com/2020/08/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem/
*(Documentación técnica sobre la definición e implementación práctica del concepto de "Golden Path" en organizaciones tecnológicas).*

**[9]** Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. Proceedings of the International Conference on Learning Representations (ICLR). arXiv preprint arXiv:2210.03629. Recuperado el 15/09/2026 de https://arxiv.org/abs/2210.03629
*(Referencia metodológica para la formulación del bucle ReAct y la orquestación agéntica en el Capítulo 6).*

**[10]** OpenTofu Authors. (2024). *OpenTofu: An open-source tool for building, changing, and versioning infrastructure safely and efficiently*. The Linux Foundation. Recuperado el 15/09/2026 de https://opentofu.org/
*(Herramienta de Infraestructura como Código [IaC] de código abierto gobernada por la Linux Foundation, contemplada en la propuesta inicial del proyecto y analizada en las Secciones 1.2.2 y 4.4).*
**[11]** Siddiq, M. L., & Santos, J. C. (2026). *Treat LLM-Generated Terraform as Untrusted: An Exploratory Security Study and a Practitioner's Verification Workflow*. IEEE Software. https://doi.org/10.1109/MS.2026.3721790
*(Estudio formal que evidencia la inseguridad del código IaC generado por LLMs, justificando la necesidad de validadores algorítmicos deterministas).*

**[12]** Tarasova, N., Balp-Straffon, E., Iancheruk, A., Sielskyi, Y., Kozodoi, N., Byrne, L., Butler, J., Jiang, D., Czelej, M., Ang, A., Shah, Y., Blanco, R., & Ivanov, S. (2026). *Evaluating Language Models on Infrastructure-as-Code Development*. IEEE Cloud Summit. https://doi.org/10.1109/CloudSummit68932.2026.00021
*(Estudio empírico cuantitativo a gran escala que evalúa la precisión y las limitaciones de los LLMs en la generación de especificaciones de infraestructura como código [IaC], citado en la Sección 2.5.2).*

**[13]** Anthropic PBC. (2024). *Model Context Protocol (MCP) Specification*. GitHub Open Source Repository. Recuperado el 15/09/2026 de https://github.com/modelcontextprotocol/modelcontextprotocol
*(Estándar tecnológico empleado para resolver el problema del 'Vendor Lock-in' y aislar la definición de herramientas JSON-RPC, documentado en la Sección 6.1).*

**[14]** Hipp, D. R. (2024). *SQLite: A small, fast, reliable, self-contained, SQL database engine*. Recuperado el 15/09/2026 de https://www.sqlite.org/
*(Base de datos transaccional ACID embebida utilizada para la persistencia del estado de la Máquina de Estados Finita).*

**[15]** Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS), 30, 5998–6008. Recuperado de https://doi.org/10.48550/arXiv.1706.03762
*(Artículo original de la arquitectura Transformer, base estructural de los Modelos de Lenguaje de Gran Escala referenciados en este trabajo).*

**[16]** Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... & Amodei, D. (2020). *Language Models are Few-Shot Learners*. Advances in Neural Information Processing Systems (NeurIPS), 33, 1877–1901. Recuperado de https://doi.org/10.48550/arXiv.2005.14165
*(Estudio empírico que analiza las capacidades emergentes de generalización zero-shot y few-shot en LLMs, fundamentando el marco teórico de la Sección 2.1).*

**[17]** Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. Advances in Neural Information Processing Systems (NeurIPS), 35, 24824–24837. Recuperado de https://doi.org/10.48550/arXiv.2201.11903
*(Técnica de prompting que precede conceptualmente al paradigma ReAct, analizada en la Sección 2.1 como antecedente directo del razonamiento intercalado con acción).*

**[18]** AI Engineer Foundation. (2023). *Agent Protocol: A single common interface for communicating with agents*. Recuperado el 15/09/2026 de https://agentprotocol.ai/
*(Iniciativa comunitaria para estandarizar la interacción multi-agente).*

**[19]** Cockburn, A. (2005). *Hexagonal Architecture (Ports and Adapters Pattern)*. Alistair.cockburn.us. Recuperado el 15/09/2026 de https://alistair.cockburn.us/hexagonal-architecture/
*(Publicación de referencia para el diseño del núcleo hexagonal, el desacoplamiento de dependencias y el modelado del dominio en el Capítulo 5).*

**[20]** Malul, E., Meidan, Y., Mimran, D., Elovici, Y., & Shabtai, A. (2024). *GenKubeSec: LLM-Based Kubernetes Misconfiguration Detection, Localization, Reasoning, and Remediation*. Proceedings of the 40th Annual Computer Security Applications Conference (ACSAC). arXiv preprint arXiv:2405.19954. https://doi.org/10.48550/arXiv.2405.19954
*(Investigación académica que aborda la detección y resolución de malas configuraciones de seguridad en Kubernetes mediante LLMs, fundamentando la necesidad de validación estricta y supervisión HITL en la Sección 2.5.2).*

**[21]** Leppänen, M., Mäkinen, S., Pagels, M., Eloranta, V. P., Itkonen, J., Mäntylä, M. V., & Männistö, T. (2015). *The Highways and Country Roads to Continuous Deployment*. IEEE Software, 32(2), 64–72. https://doi.org/10.1109/MS.2015.50
*(Estudio empírico sobre la adopción de prácticas ChatOps e integración de herramientas conversacionales en pipelines CI/CD, citado en la Sección 2.5.2 como referencia de trabajo relacionado en la integración de asistentes en flujos DevOps).*

**[22]** Chase, H. (2022). *LangChain: Building applications with LLMs through composability*. GitHub Open Source Repository. Recuperado el 15/09/2026 de https://github.com/langchain-ai/langchain
*(Framework de orquestación de agentes LLM analizado en la Sección 2.5.3 como alternativa descartada por su acoplamiento al framework y la ausencia de protocolo de interoperabilidad estándar).*

**[23]** Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., ... & Wang, C. (2023). *AutoGen: Enabling next-generation LLM applications via multi-agent conversation*. arXiv preprint arXiv:2308.08155. Recuperado el 15/09/2026 de https://arxiv.org/abs/2308.08155
*(Framework multi-agente de Microsoft analizado en la Sección 2.5.3, cuya comparativa fundamenta la elección del estándar MCP frente a abstracciones propietarias de orquestación).*

**[24]** Pydantic / Colvin, S. (2024). *Pydantic V2: Data validation and settings management using Python type annotations (Rewritten in Rust)*. Recuperado el 15/09/2026 de https://docs.pydantic.dev/
*(Librería core utilizada para la validación estricta de invariantes y la protección contra la deriva de configuración en el núcleo hexagonal).*

**[25]** Richards, T. (2023). *Streamlit for Data Science: Create interactive data apps in Python* (2nd ed.). Packt Publishing.
*(Referencia metodológica para el diseño de la interfaz gráfica asíncrona tolerante a la ambigüedad empleada por los investigadores).*

**[26]** Ollama. (2024). *Ollama: Get up and running with large language models locally*. Recuperado el 15/09/2026 de https://ollama.com/
*(Servidor de inferencia local de código abierto que habilita la ejecución de modelos como Llama 3, Mistral y Qwen2.5 en infraestructura propia, garantizando la soberanía del dato institucional. Referenciado en las Secciones 3.3.3, 6.2.1 y 6.2.2).*

**[27]** OWASP Foundation. (2023). *OWASP Top 10 for Large Language Model Applications*. Open Worldwide Application Security Project. Recuperado el 15/09/2026 de https://owasp.org/www-project-top-10-for-large-language-model-applications/
*(Marco de referencia para la mitigación de vectores de ataque como la Inyección de Prompt [Prompt Injection], abordado en el Control de Cambios del Capítulo 4 y en el Caso de Estudio del Capítulo 9).*

**[28]** Brown, S. (2018). *The C4 model for visualising software architecture*. C4model.com. Recuperado el 15/09/2026 de https://c4model.com/
*(Metodología de modelado empleada en la Sección 5.2 para la segmentación del sistema en Contexto, Contenedores y Componentes).*

**[29]** Bass, L., Clements, P., & Kazman, R. (2012). *Software Architecture in Practice* (3rd ed.). Addison-Wesley Professional.
*(Literatura base para la formulación de tácticas de disponibilidad, latencia y resiliencia en la capa hexagonal).*

**[30]** Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley Professional.
*(Catálogo de patrones de diseño de software utilizado en la justificación de los patrones Factory y Adapter en la Sección 6.2).*

**[31]** Encode OSS. (2024). *HTTPX: A next-generation HTTP client for Python*. Recuperado el 15/09/2026 de https://www.python-httpx.org/
*(Librería utilizada en la implementación del `OllamaLLMClient` nativo para comunicación HTTP/1.1 y HTTP/2 sin dependencias de terceros en la API de Ollama, documentado en la Sección 6.2.1).*

**[32]** AXELOS. (2019). *ITIL Foundation: ITIL 4 Edition*. TSO (The Stationery Office).
*(Marco de gobernanza y buenas prácticas para la gestión de servicios TI, utilizado para justificar las responsabilidades legales y la implementación del patrón Human-In-The-Loop en el Capítulo 7).*

**[33]** Richardson, C. (2018). *Microservices Patterns: With examples in Java*. Manning Publications.
*(Referencia teórica extendida para los patrones de transaccionalidad, API Composition y observabilidad en arquitecturas distribuidas).*

**[34]** Cohn, M. (2009). *Succeeding with Agile: Software Development Using Scrum*. Addison-Wesley Professional.
*(Obra donde se propone el modelo conceptual de la Pirámide de Pruebas Automáticas, adaptado en el Capítulo 8 para estructurar el aseguramiento de calidad).*

**[35]** McCabe, T. J. (1976). *A Complexity Measure*. IEEE Transactions on Software Engineering, SE-2(4), 308-320. https://doi.org/10.1109/TSE.1976.233837
*(Artículo original sobre Complejidad Ciclomática, cuyo umbral estándar fundamenta el límite de `max-complexity = 15` adoptado en la canalización CI/CD, Sección 8.1.4).*

**[36]** Winters, T., Manshreck, T., & Wright, H. (2020). *Software Engineering at Google: Lessons Learned from Programming Over Time*. O'Reilly Media.
*(Manual de ingeniería citado en la Sección 8.1.4 para respaldar el umbral pragmático del 80% de cobertura de código frente a la exigencia del 100%).*

**[37]** MacIver, D. R., Hatfield-Dodds, Z., et al. (2019). *Hypothesis: A new approach to property-based testing*. Journal of Open Source Software, 4(43), 1891. https://doi.org/10.21105/joss.01891
*(Herramienta y fundamento teórico para la inyección de entropía y la minimización de fallos [Shrinking] documentada en la evaluación de QA del Capítulo 8).*

**[38]** Segura, S., Fraser, G., Sanchez, A. B., & Ruiz-Cortés, A. (2016). *A survey on metamorphic testing*. IEEE Transactions on Software Engineering, 42(9), 805-824. https://doi.org/10.1109/TSE.2016.2532875
*(Estudio de revisión sistemática utilizado para diseñar la evaluación mediante pruebas metamórficas ante el problema del oráculo en la Sección 8.4).*

**[39]** Mrkšić, N., Séaghdha, D. O., Wen, T. H., Thomson, B., & Young, S. (2017). *Neural Belief Tracker: Data-Driven Dialogue State Tracking*. Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL). Recuperado de https://arxiv.org/abs/1606.03777
*(Artículo sobre rastreo del estado del diálogo y extracción de entidades ("Slot-Filling"), citado en la Sección 9.4.3 como base teórica para el modelo de estado destilado).*

**[40]** LangChain Contributors. (2024). *Memory Management in LLM Applications (ConversationSummaryMemory & Context Distillation)*. LangChain Documentation. Recuperado el 15/09/2026 de https://python.langchain.com/v0.2/docs/concepts/#memory
*(Referencia industrial actual sobre técnicas arquitectónicas para la compresión del historial conversacional y la prevención de la dilución de atención en modelos acotados, mencionada en la Sección 9.4.3).*

**[41]** Snell, C., et al. (2022). *Learning by Distilling Context*. arXiv preprint arXiv:2209.15189. Recuperado de https://arxiv.org/abs/2209.15189
*(Literatura académica primaria que fundamenta teóricamente la técnica de Destilación de Contexto para Modelos de Lenguaje, citada en la Sección 9.4.3).*

**[42]** Wohlin, C., Runeson, P., Höst, M., Ohlsson, M. C., Regnell, B., & Wesslén, A. (2012). *Experimentation in Software Engineering*. Springer Science & Business Media.
*(Obra de referencia metodológica sobre investigación empírica en ingeniería del software y formalización de amenazas a la validez [interna, externa, constructo y conclusión], citada en la Sección 9.6).*

**[43]** Runeson, P., & Höst, M. (2009). *Guidelines for conducting and reporting case study research in software engineering*. Empirical Software Engineering, 14(2), 131-164. https://doi.org/10.1007/s10664-008-9102-8
*(Guía metodológica para el diseño, ejecución y reporte de estudios de caso y validación empírica en ingeniería del software, citada en la Sección 9.6).*

**[44]** OpenAI. (2024). *Hello GPT-4o*. Recuperado el 15/09/2026 de https://openai.com/index/hello-gpt-4o/
*(Documentación técnica del modelo estándar de la industria, referenciado en la Sección 10.1.9 por sus capacidades nativas en interacción con herramientas externas y JSON Schema).*

**[45]** Anthropic. (2024). *Introducing Claude 3.5 Sonnet*. Recuperado el 15/09/2026 de https://www.anthropic.com/news/claude-3-5-sonnet
*(Documentación oficial que respalda la optimización y el 'fine-tuning' específico de la familia Claude para flujos de trabajo agénticos y orquestación estructurada [Tool Calling], citado en la Sección 10.1.9).*

**[46]** Open Policy Agent (OPA). (2024). *OPA: Policy-based control for cloud native environments*. Cloud Native Computing Foundation (CNCF). Recuperado el 15/09/2026 de https://www.openpolicyagent.org/
*(Motor de Policy-as-Code propuesto como evolución del `SecurityContextValidator` en la planificación de Trabajo Futuro [Sección 10.3.2], permitiendo externalizar y actualizar reglas de validación sin redespliegue del backend).*

**[47]** Kyverno Authors. (2024). *Kyverno: Kubernetes Native Policy Management*. Cloud Native Computing Foundation (CNCF). Recuperado el 15/09/2026 de https://kyverno.io/
*(Alternativa nativa de Kubernetes a OPA para la gestión declarativa de políticas de seguridad como recursos del clúster. Referenciada en la Sección 10.3.2 como mecanismo de gobernanza para la evolución del sistema).*

