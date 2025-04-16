import pytest
from utils.msg_gen import MessageGenerator
from constants.settings import Settings
import tempfile
import os


def test_load_file_clearly():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        try:
            temp_file.write(b"  Test content with extra spaces and\nnewlines.  ")
            temp_file.close()

            result = MessageGenerator.load_file_clearly(temp_file.name)
            assert result == "Test content with extra spaces and newlines."
        finally:
            os.unlink(temp_file.name)

def test_load_file_clearly_file_not_found():
    result = MessageGenerator.load_file_clearly("/non/existent/filepath")
    assert result is None

def test_load_file_clearly_max_length():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        try:
            temp_file.write(b"1234567890")
            temp_file.close()

            result = MessageGenerator.load_file_clearly(temp_file.name, max_length=5)
            assert result == "12345"
        finally:
            os.unlink(temp_file.name)

def test_generate_mocked(mock_llm_utils):
    msg_gen = MessageGenerator(api_key="test_key")
    result = msg_gen.generate("Test item description")
    assert result == "Generated text"
    mock_llm_utils.generate_text.assert_called_once()

def test_generate_prompt(message_generator):
    with tempfile.NamedTemporaryFile(delete=False) as prompt_file, \
         tempfile.NamedTemporaryFile(delete=False) as profile_file:
        try:
            prompt_file.write(b"This is a prompt with <PROFILE_PLACEHOLDER> and <WOMEN_PLACEHOLDER>.")
            profile_file.write(b"User profile content.")
            prompt_file.close()
            profile_file.close()

            # Update settings to use the temporary files
            message_generator.prompt_file_path = prompt_file.name
            message_generator.profile_file_path = profile_file.name

            prompt = message_generator.generate_prompt("Item description")
            assert "User profile content" in prompt
            assert "Item description" in prompt
            assert "<PROFILE_PLACEHOLDER>" not in prompt
            assert "<WOMEN_PLACEHOLDER>" not in prompt
        finally:
            os.unlink(prompt_file.name)
            os.unlink(profile_file.name)

def test_generate(message_generator):
    with tempfile.NamedTemporaryFile(delete=False) as prompt_file, \
         tempfile.NamedTemporaryFile(delete=False) as profile_file:
        try:
            # Provide detailed instructions in the prompt
            prompt_file.write(b"Hello, My name is <PROFILE_PLACEHOLDER>. My friend name is <WOMEN_PLACEHOLDER>. what is my name and my friend name?")
            profile_file.write(b"John Doe")
            prompt_file.close()
            profile_file.close()

            # Update settings to use the temporary files
            message_generator.prompt_file_path = prompt_file.name
            message_generator.profile_file_path = profile_file.name

            result = message_generator.generate("Shimi Tavori")
            # Assert the LLM's expected response
            assert "John Doe" in result
            assert "Shimi Tavori" in result
            # assert "Sholomo Tavori" in result
        
        finally:
            os.unlink(prompt_file.name)
            os.unlink(profile_file.name)
