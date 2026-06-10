from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quiz
from .serializers import QuizSerializer


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