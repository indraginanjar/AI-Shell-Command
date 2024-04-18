from subprocess import CompletedProcess
import subprocess


class TestAiPrompt:
    def test_prompt_how_to_remove_environment_variable(self):
        prompt: str = 'how to remove an environment variable on powershell'

        result: CompletedProcess[bytes] = subprocess.run(
            ["python", 'aiprompt.py', '"' + prompt + '"'],
            stdout=subprocess.PIPE
        )

        output: str = result.stdout.decode("utf-8")

        assert output.__contains__('use the following command')
