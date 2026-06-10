from .models import Question, Quiz
from .utils import create_dummy_questions


def create_quiz_from_url(user, video_url):
    """
    Create a quiz from a video url.
    """

    quiz = Quiz.objects.create(
        user=user,
        title="Quiz Title",
        description="Quiz Description",
        video_url=video_url,
    )

    create_questions(quiz)

    return quiz


def create_questions(quiz):
    """
    Create all quiz questions.
    """

    questions = create_dummy_questions()

    for question in questions:
        Question.objects.create(
            quiz=quiz,
            **question,
        )