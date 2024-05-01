from .ai_provider import AiProvider
import os
import openai


class OpenAiProvider(AiProvider):
    def __init__(self, base_url: str, model_name: str, api_key: str):
        if base_url is None or base_url == '':
            self._base_url = 'https://api.openai.com/v1'

        if model_name is None or model_name == '':
            self._model_name = "gpt-3.5-turbo"

        if api_key is None or api_key == '':
            self._api_key = os.environ.get("AI_SHELL_COMMAND_OPENAI_API_KEY")

        super().__init__(self._base_url, self._model_name, self._api_key)

    def generate_response(self, prompt: str):
        client: openai.Client = openai.Client(api_key=self._api_key, base_url=self._base_url)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self._model_name,
        )

        choice = chat_completion.choices[0]
        return choice.message.content.strip()
