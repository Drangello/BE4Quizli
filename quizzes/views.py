from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question, Quiz
from .serializers import QuizSerializer
from .utils import create_dummy_questions


class QuizListCreateView(APIView):
    """
    List user quizzes or create a new quiz.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(
            user=request.user
        ).order_by("-created_at")
        serializer = QuizSerializer(quizzes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        quiz = Quiz.objects.create(
            user=request.user,
            title="Quiz Title",
            description="Quiz Description",
            video_url=request.data.get("url"),
        )
        self.create_questions(quiz)

        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_questions(self, quiz):
        questions = create_dummy_questions()

        for question in questions:
            Question.objects.create(
                quiz=quiz,
                **question,
            )