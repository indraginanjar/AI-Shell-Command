from .ai_provider import AiProvider
from .open_ai_provider import OpenAiProvider
from .lm_studio_provider import LmStudioProvider

def get_ai_provider(provider_name: str, base_url: str, model_name: str, api_key: str) -> AiProvider:
    if provider_name == "openai":
        return OpenAiProvider(base_url=base_url, model_name=model_name, api_key=api_key)
    elif provider_name == "lmstudio":
        return LmStudioProvider(base_url=base_url, model_name=model_name, api_key=api_key)
    else:
        raise ValueError("Invalid AI provider name")


