import logging

from gemini_client import ask_gemini

logger = logging.getLogger(__name__)


def explain_topic(topic: str) -> str:
    """Explain a topic in simple language using Gemini."""
    prompt = f"""\
You are EduGenie, an educational assistant.
Explain the following topic in simple language so that a beginner
can easily understand it.

Topic:
{topic}

Requirements:
- Use simple words.
- Explain the main idea clearly.
- Break difficult ideas into smaller points.
- Give a simple example when useful.
- Avoid unnecessary technical jargon.
"""
    logger.info("Explaining topic: %.80s…", topic)
    return ask_gemini(prompt)
