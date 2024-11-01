import requests

from src.ai.ai_service import AIService


class ClaudeService(AIService):
    def __init__(self, api_key: str, use_sonnet: bool = False):
        self.api_key = api_key
        self.use_sonnet = use_sonnet
        self.conversation_id = None

        if self.use_sonnet:
            self._initialize_claude_conversation()

    def _initialize_claude_conversation(self):
        """
        Initialize a conversation with Claude for Sonnet mode.
        :return: None
        """
        response = requests.post(
            "https://api.anthropic.com/v1/conversation",
            headers={"x-api-key": self.api_key},
            json={}
        )

        self.conversation_id = response.json().get("conversation_id")

    def generate_commit_message(self, diff_output: str) -> str:
        """
        Generate a commit message using Claude.
        :param diff_output: The diff output to generate the commit message from
        :return: The generated commit message
        """
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        data = {
            "model": "claude-sonnet" if self.use_sonnet else "claude-v1",
            "prompt": f"Generate a concise and descriptive commit message for the following changes:\n\n{diff_output}",
            "max_tokens_to_sample": 50,
            "temperature": 0.7
        }

        if self.use_sonnet and self.conversation_id:
            data["conversation_id"] = self.conversation_id

        response = requests.post(
            "https://api.anthropic.com/v1/complete",
            headers=headers,
            json=data
        )

        return response.json()["completion"].strip()
