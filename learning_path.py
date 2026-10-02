import logging

from gemini_client import ask_gemini

logger = logging.getLogger(__name__)


def get_learning_recommendations(topic: str) -> str:
    """Create a personalized learning path for the given topic."""
    prompt = f"""\
You are EduGenie, an educational learning-path assistant.
Create a personalized learning path for the following topic:
{topic}

Requirements:
- Start with beginner concepts.
- Progress from beginner to intermediate to advanced.
- Organize the learning path in a clear sequence.
- Give a short description for each stage.
- Suggest useful learning resources such as videos, articles, or books.
- Include a realistic suggested timeline.
- Use simple and practical language.
- Adapt the path to a beginner learner.
"""
    logger.info("Generating learning path for: %.80s…", topic)
    return ask_gemini(prompt)