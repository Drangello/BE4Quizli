from django.urls import path

from .views import QuizDetailView, QuizListCreateView


urlpatterns = [
    path("quizzes/", QuizListCreateView.as_view()),
    path("quizzes/<int:quiz_id>/", QuizDetailView.as_view()),
]