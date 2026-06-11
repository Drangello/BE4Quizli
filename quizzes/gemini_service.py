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

def generate_quiz_content(transcript):
    """
    Generate quiz data from transcript.
    """

    client = get_gemini_client()

    prompt = f"""
Create a quiz from the following transcript.

Return ONLY valid JSON.

Format:

{{
  "title": "Quiz Title",
  "description": "Quiz Description",
  "questions": [
    {{
      "question_title": "Question",
      "question_options": [
        "A",
        "B",
        "C",
        "D"
      ],
      "answer": "Correct Answer"
    }}
  ]
}}

Rules:
- Create exactly 10 questions
- Exactly 4 answer options
- One correct answer
- Return valid JSON only
- No markdown
- No explanation

Transcript:

{transcript}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return json.loads(response.text)