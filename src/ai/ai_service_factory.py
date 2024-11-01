import os

from src.ai.ai_service import AIService
from src.ai.services.chatgpt_service import ChatGPTService
from src.ai.services.claude_service import ClaudeService


class AIServiceFactory:
    @staticmethod
    def create_service(use_chatgpt: bool = False, use_claude: bool = False, use_sonnet: bool = False,
                       openai_api_key: str = None, anthropic_api_key: str = None) -> AIService:
        """
        Creates an instance of the AI service based on specified flags and API keys.

        :param use_chatgpt: Boolean indicating if ChatGPT should be used
        :param use_claude: Boolean indicating if Claude should be used
        :param use_sonnet: Boolean indicating if Sonnet should be used
        :param openai_api_key: OpenAI API key for ChatGPT service
        :param anthropic_api_key: Anthropic API key for Claude service
        :return: An instance of the selected AIService
        :raises ValueError: If an invalid configuration is provided
        """
        # Determine the AI service and API key to use
        if use_chatgpt:
            openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

            if not openai_api_key:
                raise ValueError("OpenAI API key is required for ChatGPT.")

            return ChatGPTService(openai_api_key)

        elif use_claude:
            anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")

            if not anthropic_api_key:
                raise ValueError("Anthropic API key is required for Claude.")

            return ClaudeService(anthropic_api_key, use_sonnet)

        raise ValueError("Invalid AI assistant choice or missing API key for the selected assistant.")
