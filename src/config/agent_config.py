"""AutoGen agent configuration with Groq API setup."""

import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "openai/gpt-oss-120b"

# Validate API key is set
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY environment variable is not set. "
        "Please create a .env file with your Groq API key. "
        "See .env.example for reference."
    )

# Initialize OpenAI-compatible client with Groq endpoint
groq_client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


# AutoGen LLM Configuration
def get_llm_config():
    """Get LLM configuration for AutoGen agents."""
    return {
        "model": GROQ_MODEL,
        "api_key": GROQ_API_KEY,
        "base_url": GROQ_BASE_URL,
        "api_type": "openai",
    }


# Alternative configuration using client directly
def get_llm_config_with_client():
    """Get LLM configuration with OpenAI client for AutoGen agents."""
    return {
        "model": GROQ_MODEL,
        "client": groq_client,
    }
