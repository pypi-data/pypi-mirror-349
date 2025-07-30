**PRD: Componente `PodcastMakerCommonLib` (Librería Común de Utilidades)**

**1. Overview**

`PodcastMakerCommonLib` es una librería interna de Python, diseñada para ser una dependencia compartida por todos los componentes de servicio del sistema PodcastMaker. Se distribuirá como el paquete Python **`zc-podcastmaker-common`** desde un repositorio PyPI dedicado en **`nexus.zczoft.com`**.

Su propósito es encapsular y centralizar la lógica común para:
* Interactuar con el servicio de almacenamiento de objetos (a través del módulo `object_storage_client`).
* Acceder a configuraciones de aplicación y secretos de manera estandarizada desde un volumen `tmpfs` (poblado por un Vault Agent sidecar), a través del módulo `config_manager`.
* Realizar llamadas a APIs de Modelos de Lenguaje Grandes (LLM) generativos (a través del módulo `generative_llm_client`).
* Interactuar con el bus de mensajes (a través del módulo `message_bus_client`).

Al proporcionar interfaces de alto nivel y bien probadas para estas operaciones comunes, `PodcastMakerCommonLib` busca reducir la duplicación de código, asegurar la consistencia, mejorar la mantenibilidad y acelerar el desarrollo de los componentes individuales del PodcastMaker. Resuelve el problema de la repetición de código "boilerplate" y la inconsistencia en las interacciones con servicios comunes, adaptándose a una infraestructura gestionada con Vault, Ansible y Docker Swarm. Su ciclo de vida, desde las pruebas hasta el empaquetado y la distribución, será gestionado mediante Integración Continua (CI/CD) desde GitHub Actions.

**2. Core Features**

* **Gestor de Configuración y Secretos (desde `tmpfs`):**
    * *Módulo:* `config_manager`
    * *What it does:* Proporciona un mecanismo unificado para que los componentes lean su configuración de aplicación y secretos. Estos datos son previamente materializados en archivos dentro de un volumen `tmpfs` por un Vault Agent sidecar que se ejecuta junto al contenedor de la aplicación.
    * *Why it's important:* Desacopla los componentes de la necesidad de ser clientes directos de Vault, estandariza el acceso a la configuración de forma segura y eficiente dentro del entorno del contenedor, y se alinea con la estrategia de entrega de secretos mediante Vault Agent.
    * *How it works at a high level:* Ofrece funciones como `get_config_value(key_name: str, default_value: any = None) -> any` y `get_secret_value(key_name: str) -> str`. Estas funciones leen de rutas de archivo predefinidas o convencionales dentro del `tmpfs` (ej. `/vault/configs/config.json` y `/vault/secrets/secrets.json`, o archivos individuales por clave como `/vault/secrets/api_key_anthropic`). La estructura exacta en `tmpfs` será definida por la configuración del Vault Agent.
* **Cliente de Almacenamiento de Objetos Abstraído:**
    * *Módulo:* `object_storage_client`
    * *What it does:* Proporciona funciones simplificadas para interactuar con un servicio de almacenamiento de objetos compatible con la API S3 (como MinIO). La configuración del servicio de almacenamiento (ej. endpoint S3, región, y credenciales de acceso) se obtiene a través del `config_manager`.
    * *Why it's important:* Centraliza y estandariza la lógica de interacción con el almacenamiento de objetos, permitiendo cambiar la implementación S3 subyacente con un impacto mínimo en los componentes consumidores.
    * *How it works at a high level:* Internamente utiliza `boto3` (o una librería S3 compatible). Ofrece funciones como `upload_file(bucket_name: str, object_key: str, file_path: str, extra_args: dict = None)`, `download_file(bucket_name: str, object_key: str, download_path: str)`, y potencialmente `upload_bytes(bucket_name: str, object_key: str, data_bytes: bytes, extra_args: dict = None)`. Maneja reintentos básicos y errores comunes.
* **Cliente de LLM Generativo Abstraído:**
    * *Módulo:* `generative_llm_client`
    * *What it does:* Ofrece una interfaz simplificada para realizar llamadas a modelos de lenguaje generativos (inicialmente enfocado en Anthropic Claude). La configuración específica del modelo a invocar (ej. API key, identificador del modelo como "claude_default") se obtiene a través del `config_manager` utilizando un alias de modelo.
    * *Why it's important:* Facilita la interacción con LLMs, permite cambiar o añadir modelos con reconfiguración (gestionada en Vault y entregada vía `tmpfs`) y centraliza el manejo de la comunicación con la API del LLM. No contiene lógica de prompts específica de cada componente.
    * *How it works at a high level:* Envuelve la librería cliente del proveedor de LLM (ej. Anthropic). Proporciona una función como `get_text_completion(prompt: str, model_alias: str, params: dict = None) -> str`. El `model_alias` se usa para que el `config_manager` recupere la configuración de ese modelo (ej. API key, nombre del modelo específico de Claude).
* **Utilidades para el Bus de Mensajes:**
    * *Módulo:* `message_bus_client`
    * *What it does:* Proporciona funciones helper para publicar mensajes en una cola y para configurar un consumidor de mensajes de manera estandarizada. La configuración del broker del bus de mensajes (dirección, credenciales si son necesarias, nombres de colas base o prefijos) se obtiene del `config_manager`.
    * *Why it's important:* Simplifica y estandariza la interacción con el bus de mensajes (ej. RabbitMQ, SQS), reduciendo código repetitivo en los componentes.
    * *How it works at a high level:* Envuelve la librería cliente del bus de mensajes elegida. Ofrece funciones como `publish_message(queue_name: str, message_body: dict, exchange_name: str = '')` y una clase base o decorador para `create_consumer(queue_name: str, message_handler_callback: callable, prefetch_count: int = 1)`. Maneja serialización JSON y confirmaciones (ACK/NACK) básicas.

**3. Technical Architecture**

* **System Components:**
    * La librería `PodcastMakerCommonLib` es un paquete Python instalable, con el nombre **`zc-podcastmaker-common`**.
* **Data Models:**
    * Puede definir modelos Pydantic para las estructuras de configuración que espera leer de `tmpfs` o para los cuerpos de los mensajes (si se estandarizan y comparten).
* **APIs and Integrations (Lo que *proporciona* a otros componentes):**
    * Módulo `config_manager`: Funciones `get_config_value(key, default=None)`, `get_secret_value(key)`.
    * Módulo `object_storage_client`: Funciones `upload_file(...)`, `download_file(...)`, `upload_bytes(...)`.
    * Módulo `generative_llm_client`: Función `get_text_completion(prompt, model_alias, params=None)`.
    * Módulo `message_bus_client`: Funciones `publish_message(...)`, `create_consumer(...)`.
* **APIs and Integrations (Lo que *usa* internamente):**
    * `boto3` (para la implementación S3 de `object_storage_client`).
    * Librería cliente de Anthropic (para la implementación inicial de `generative_llm_client`).
    * Librería cliente del bus de mensajes (ej. `pika` si es RabbitMQ, o `boto3` si es SQS).
    * Librerías estándar de Python para manejo de archivos (para leer de `tmpfs`), JSON, logging.
    * Pydantic (recomendado para modelos de configuración y validación).
* **Infrastructure Requirements (Para desarrollar y usar la librería):**
    * **Repositorio Git en GitHub:** Para el código fuente de la librería y la integración con GitHub Actions.
    * **GitHub Actions:** Para la Integración Continua (ejecución de pruebas, linters) y Despliegue Continuo (empaquetado y publicación de la librería).
    * **Sonatype Nexus en `nexus.zczoft.com`:**
        * **Repositorio PyPI (hosted, ej. `pypi-internal`):** Para alojar las versiones empaquetadas de **`zc-podcastmaker-common`**.
        * **Repositorio PyPI (proxy):** (Recomendado) Para cachear dependencias públicas de PyPI.
    * Se utilizará **`uv`** para la gestión de dependencias, entornos virtuales (`uv venv`), y empaquetado (`uv build`) dentro del pipeline de GitHub Actions y para el desarrollo local de la librería.
    * Para pruebas: Entornos que puedan simular la presencia de archivos en `tmpfs` (poblados por un mock de Vault Agent o manualmente), y acceso mockeado/real a servicios de almacenamiento, LLMs, y bus de mensajes.
    * Los componentes que usan esta librería se desplegarán en **Docker Swarm**, con un Vault Agent sidecar proveyendo configuraciones/secretos a `tmpfs`. Esta estrategia de Vault será gestionada por **Ansible**.

**4. Development Roadmap (MVP Requirements)**

* **Fase 1: Diseño y Estructura Fundamental de la Librería**
    * 1.1. Crear el repositorio en GitHub y la estructura del paquete Python para `PodcastMakerCommonLib` (configurar `pyproject.toml` para gestión con **`uv`** y nombre de paquete **`zc-podcastmaker-common`**).
    * 1.2. Establecer el sistema de pruebas (ej. `pytest` con plugins como `pytest-mock`).
    * 1.3. **Módulo `config_manager`:**
        * Implementar `get_config_value(key_path: str, default_value=None)` y `get_secret_value(key_path: str)` que lean de rutas de archivo convencionales en `tmpfs` (ej. `/vault/configs/<key_path>`, `/vault/secrets/<key_path>`).
        * Definir la convención de rutas y formatos de archivo (ej. JSON, archivos de texto simple) esperados en `tmpfs`.
        * Pruebas unitarias (mockeando el sistema de archivos `pathlib`).
    * 1.4. Definir las interfaces públicas iniciales (firmas de funciones y clases) para los otros módulos, utilizando type hints.
* **Fase 2: Implementación del `object_storage_client`**
    * 2.1. Implementar las funciones principales (ej. `upload_file`, `download_file`), obteniendo la configuración necesaria (endpoint S3, credenciales) del `config_manager`.
    * 2.2. Incluir manejo de excepciones comunes de `boto3` y configuración de reintentos básicos.
    * 2.3. Escribir pruebas unitarias exhaustivas, mockeando `boto3` y el `config_manager`.
* **Fase 3: Implementación del `generative_llm_client`**
    * 3.1. Implementar `get_text_completion(prompt: str, model_alias: str, params: dict = None)`, obteniendo la configuración del modelo (API key, identificador de modelo específico de Claude, etc.) del `config_manager` usando `model_alias`.
    * 3.2. Incluir manejo de excepciones comunes de la API del proveedor LLM y configuración de reintentos básicos.
    * 3.3. Escribir pruebas unitarias, mockeando la API del proveedor LLM y el `config_manager`.
* **Fase 4: Implementación del `message_bus_client`**
    * 4.1. Implementar `publish_message(queue_name: str, message_body: dict, ...)`, obteniendo la configuración del broker del bus del `config_manager`.
    * 4.2. Implementar un helper o clase base `create_consumer(queue_name: str, message_handler_callback: callable, ...)`, obteniendo la configuración del bus del `config_manager`.
    * 4.3. Escribir pruebas unitarias, mockeando la librería del bus de mensajes y el `config_manager`.
* **Fase 5: Configuración de CI/CD, Empaquetado, Documentación y Primer Release**
    * 5.1. **Configurar el pipeline de GitHub Actions:**
        * Workflow para ejecutar pruebas y linters en cada push/pull request.
        * Workflow para construir el paquete Python **`zc-podcastmaker-common`** (con **`uv build`**) y publicarlo en el repositorio PyPI de `nexus.zczoft.com` (ej. `https://nexus.zczoft.com/repository/pypi-internal/`) cuando se cree un nuevo tag de versión. Esto requerirá configurar secretos en GitHub Actions con credenciales para `nexus.zczoft.com`.
    * 5.2. Asegurar que `pyproject.toml` está correctamente configurado para el nombre del paquete `zc-podcastmaker-common` y sus dependencias.
    * 5.3. Documentar la API pública de la librería (ej. con docstrings conformes a Sphinx y generación automática de documentación). Detallar la convención de cómo y dónde la librería espera encontrar los archivos de configuración/secretos en `tmpfs` que el Vault Agent debe proveer.
    * 5.4. Realizar un primer release (ej. v0.1.0) de **`zc-podcastmaker-common`** a `nexus.zczoft.com` a través del pipeline de GitHub Actions.
    * 5.5. Crear un `README.md` para la librería con instrucciones de instalación (ej. **`uv pip install zc-podcastmaker-common --index-url https://nexus.zczoft.com/repository/pypi-internal/simple`**), uso básico, y prerrequisitos sobre la configuración del Vault Agent y `tmpfs`.

**5. Risks and Mitigations**

* **Riesgo:** La convención de rutas y formatos de archivo en `tmpfs` entre el Vault Agent (configurado por Ansible) y `PodcastMakerCommonLib` es frágil o se desincroniza.
    * **Mitigación:** Documentación exhaustiva y compartida entre el equipo de Ansible y los desarrolladores de la librería/componentes. Contratos claros (posiblemente esquemas JSON para los archivos en `tmpfs` si son complejos). Versionar esta convención si es necesario. Considerar una configuración inicial en `PodcastMakerCommonLib` (leída de `tmpfs`) que defina estas rutas base, si la estructura es muy dinámica.
* **Riesgo:** Errores en la configuración del Vault Agent sidecar (ej. plantillas incorrectas, permisos de Vault) impiden que `PodcastMakerCommonLib` encuentre los archivos necesarios en `tmpfs` o que estos tengan el contenido correcto.
    * **Mitigación:** Pruebas de integración robustas que incluyan el despliegue del Vault Agent y la verificación de los archivos en `tmpfs`. Logging claro en `PodcastMakerCommonLib` si no encuentra los archivos esperados o si su contenido no es el esperado.
* **Riesgo:** La librería se vuelve demasiado dependiente de una estructura específica de `tmpfs` impuesta por una implementación particular de Vault Agent, limitando la flexibilidad si la estrategia de entrega de secretos cambia.
    * **Mitigación:** Diseñar el `config_manager` con interfaces claras. Aunque la implementación inicial lea de `tmpfs`, la interfaz podría permitir en el futuro otros "backends" (ej. leer de variables de entorno como fallback para desarrollo local sin agente, o incluso un cliente Vault directo si el sidecar no está disponible en algún entorno).
* **Riesgo:** La gestión de versiones de `PodcastMakerCommonLib` y la actualización de dependencias en los componentes consumidores se vuelve una carga.
    * **Mitigación:** Usar versionado semántico estricto (SemVer: MAJOR.MINOR.PATCH). Tener un buen proceso de CI/CD para la librería que incluya pruebas automáticas y publicación al índice privado. Comunicar claramente los "breaking changes" en los changelogs. Fomentar actualizaciones frecuentes y planificadas en los componentes.
* **Riesgo:** Errores en la lógica de `PodcastMakerCommonLib` afectan a múltiples componentes.
    * **Mitigación:** Pruebas unitarias y de integración exhaustivas para la librería. Despliegues canary o por fases de nuevas versiones de la librería si el sistema es muy crítico y el impacto de un error es alto.
* **Riesgo:** La abstracción proporcionada por la librería (especialmente para el `generative_llm_client`) oculta detalles importantes de los servicios subyacentes que podrían ser necesarios para optimizaciones específicas o debugging avanzado.
    * **Mitigación:** Proveer mecanismos para pasar parámetros opcionales ("passthrough" `params`) a las implementaciones subyacentes si es necesario. Asegurar que la librería proporciona suficiente logging y telemetría. Documentar las limitaciones de la abstracción.
* **Riesgo:** La librería no se adopta correctamente o de manera consistente por los equipos de desarrollo de los componentes.
    * **Mitigación:** Buena documentación, ejemplos claros de uso, y comunicación activa con los equipos. Involucrarlos en el diseño de las interfaces de la librería. Proveer fragmentos de código o plantillas para el uso común.
* **Riesgo:** Fallos en el pipeline de CI/CD de GitHub Actions impiden la distribución de nuevas versiones de **`zc-podcastmaker-common`** a `nexus.zczoft.com`.
    * **Mitigación:** Pipeline robusto y bien probado. Monitorización del pipeline. Plan de contingencia para publicación manual si es estrictamente necesario.
* **Riesgo:** Problemas de seguridad con los tokens de acceso a `nexus.zczoft.com` para la publicación automática desde GitHub Actions.
    * **Mitigación:** Usar tokens de API con permisos limitados (scoped tokens) para Nexus, específicos para la publicación. Almacenarlos de forma segura como secretos en GitHub Actions. Rotar tokens periódicamente.
* **Riesgo Adicional por Abstracción (en `generative_llm_client`):** Si la abstracción (ej. `get_text_completion`) es demasiado genérica, puede ser difícil de usar para LLMs muy diferentes o puede ocultar funcionalidades importantes del modelo específico.
    * **Mitigación:** Empezar con un nivel de abstracción que sirva bien para el caso de uso inicial (Claude). Permitir pasar parámetros específicos del modelo a través de un diccionario `params`. Estar preparado para refinar o añadir funciones más especializadas en la librería si es necesario, en lugar de hacer una única función demasiado compleja.
