import os

from google import genai
from google.genai import types

REQUEST_TIMEOUT_MS = 20000

DEFAULT_MODEL = "gemini-3.5-flash-lite"


def create_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Configure it to enable AI analysis.")

    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=REQUEST_TIMEOUT_MS,
            retry_options=types.HttpRetryOptions(attempts=2),
        ),
    )


def get_model_name():
    return os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def generate_response(prompt):
    with create_client() as client:
        response = client.models.generate_content(
            model=get_model_name(),
            contents=prompt,
        )

    return response.text or ""