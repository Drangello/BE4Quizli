from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quiz
from .serializers import QuizSerializer
from .services import create_quiz_from_url


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
        quiz = create_quiz_from_url(
            user=request.user,
            video_url=request.data.get("url"),
        )
        serializer = QuizSerializer(quiz)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        questions = create_dummy_questions()

        for question in questions:
            Question.objects.create(
                quiz=quiz,
                **question,
            )


class QuizDetailView(APIView):
    """
    Retrieve, update or delete one quiz.
    """

    permission_classes = [IsAuthenticated]

    def get_quiz(self, request, quiz_id):
        return Quiz.objects.filter(
            id=quiz_id,
            user=request.user,
        ).first()

    def get(self, request, quiz_id):
        quiz = self.get_quiz(request, quiz_id)

        if quiz is None:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, quiz_id):
        quiz = self.get_quiz(request, quiz_id)

        if quiz is None:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = QuizSerializer(
            quiz,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, quiz_id):
        quiz = self.get_quiz(request, quiz_id)

        if quiz is None:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)