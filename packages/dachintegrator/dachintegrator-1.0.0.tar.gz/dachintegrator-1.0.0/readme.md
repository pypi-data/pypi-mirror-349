# 🔌 Integrator System
This module provides a lightweight abstraction for integrating external CRUD-based APIs with your Django models. It defines a base Integrator class and a specialized CrudIntegrator class to manage create, update, and delete operations while mapping responses back to local Django models.

## 📦 Classes Overview
### BaseIntegrator
A base class designed to prepare data, configure headers, and validate HTTP responses.

#### ✅ Responsibilities:
Initialize headers, data, and rate_limit attributes.

Provide a validate_response() method that:

Parses the HTTP response JSON.

Logs response success or failure.

Extracts and returns the 'id' from the JSON (or full content fallback).

Convert a model-like object to dictionary using model.dict().

#### 🔧 Methods:
set_headers(): Override to define custom HTTP headers.

set_data(model): Prepares the model payload as a dictionary.

validate_response(response): Handles status code and JSON parsing for HTTP responses.

### CrudIntegrator
A subclass of BaseIntegrator that specializes in full CRUD operations for Django models via external APIs.

#### ✅ Responsibilities:
Maps Django model classes to remote API endpoints.

Sends HTTP requests to external systems.

Writes responses back to local Django models (.objects.create(...), etc.).

#### 🧠 Requires:
A defined dictionary of object_types, mapping string keys to:

model: A Django model class

endpoint: A relative API path

A data_constraints structure to restrict invalid payloads (e.g. forbidden values).

#### 🔧 Methods:
create_object(object_id):
Sends a POST request to the API. If successful, creates a corresponding object in the local DB.

update_object(object_id: int):
Sends a PATCH request to update an existing record, found by object_id.

delete_object(object_id: int):
Sends a DELETE request and deletes the local object after remote deletion.

validate_object():
Ensures object_type exists in the object_types mapping.

validate_data():
Enforces value constraints from data_constraints before proceeding with remote API operations.

#### 🧱 Type Definitions
Located in types.py (or definitions.py), used to enforce type safety:

python
Copy
Edit
from typing import Protocol, TypedDict, Type, Any
from django.db.models.manager import Manager

class DjangoModelProtocol(Protocol):
    objects: Manager
    _meta: Any

class ObjectTypeDefinition(TypedDict):
    model: Type[DjangoModelProtocol]
    endpoint: str
#### 🧪 Example Usage
python
Copy
Edit
class ProductModel(models.Model):
    ...

class MyIntegrator(CrudIntegrator):
    @staticmethod
    def set_object_types():
        return {
            "product": {
                "model": ProductModel,
                "endpoint": "products"
            }
        }

    @staticmethod
    def set_data_constraints():
        return {
            "product": {"status": ["invalid", "archived"]}
        }
## 🚨 Notes
This system assumes each remote object has an id returned in its API response.

Make sure your models are compatible with the fields being returned or used.

Designed to be extended and customized per integration.

