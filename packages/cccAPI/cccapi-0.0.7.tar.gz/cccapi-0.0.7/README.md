# ccc_client

This package provides a simple, modular SDK for the CCC REST API.

## Features

* Automatically handles authentication and renewal
* Graceful error management
* Logically organized modules
* Easily maintained

## Installation

**Install using `pip`:**

```bash
pip install cccAPI 
```

**Install from source:**

```bash
git clone https://github.hpe.com/hpe/cccAPI.git
cd cccAPI
pip install -e .
```

## Quick Start

### Initialize the Client
- Install prerequisites: `pip install requests jsonschema`
- Simple usage 
```python
import json
from cccAPI import cccAPIClient
client = cccAPIClient("https://localhost:8000/cmu/v1", "root", "your-password")
```

### Example Usage

#### Get Nodes

```python
nodes = client.nodes.show_nodes()
print(json.dumps(nodes, indent=4))
```

#### Get specific Node

```python
#Specific node named BartC01n1-091
node = client.nodes.show_node("BartC01n1-091")
print(json.dumps(node, indent=4))
```

#### Get specific Node/fields 
- Allowed fields are: 

```python 
query_params = {"fields": "name,id,uuid,network.name,network.ipAddress,network.macAddress"}
specific_nodes=client.nodes.show_nodes(query_params)
print(json.dumps(specific_nodes, indent=4))
```

See `examples/test.py` for other test cases as implemented

## API Modules

| Module                | Description | User Guide Section | 
|----------------------|-------------|----------------------|
| `nodes`           | Node Operations
                      - Create/Delete/Update/List Nodes
                      - Add/Remove nodes in image/no-image/network group
                      - Get/Add actions/features of node 
                    |   Section 4.5  | 
| `image_groups`       | Image Group Operations |   Section 4.3 | 
| `network_groups`  | Network Group Operations |    Section 4.4 |
| `custom_groups` | Custom Group Operations |   Section 4.2 |
| `resource_features` | Resource Features | ------------- | 
| `image_capture_deployment`   | Image Capture Deployment | --------------- |
| `power_operation`            | Power operations |
| `application`          | application entrypoints, settings |  Section 4.1 | 
| `architecture`              | architecture  | --------------  |
| `management_cards`      | View network devices, interfaces, routes |  ------------- |
| `tasks`           | Tasks Operations |    Section 4.7     |
| `conn`           | Sessions Operations |  Section 4.6     |

## Building package

### Locally 
```
pip install .
```

or 
```
pip install pip-tools
pip-compile pyproject.toml  #This will produce requirements.txt
pip install -r requirements.txt
```

or 

```
curl -LsSf https://astral.sh/uv/install.sh | sh.
uv lock 
RUN uv pip install -e . --system
```
or
```bash
pip install build
# Build the package
python -m build
#Creates dist/ with tar.gz and .whl
```
### Publishing 
- Verify ~/.pypirc has PyPi token
```
pip install setuptools wheel twine
#This will create a dist directory containing the .tar.gz and .whl files for the package
python3 setup.py sdist bdist_wheel
#pip install dist/cccAPI-0.0.1-py3-none-any.whl
pip install twine
twine upload dist/*
```
## License

This project is license under the [MIT license](LICENSE).
