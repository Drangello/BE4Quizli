import json
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def get_gemini_client():
    """
    Return configured Gemini client.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    return genai.Client(api_key=api_key)


def test_gemini():
    """
    Test Gemini connection.
    """

    client = get_gemini_client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Answer only with: Quizly works",
    )

    return response.text