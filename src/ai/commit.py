import subprocess

from ai.ai_service import AIService

# Commit Message Generator class
class CommitMessageGenerator:
    def __init__(self, service: AIService):
        self.service = service

    def generate_commit_message(self) -> str:
        """
        Generate a commit message using the AI service.
        :return: The generated commit message
        """
        diff_output = subprocess.run(
            ["git", "diff", "--cached"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdout

        return self.service.generate_commit_message(diff_output)
