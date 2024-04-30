from argparse import ArgumentParser, Namespace
from openai.types.chat.chat_completion import ChatCompletion, Choice
import argparse
import os
import openai
import requests


class AIProvider:
    def __init__(self, base_url: str, model_name: str, api_key: str):
        self._base_url = base_url
        self._model_name = model_name
        self._api_key = api_key

    def generate_response(self, prompt: str):
        raise NotImplementedError("Subclasses must implement generate_response method")


class OpenAIProvider(AIProvider):
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


class LMStudioProvider(OpenAIProvider):
    def __init__(self, base_url: str, model_name: str, api_key: str):
        if base_url is None or base_url == '':
            self._base_url = 'http://localhost:1234/v1'

        super().__init__(self._base_url, model_name, api_key)


def get_ai_provider(provider_name: str, base_url: str, model_name: str, api_key: str) -> AIProvider:
    if provider_name == "openai":
        return OpenAIProvider(base_url=base_url, model_name=model_name, api_key=api_key)
    elif provider_name == "lmstudio":
        return LMStudioProvider(base_url=base_url, model_name=model_name, api_key=api_key)
    else:
        raise ValueError("Invalid AI provider name")


parser: ArgumentParser = ArgumentParser("aicommand")

parser.add_argument(
    "prompt", help="Your prompt.", type=str
)
parser.add_argument(
    "--provider", help="AI provider (openai or lmstudio).", type=str, default="openai"
)
parser.add_argument(
    "--base-url", help="Base URL for LM Studio server.", type=str
)
parser.add_argument(
    "--model", help="Name of the model to use (e.g., gpt-3, gpt-neo).", type=str
)
parser.add_argument(
    "--api-key", help="API key.", type=str
)

args = parser.parse_args()
print("Prompt:\n" + args.prompt.strip())

prompt = args.prompt.strip()
base_url: str = args.base_url
model_name: str = args.model
api_key: str = args.api_key

ai_provider: AIProvider = get_ai_provider(args.provider, base_url, model_name, api_key)

generated_text = ai_provider.generate_response(prompt)
print("Response:\n" + generated_text)
