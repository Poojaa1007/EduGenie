import logging

from gemini_client import ask_gemini

logger = logging.getLogger(__name__)


def answer_question(question: str) -> str:
    """Use Gemini to answer a student's question."""
    prompt = f"""\
You are EduGenie, an educational assistant.
Answer the student's question clearly and concisely.
Use simple language that a student can understand.
If useful, include a short example.

Student question:
{question}
"""
    logger.info("Answering question: %.80s…", question)
    return ask_gemini(prompt)