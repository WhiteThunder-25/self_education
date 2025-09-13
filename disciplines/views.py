from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny

from disciplines.models import EducationalModule, Topic, Answers, StudentAnswers, Lesson, Quiz
from disciplines.serializers import (AnswersSerializer, StudentAnswersSerializer, EducationalModuleSerializer,
                                LessonSerializer, QuizSerializer, TopicSerializer)
from users.permissions import IsAdmin, IsOwner, IsTeacher
from disciplines.paginators import LessonPagination


class EducationalModuleViewSet(viewsets.ModelViewSet):
    serializer_class = EducationalModuleSerializer
    queryset = EducationalModule.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            self.permission_classes = (IsAuthenticated, IsAdmin)
        else:
            self.permission_classes = (AllowAny,)

        return super().get_permissions()


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            self.permission_classes = (IsAuthenticated, IsAdmin)
        else:
            self.permission_classes = (AllowAny,)

        return super().get_permissions()


class LessonCreateView(generics.CreateAPIView):
    """Создание занятия"""
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsTeacher | IsAdmin)

    def perform_create(self, serializer):
        """Определение владельца занятия"""
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


@method_decorator(cache_page(60 * 15), name='dispatch')
class LessonListView(generics.ListAPIView):
    """Список всех занятий"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination


class LessonDetailView(generics.RetrieveAPIView):
    """Получение информации о конкретном занятии"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateView(generics.UpdateAPIView):
    """Изменение информации о конкретном занятии"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class LessonDeleteView(generics.DestroyAPIView):
    """Удаление конкретного занятия"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsOwner)


class QuizCreateApiView(CreateAPIView):
    """Создание вопроса по занятию"""

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsTeacher | IsAdmin,)

    def perform_create(self, serializer):
        """Определение владельца вопроса"""

        questions = serializer.save()
        questions.owner = self.request.user
        questions.save()


class QuizListApiView(ListAPIView):
    """Список всех вопросов теста по конкретному занятию"""

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizUpdateApiView(UpdateAPIView):
    """Изменение информации о конкретном вопросе теста"""

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (
        IsTeacher | IsAdmin,
        IsOwner | IsAdmin,
    )


class QuizDeleteApiView(DestroyAPIView):
    """Удаление конкретного вопроса теста"""

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (
        IsTeacher | IsAdmin,
        IsOwner | IsAdmin,
    )


class AnswersCreateApiView(CreateAPIView):
    """Создание ответа к вопросу теста"""

    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer
    permission_classes = (IsTeacher | IsAdmin,)

    def perform_create(self, serializer):
        """Определение владельца ответа"""

        answers = serializer.save()
        answers.owner = self.request.user
        answers.save()


class AnswersListApiView(ListAPIView):
    """Список всех ответов к вопросу теста по конкретному вопросу"""

    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer


class AnswersUpdateApiView(UpdateAPIView):
    """Изменение информации о конкретном ответе к вопросу теста"""

    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer
    permission_classes = (
        IsTeacher | IsAdmin,
        IsOwner | IsAdmin,
    )


class AnswersDeleteApiView(DestroyAPIView):
    """Удаление конкретного ответа к вопросу теста"""

    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer
    permission_classes = (
        IsTeacher | IsAdmin,
        IsOwner | IsAdmin,
    )


class StudentAnswersCreateApiView(CreateAPIView):
    """Создание ответа студента на вопрос теста"""

    queryset = StudentAnswers.objects.all()
    serializer_class = StudentAnswersSerializer

    def perform_create(self, serializer):
        """Определение владельца ответа """

        answer_student = serializer.save()
        # сохраняем текущего владельца
        answer_student.owner = self.request.user

        if answer_student.answer.correct:
            answer_student.is_correct = True
            answer_student.save()

        # увеличиваем счетчик правильных ответов с фильтром по пользователю и занятию
        answer_student.count_of_correct = StudentAnswers.objects.filter(
            owner=self.request.user,
            answer__question__lesson=answer_student.answer.question.lesson,
            is_correct=True,
        ).count()
        # увеличиваем счетчик заданных вопросов пользователю и занятию
        answer_student.count_of_question = StudentAnswers.objects.filter(
            owner=self.request.user,
            answer__question__lesson=answer_student.answer.question.lesson,
        ).count()

        answer_student.save()

    def get_queryset(self):
        """Ограничение доступа к ответам студента по текущему владельцу"""

        return StudentAnswers.objects.filter(owner=self.request.user)


class StudentAnswersListApiView(ListAPIView):
    """Список всех ответов студента на вопросы теста"""

    queryset = StudentAnswers.objects.all()
    serializer_class = StudentAnswersSerializer

    def get_queryset(self):
        """Ограничение доступа к ответам студента по текущему владельцу, кроме администратора и преподавателей"""

        if (
            self.request.user.is_staff
            | self.request.user.groups.filter(name="teacher").exists()
        ):
            return StudentAnswers.objects.all()

        return StudentAnswers.objects.filter(owner=self.request.user)


class StudentAnswersDeleteApiView(DestroyAPIView):
    """Удаление ответов студента"""

    queryset = Answers.objects.all()
    serializer_class = StudentAnswersSerializer
    permission_classes = (
        IsTeacher | IsAdmin,
        IsOwner | IsAdmin,
    )


class StudentAnswersDetailApiView(RetrieveAPIView):
    """Получение информации об ответе студента"""

    queryset = StudentAnswers.objects.all()
    serializer_class = StudentAnswersSerializer
