"""
Google Gemini AI service for PocketSmartAI.

The Gemini SDK is imported only when an API request is made,
so the application can still start when no API key is configured.
"""

from functools import lru_cache

from app.config import settings


DEFAULT_MODEL = "gemini-2.5-flash"


@lru_cache(maxsize=1)
def _get_gemini_client():
    """
    Create and cache the Gemini client.

    Returns None when the Gemini package or API key is unavailable.
    """

    if not settings.gemini_api_key:
        return None

    try:
        from google import genai

        return genai.Client(
            api_key=settings.gemini_api_key
        )

    except ImportError:
        return None

    except Exception:
        return None


def is_gemini_available() -> bool:
    """
    Check whether Gemini is configured and available.
    """

    return _get_gemini_client() is not None


def generate_ai_response(
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Generate a response using Google Gemini.

    If Gemini is not configured, a helpful fallback response
    is returned instead of crashing the application.
    """

    prompt = prompt.strip()

    if not prompt:
        return "Please provide a question or planning request."

    client = _get_gemini_client()

    if client is None:
        return (
            "Gemini AI is not configured yet. "
            "Please add GEMINI_API_KEY to your .env file "
            "and install the Google GenAI package."
        )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        text = getattr(response, "text", None)

        if text:
            return text.strip()

        return (
            "Gemini returned an empty response. "
            "Please try again."
        )

    except Exception as exc:
        # Do not expose internal API details to users.
        print(
            f"Gemini service error: {type(exc).__name__}"
        )

        return (
            "I couldn't generate the AI response right now. "
            "Please try again in a moment."
        )


def generate_planner(
    planner_type: str,
    user_input: str,
) -> str:
    """
    Generate a PocketSmartAI planning response.
    """

    planner_type = planner_type.strip()
    user_input = user_input.strip()

    if not planner_type:
        planner_type = "general"

    prompt = f"""
You are PocketSmartAI, a helpful personal planning assistant.

Create a practical and easy-to-follow plan.

Planner type:
{planner_type}

User requirements:
{user_input}

Instructions:
- Understand the user's requirements.
- Give a clear structured plan.
- Keep recommendations practical.
- Consider the user's stated budget or constraints.
- Use headings and bullet points where useful.
- Do not invent personal information about the user.
- If important information is missing, state reasonable assumptions.
"""

    return generate_ai_response(prompt)