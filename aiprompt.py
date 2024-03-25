from argparse import ArgumentParser, Namespace
from openai.types.chat.chat_completion import ChatCompletion, Choice
from subprocess import CompletedProcess
import argparse
import openai
import os

client = openai.Client(
    api_key=os.environ.get("AI_COMMAND_OPENAI_API_KEY"),
)

parser: ArgumentParser = argparse.ArgumentParser("aicommand")

parser.add_argument(
    "prompt", help="Your prompt.", type=str
)

args: Namespace = parser.parse_args()
print("Prompt:\n" + args.prompt.strip())

prompt: str = args.prompt.strip()
temperature: float = 0.7
max_tokens: int = 60

chat_completion: ChatCompletion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
)

choice: Choice = chat_completion.choices[0]
generated_text = choice.message.content.strip()
print("Response:\n" + generated_text)
