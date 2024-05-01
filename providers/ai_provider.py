class AiProvider:
    def __init__(self, base_url: str, model_name: str, api_key: str):
        self._base_url = base_url
        self._model_name = model_name
        self._api_key = api_key

    def generate_response(self, prompt: str):
        raise NotImplementedError("Subclasses must implement generate_response method")
