import logging
from typing import Dict
import requests
from json import JSONDecodeError

from .types import ObjectTypeDefinition


class BaseIntegrator:
    absolute_url = None
    secret_key = None
    header_rate_limit_attr = None

    def __init__(self, model=None):
        self.headers = self.set_headers()
        self.data = self.set_data(model)
        self.rate_limit = None

    def set_headers(self, *args, **kwargs):
        return {}

    def set_data(self, model):
        return model.dict() if model else None

    def validate_response(self, response):
        self.rate_limit = response.headers.get(self.header_rate_limit_attr) if self.header_rate_limit_attr else None
        try:
            json_data = response.json()
        except JSONDecodeError:
            logging.error(f"Invalid JSON: {response.content}")
            return None

        if response.status_code not in [200, 201, 204]:
            logging.info(f"Invalid response, status code: {response.status_code} {json_data}")
            return None

        response_content = json_data.get('id', json_data)
        logging.info(f"Operation is successful for object: {response_content}")
        return response_content


class CrudIntegrator(BaseIntegrator):

    def __init__(self, object_type, model=None):
        self.object_type: str = object_type
        self.object_types = self.set_object_types()
        self.data_constraints = self.set_data_constraints()
        super().__init__(model)
        self.validate_object()

    @staticmethod
    def set_object_types(*args, **kwargs) -> Dict[str, ObjectTypeDefinition]:
        return {}

    @staticmethod
    def set_data_constraints(*args, **kwargs):
        return {}

    def create_object(self, object_id):
        if not self.validate_data():
            return
        endpoint = f"{self.absolute_url}/{self.object_types[self.object_type]['endpoint']}"
        response = requests.post(endpoint, json=self.data, headers=self.headers)
        crud_model = self.object_types[self.object_type]['model']
        validated_response = self.validate_response(response)
        if response.status_code == 201:
            fields = crud_model._meta.fields
            crud_object_dict = {field.name: self.data[field.name] if field.name in self.data else '' for field in
                                fields}
            crud_object_dict['id'] = int(validated_response)
            crud_object_dict['object_id'] = object_id
            crud_model.objects.create(**crud_object_dict)
        return validated_response

    def update_object(self, object_id: int):
        crud_model = self.object_types[self.object_type]['model']
        crud_object = crud_model.objects.get(object_id=object_id)
        endpoint = f"{self.absolute_url}/{self.object_types[self.object_type]['endpoint']}/{crud_object.id}"
        response = requests.patch(endpoint, json=self.data, headers=self.headers)
        return self.validate_response(response)

    def delete_object(self, object_id: int = None):
        crud_model = self.object_types[self.object_type]['model']
        crud_object = crud_model.objects.get(object_id=object_id)
        endpoint = f"{self.absolute_url}/{self.object_types[self.object_type]['endpoint']}/{crud_object.id}"
        response = requests.delete(endpoint, json=self.headers)
        crud_object.delete()
        return self.validate_response(response)

    def validate_object(self):
        if self.object_type not in self.object_types:
            raise ValueError(
                f"Invalid object type: {self.object_type}. "
                f"Supported object types are: {list(self.object_types.keys())}")

    def validate_data(self):
        object_query_permission = self.data_constraints[self.object_type]
        for key, value in object_query_permission.items():
            if self.data[key] in value:
                return False