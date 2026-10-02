import json
import logging

from gemini_client import ask_gemini

logger = logging.getLogger(__name__)


def generate_quiz(text: str):
    """Generate a 3-question multiple-choice quiz from the given text."""
    prompt = f"""\
You are EduGenie, an educational quiz generator.
Create exactly 3 multiple-choice questions from the following text.

Requirements:
- Exactly 3 questions
- Each question must have exactly 4 options
- Include the correct answer
- Make the questions relevant to the provided text
- Make the incorrect options plausible
- Return ONLY valid JSON
- Do not use Markdown code fences

Return this exact structure:
[
  {{
    "question": "Question here",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option"
  }}
]

Text:
{text}
"""
    logger.info("Generating quiz for: %.80s…", text)
    result = ask_gemini(prompt).strip()

    # Strip markdown code fences if the model wraps output in them
    if result.startswith("```"):
        result = result.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        logger.warning("Failed to parse quiz JSON, returning raw response")
        return {
            "error": "Could not parse the generated quiz as JSON.",
            "raw_response": result,
        }