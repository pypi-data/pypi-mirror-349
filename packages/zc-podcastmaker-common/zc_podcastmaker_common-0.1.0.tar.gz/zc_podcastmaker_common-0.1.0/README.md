# zc-podcastmaker-common

Common utilities library for PodcastMaker components.

## Overview

This package provides shared functionality for all PodcastMaker components, including:

- Configuration management (via `config_manager`)
- Object storage client (via `object_storage_client`)
- Generative LLM client (via `generative_llm_client`)
- Message bus client (via `message_bus_client`)

## Installation

Install the package using uv:

```bash
uv pip install zc-podcastmaker-common
```

## Usage

### Configuration Manager

```python
from zc_podcastmaker_common.config_manager import get_config_value, get_secret_value

# Get configuration values
api_url = get_config_value("api.url", "http://default-api.example.com")

# Get secret values
api_key = get_secret_value("api.key")
```

### Object Storage Client

```python
from zc_podcastmaker_common.object_storage_client import upload_file, download_file

# Upload a file
upload_file("my-bucket", "path/to/object.txt", "/local/path/to/file.txt")

# Download a file
download_file("my-bucket", "path/to/object.txt", "/local/download/path.txt")
```

### Generative LLM Client

```python
from zc_podcastmaker_common.generative_llm_client import get_text_completion

# Get a text completion
response = get_text_completion(
    "Summarize the following text: ...",
    model_alias="claude_default"
)
```

### Message Bus Client

```python
from zc_podcastmaker_common.message_bus_client import publish_message, MessageConsumer

# Publish a message
publish_message("my_queue", {"key": "value"})

# Consume messages
def handle_message(message):
    print(f"Received message: {message}")
    return True  # Message processed successfully

# Using the context manager
with MessageConsumer("my_queue") as consumer:
    consumer.consume(handle_message)
```

## Configuration Requirements

This library expects configuration and secrets to be available in specific locations:

- Configuration files: `/vault/configs/`
- Secret files: `/vault/secrets/`

These paths are populated by a Vault Agent sidecar running alongside the application container.

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/oadiazp/podcast_ai_common.git
cd podcast_ai_common

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
pytest
```

## Código y estilo

Para mantener la calidad y consistencia del código, este proyecto utiliza **Ruff** como herramienta única de linting y formateo (reemplazando a black, isort y flake8).

### Cómo usar Ruff

Instala las dependencias de desarrollo con uv:

```bash
uv pip install -e .[dev]
```

Revisa y corrige el estilo de código localmente:

```bash
# Formatear y corregir automáticamente
ruff format src tests

# Verificar errores de estilo y sintaxis
ruff check src tests
```

Para verificar el código sin modificar archivos (modo solo chequeo):

```bash
ruff format --check src tests
ruff check src tests
```

### Pre-commit hooks

Este proyecto utiliza pre-commit para ejecutar verificaciones automáticas antes de cada commit. Los hooks configurados incluyen:

- Formateo con Ruff
- Linting con Ruff
- Corrección de finales de línea
- Eliminación de espacios en blanco al final de las líneas
- Verificación de archivos YAML y TOML

Para instalar los hooks:

```bash
# Asegúrate de tener pre-commit instalado
uv pip install -e ".[dev]"

# Instala los hooks en el repositorio local
pre-commit install
```

Una vez instalados, los hooks se ejecutarán automáticamente en cada commit. También puedes ejecutarlos manualmente:

```bash
# Ejecutar en todos los archivos
pre-commit run --all-files

# Ejecutar un hook específico
pre-commit run ruff --all-files
```

Estas comprobaciones también se ejecutan automáticamente en el pipeline de CI.

## Release Process

This project uses [Python Semantic Release](https://python-semantic-release.readthedocs.io/) for automated versioning and package publishing.

### How Releases Work

1. Commits to the `main` branch are automatically analyzed for conventional commit messages
2. Based on these messages, a new version is determined following semantic versioning rules:
   - `fix:` commits trigger a patch version bump (e.g., 1.0.0 → 1.0.1)
   - `feat:` commits trigger a minor version bump (e.g., 1.0.0 → 1.1.0)
   - `feat!:` or `fix!:` commits (or any with a breaking change footer) trigger a major version bump (e.g., 1.0.0 → 2.0.0)
3. A new GitHub release is created with automatically generated release notes
4. The package is built and published to PyPI

### Commit Message Format

For automated releases to work properly, commit messages should follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Where `<type>` is one of:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Changes that don't affect code functionality (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or correcting tests
- `chore`: Changes to the build process, tooling, etc.

Examples:
```
feat(config): add support for environment variables
fix(storage): handle file not found errors properly
docs: update installation instructions
```

### Manual Release

To manually trigger a release (for administrators):

1. Go to the GitHub Actions tab in the repository
2. Select the "Release" workflow
3. Click "Run workflow"
4. Select the desired release type (patch, minor, or major)
5. Click "Run workflow"

This will trigger the release process with the specified version bump.
