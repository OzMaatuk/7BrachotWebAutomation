import re
import logging
from llm_utils import LLMUtils
from constants.settings import Settings
logger = logging.getLogger(__name__)

class MessageGenerator:
    def __init__(self, api_key: str = None,
                    prompt_file_path: str = Settings().PROMPT_FILE,
                    profile_file_path: str = Settings().PROFILE_FILE):
        logger.debug("MessageGenerator instance created")
        self.llm = LLMUtils(api_key)
        self.prompt_file_path = prompt_file_path
        self.profile_file_path = profile_file_path

    def generate(self, item_description: str) -> str:
        logger.debug("MessageGenerator.generate")
        prompt = self.generate_prompt(item_description)
        res = self.llm.generate_text(prompt)
        logger.debug(f"Result: {res}")
        return res
    
    def generate_prompt(self, item_description: str) -> str:
        logger.debug("MessageGenerator.generate_prompt")
        prompt = MessageGenerator.load_file_clearly(self.prompt_file_path)
        user_profile = MessageGenerator.load_file_clearly(self.profile_file_path)
        
        prompt = prompt.replace("<PROFILE_PLACEHOLDER>", user_profile)
        prompt = prompt.replace("<WOMEN_PLACEHOLDER>", item_description)
        logger.debug(f"prompt: {prompt}")
        return prompt

    @staticmethod
    def load_file_clearly(filepath: str, max_length: int = None) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

            # 1. Remove extra whitespace (newlines, tabs, multiple spaces).
            text = re.sub(r'\s+', ' ', text).strip()
            # 2. Remove non-printable characters (optional, but often helpful).
            text = ''.join(char for char in text if ord(char) >= 32) #remove control characters

            if max_length is not None:
                text = text[:max_length]

            return text

        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None