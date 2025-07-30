import requests
from .base_model_client import BaseDockerModelClient


class BaseTransformer(BaseDockerModelClient):
    """Abstract base class for sklearn-like transformers."""

    def transform(self, X, y=None, dockerfile_dir="."):
        """Transform the training data"""
        try:
            self.ensure_container_running()
            payload = {

            }
            response = requests.post(f"{self.api_url}/transform", json=payload)
            response.raise_for_status()
            return response.json()
        finally:
            self.stop_container()
