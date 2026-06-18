from django.db import transaction

from .gemini_service import generate_quiz_content
from .models import Question, Quiz
from .utils import normalize_youtube_url
from .whisper_service import transcribe_audio
from .youtube_service import download_audio


@transaction.atomic
def create_quiz_from_url(user, video_url):
    """
    Create and save quiz from youtube url.
    """

    normalized_video_url = normalize_youtube_url(video_url)
    quiz_data = create_quiz_from_video(normalized_video_url)
    quiz = save_quiz(user, normalized_video_url, quiz_data)

    create_questions(quiz, quiz_data["questions"])

    return quiz


def create_quiz_from_video(video_url):
    """
    Create quiz data from youtube video.
    """

    audio_path = download_audio(video_url)
    try:
        transcript = transcribe_audio(audio_path)
    finally:
        delete_audio_file(audio_path)

    return generate_quiz_content(transcript)


def delete_audio_file(audio_path):
    """
    Delete temporary audio file.
    """

    if audio_path.exists():
        audio_path.unlink()


def save_quiz(user, video_url, quiz_data):
    """
    Save generated quiz.
    """

    return Quiz.objects.create(
        user=user,
        title=quiz_data["title"],
        description=quiz_data["description"],
        video_url=video_url,
    )


def create_questions(quiz, questions):
    """
    Save generated questions for quiz.
    """

    for question in questions:
        Question.objects.create(
            quiz=quiz,
            question_title=question["question_title"],
            question_options=question["question_options"],
            answer=question["answer"],
        )
