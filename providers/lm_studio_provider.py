from .open_ai_provider import OpenAiProvider


class LmStudioProvider(OpenAiProvider):
    def __init__(self, base_url: str, model_name: str, api_key: str):
        if base_url is None or base_url == '':
            self._base_url = 'http://localhost:1234/v1'

        super().__init__(self._base_url, model_name, api_key)
