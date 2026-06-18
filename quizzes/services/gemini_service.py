import json
import os
import time

from dotenv import load_dotenv
from google import genai

from ..utils import create_dummy_questions


load_dotenv()


def get_gemini_client():
    """
    Return configured Gemini client.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    return genai.Client(api_key=api_key)


def clean_json_response(response_text):
    """
    Remove markdown from Gemini JSON response.
    """

    return response_text.replace("```json", "").replace("```", "").strip()


def build_quiz_prompt(transcript):
    """
    Build prompt for Gemini quiz generation.
    """

    return f"""
Create a quiz from the following transcript.

Return ONLY valid JSON with:
title, description, questions.

Rules:
- Create exactly 10 questions
- Each question has question_title
- Each question has exactly 4 question_options
- Each question has one answer
- The answer must match one option exactly
- No markdown
- No explanation
- Create the title, description, questions and answers in German

Transcript:
{transcript}
"""


def get_fallback_quiz():
    """
    Return fallback quiz if Gemini fails.
    """

    return {
        "title": "Ersatz Quiz",
        "description": "Automatisch erzeugtes Ersatzquiz.",
        "questions": create_dummy_questions(),
    }


def generate_quiz_content(transcript):
    """
    Generate quiz data from transcript.
    """

    client = get_gemini_client()
    prompt = build_quiz_prompt(transcript)

    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            clean_text = clean_json_response(response.text)

            return json.loads(clean_text)

        except Exception:
            time.sleep(3)

    return get_fallback_quiz()
