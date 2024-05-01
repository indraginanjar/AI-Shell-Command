from argparse import ArgumentParser
from providers.ai_provider import AiProvider
from providers import get_ai_provider


parser: ArgumentParser = ArgumentParser("aicommand")

parser.add_argument(
    "prompt", help="Your prompt.", type=str
)
parser.add_argument(
    "--provider",
    help="AI provider (openai or lmstudio).",
    type=str, default="openai"
)
parser.add_argument(
    "--base-url",
    help="AI Provider's base URL.",
    type=str
)
parser.add_argument(
    "--model",
    help="Name of the model to use (e.g., gpt-3, gpt-neo).",
    type=str
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

ai_provider: AiProvider = get_ai_provider(
    args.provider, base_url, model_name, api_key
)

generated_text = ai_provider.generate_response(prompt)
print("Response:\n" + generated_text)
