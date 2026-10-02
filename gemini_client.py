import os
import logging

from google import genai

logger = logging.getLogger(__name__)

# ── Primary and Fallback Models ─────────────────────────────────────
# Using gemini-3.5-flash as primary (fast, generous free quota)
# with automatic fallback if a model hits rate limit or high demand
MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
]


def get_gemini_client() -> genai.Client:
    """Create and return a Gemini API client using the GEMINI_API_KEY env var."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Get one at https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=api_key)


def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response.

    Tries the primary model first, and falls back to alternate models
    if quota (429) or high server demand (503) occurs.
    """
    client = get_gemini_client()
    last_error = None

    for model_name in MODELS:
        logger.info("Sending prompt to Gemini (%s) – %d chars", model_name, len(prompt))
        try:
            response = client.interactions.create(
                model=model_name,
                input=prompt,
                timeout=45.0,
            )
            text = response.output_text
            if text:
                logger.info("Gemini (%s) responded – %d chars", model_name, len(text))
                return text
            logger.warning("Gemini (%s) returned empty text, trying fallback...", model_name)
        except Exception as e:
            err_msg = str(e)
            logger.warning("Gemini model %s failed: %s", model_name, err_msg[:120])
            last_error = e
            # Only try next model if it's a rate limit, quota, or service issue
            if any(k in err_msg for k in ["429", "RESOURCE_EXHAUSTED", "503", "high demand", "not_found", "404"]):
                continue
            raise

    # If all models failed, raise the last encountered error
    raise last_error or RuntimeError("All Gemini models failed to respond.")