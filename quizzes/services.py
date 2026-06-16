from .gemini_service import generate_quiz_content
from .models import Question, Quiz
from .whisper_service import transcribe_audio
from .youtube_service import download_audio


def create_quiz_from_url(user, video_url):
    """
    Create and save quiz from youtube url.
    """

    quiz_data = create_quiz_from_video(video_url)
    quiz = save_quiz(user, video_url, quiz_data)

    create_questions(quiz, quiz_data["questions"])

    return quiz


def create_quiz_from_video(video_url):
    """
    Create quiz data from youtube video.
    """

    audio_path = download_audio(video_url)
    transcript = transcribe_audio(audio_path)

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