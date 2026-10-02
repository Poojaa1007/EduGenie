import logging

from gemini_client import ask_gemini

logger = logging.getLogger(__name__)


def summarize_text(text: str) -> str:
    """Summarize educational text using Gemini."""
    prompt = f"""\
You are EduGenie, an educational assistant.
Summarize the following educational text.

Requirements:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple, clear language.
- Make the summary useful for quick revision.
- Do not add information that is not present in the text.

Text:
{text}
"""
    logger.info("Summarizing text: %.80s…", text)
    return ask_gemini(prompt)