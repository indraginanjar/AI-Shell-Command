from argparse import ArgumentParser, Namespace
from subprocess import CompletedProcess
import argparse
import os
import subprocess
from providers.ai_provider import AiProvider
from providers import get_ai_provider


parser: ArgumentParser = argparse.ArgumentParser("aicommand")

parser.add_argument(
    "prompt",
    help="Prompt describing task/command to produce and execute.",
    type=str
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

parser.add_argument(
    "--executor",
    help="Application/executor for executing the generated command",
    type=str,
)

args: Namespace = parser.parse_args()
print("Prompt:\n" + args.prompt.strip())

executor: str = "powershell"

if os.name != "nt":
    executor = "pwsh"

customExecutor: str = os.environ.get("AI_COMMAND_EXECUTOR")

if customExecutor is not None:
    executor = customExecutor

if args.executor is not None:
    executor = args.executor

prompt: str = (
    "Create a "
    + executor
    + " script. Answer without giving explanation, just pure script."
    + " Do not mark the produced script as a code."
)
prompt += '"""' + args.prompt.strip() + '"""'

if executor == "python":
    prompt += " Do not use new line as statement delimiter,"
    prompt += " use semicolon instead. Remove all new line,"
    prompt += " make all statements fit on a single line"
elif executor == "bash" or executor == "zsh" or executor == "sh":
    prompt += " Do not use shebang."
    prompt += " Do not use new line as statement delimiter,"
    prompt += " use semicolon instead. Remove all new line,"
    prompt += " make all statements fit on a single line"

base_url: str = args.base_url
model_name: str = args.model
api_key: str = args.api_key

ai_provider: AiProvider = get_ai_provider(
    args.provider, base_url, model_name, api_key
)

generated_text = ai_provider.generate_response(prompt)

print("Generated command:\n" + generated_text)

confirm: str = "Do you want to execute the generated command? (y)es/(n)o: "
user_input: str = input(confirm)
lowered_user_input: str = user_input.lower()

user_choose_to_execute: bool = lowered_user_input == "yes"
user_choose_to_execute |= lowered_user_input == "y"

if user_choose_to_execute:
    print("Executing generated command ...")

    if executor == "powershell" or executor == "pwsh":
        result: CompletedProcess[bytes] = subprocess.run(
            [executor, "-Command", generated_text], stdout=subprocess.PIPE
        )
    elif executor == "bash":
        result: CompletedProcess[bytes] = subprocess.run(
            [executor, "-c", '"' + generated_text + '"'],
            stdout=subprocess.PIPE
        )
    elif executor == "zsh":
        result: CompletedProcess[bytes] = subprocess.run(
            [executor, "-c", '"' + generated_text + '"'],
            stdout=subprocess.PIPE
        )
    elif executor == "python":
        result: CompletedProcess[bytes] = subprocess.run(
            [executor, "-c", '"' + generated_text + '"'],
            stdout=subprocess.PIPE
        )
        result_text = exec(generated_text)
    elif executor == "cmd":
        result: CompletedProcess[bytes] = subprocess.run(
            [executor, "/c", generated_text], stdout=subprocess.PIPE
        )
    else:
        result: CompletedProcess[bytes] = subprocess.run(
            ["sh", "-c", '"' + generated_text + '"'],
            stdout=subprocess.PIPE
        )

    print(result.stdout.decode("utf-8"))

    if result.stderr is not None:
        print(result.stderr.decode("utf-8"))
else:
    print("You choose not to execute the generated command.")
