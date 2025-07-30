# 🔧 Federated Learning Clinical Safety Server SDK

This is the documentation for the Federated Learning Clinical Safety Dashboard SDK! This project provides a package for interacting with the [Federated Learning Clinical Safety Dashboard Server](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-server) in a type-safe and easy manner.


[![CI](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/ci.yml)

[![SDK ↔ Server Integration](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/integration.yml/badge.svg)](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk/actions/workflows/integration.yml)

## Using the SDK

The package is [available from PyPi](https://pypi.org/project/federated-learning-clinical-safety-sdk/).

### Installation

```bash
pip install federated-learning-clinical-safety-sdk
```

### 🚀 Quickstart code

```
from api_sdk.client import APIClient
from api_sdk.models import FlModel

# 1. Initialize
BASE_URL = "http://localhost:8000/api"       # i.e. vht-dev.shef.ac.uk/api
TOKEN    = "your_api_token_here"             # create a machine account with create_uploader <username>

client = APIClient(BASE_URL, TOKEN)

# 2. List all federated models
models = client.list_models()
for m in models:
    print(f"{m.id}: {m.name} ({m.accuracy*100:.1f}% accuracy)")

# 3. Fetch a single model by ID
model = client.get_model(model_id=1)
print(model)

# 4. Create a new model
new = FlModel(
    name="MyModel",
    accuracy=0.88,
    generalisability=0.82,
    security=0.75
)
created = client.create_model(new)
print(f"Created model ID = {created.id}")
```

## Development
### Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.10+
* Poetry

#### Installing poetry

Windows NT
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Then add to path:

```
%USERPROFILE%\AppData\Roaming\pypoetry\venv\Scripts
```

Linux/MacOS/Unix-like systems:
```bash
pipx install poetry
```

### Publishing new versions

This repo is set up with Continuous Deployment to automatically deploy new packages to PyPi.

To deploy a new version, do the following.

1. Bump the package version

```bash
poetry version patch
```

2. Create a matching git tag

```bash
git tag v<version number (i.e. 0.1.1)>
```

3. Push the tag to GitHub

```bash
git push origin v<version number from step 2 (i.e. 0.1.1)>
```