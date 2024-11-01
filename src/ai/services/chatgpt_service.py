import openai

from src.ai.ai_service import AIService


class ChatGPTService(AIService):
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate_commit_message(self, diff_output: str) -> str:
        """
        Generate a commit message using ChatGPT.
        :param diff_output: The diff output to generate the commit message from
        :return: The generated commit message
        """
        response = openai.Completion.create(
            model="gpt-4-turbo",
            prompt=f"Generate a concise and descriptive commit message for the following changes:\n\n{diff_output}",
            max_tokens=50
        )

        return response.choices[0].text.strip()
