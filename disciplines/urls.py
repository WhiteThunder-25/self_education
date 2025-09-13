from django.urls import path
from rest_framework.routers import DefaultRouter
from disciplines.apps import DisciplinesConfig
from disciplines.views import (AnswersCreateApiView, AnswersDeleteApiView,
                          AnswersListApiView, StudentAnswersCreateApiView,
                          StudentAnswersDeleteApiView,
                          StudentAnswersListApiView,
                          AnswersUpdateApiView,
                          LessonCreateView, LessonDeleteView,
                          LessonListView, LessonDetailView,
                          LessonUpdateView, QuizCreateApiView,
                          QuizDeleteApiView, QuizListApiView,
                          QuizUpdateApiView, EducationalModuleViewSet,
                          TopicViewSet)

app_name = DisciplinesConfig.name

router = DefaultRouter()
router.register(r'educational_modules', EducationalModuleViewSet)
router.register(r'topics', TopicViewSet)
urlpatterns = [
    path("lesson/", LessonListView.as_view(), name="lessons"),
    path("lesson/create/", LessonCreateView.as_view(), name="create_lesson"),
    path("lesson/<int:pk>/", LessonDetailView.as_view(), name="lesson"),
    path("lesson/<int:pk>/update/", LessonUpdateView.as_view(), name="update_lesson"),
    path("lesson/<int:pk>/delete/", LessonDeleteView.as_view(), name="delete_lesson"),
    path("quiz/", QuizListApiView.as_view(), name="quiz"),
    path("quiz/create/", QuizCreateApiView.as_view(), name="create_quiz"),
    path("quiz/<int:pk>/update/", QuizUpdateApiView.as_view(), name="update_quiz"),
    path("quiz/<int:pk>/delete/", QuizDeleteApiView.as_view(), name="delete_quiz"),
    path("answers/", AnswersListApiView.as_view(), name="answers"),
    path("answers/create/", AnswersCreateApiView.as_view(), name="create_answers"),
    path("answers/<int:pk>/update/", AnswersUpdateApiView.as_view(), name="update_answers"),
    path("answers/<int:pk>/delete/", AnswersDeleteApiView.as_view(), name="delete_answers"),
    path("student_answers/create/", StudentAnswersCreateApiView.as_view(), name="create_student_answers"),
    path("student_answers/", StudentAnswersListApiView.as_view(), name="list_student_answers"),
    path("student_answers/<int:pk>/delete/", StudentAnswersDeleteApiView.as_view(), name="delete_student_answers"),
] + router.urls