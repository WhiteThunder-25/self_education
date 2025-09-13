from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from disciplines.models import Answers, StudentAnswers, Lesson, Quiz
from users.models import User


class QuizTestCase(APITestCase):
    """Тестирование API для урока"""

    def setUp(self):
        """Создание пользователя, урока и опроса"""
        self.user = User.objects.create(email="123@123.123")
        teachers_group = Group.objects.create(name="Teachers")
        self.user.groups.add(teachers_group)
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(
            owner=self.user,
            name="История Древней Греции",
            description="Раздел истории древних времен",
        )
        self.questions = Quiz.objects.create(
            lesson=self.lesson,
            question="История Древней Греции",
            owner=self.user,
        )
        self.answers = Answers.objects.create(
            question=self.questions,
            owner=self.user,
            answer="Герой мифов",
            correct=True,
        )


    def test_lesson_detail(self):
        """Проверка получения конкретного занятия"""
        url = reverse("disciplines:lesson", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "История Древней Греции")


    def test_lesson_list(self):
        url = reverse("disciplines:lessons")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "topic": None,
                    "video_link": self.lesson.video_link,
                }
            ]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


    def test_create_student_answers(self):
        """Проверка создания нового ответа студента"""
        url = reverse("disciplines:create_student_answers")
        data = {
            "answer": self.answers.pk,
            "question": self.questions.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentAnswers.objects.count(), 1)


    def test_list_student_answers(self):
        """Проверка получения списка всех ответов студента"""
        self.student_answers = StudentAnswers.objects.create(
            answer=self.answers, question=self.questions, owner=self.user
        )
        url = reverse("disciplines:list_student_answers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["is_correct"], False)


    def test_quiz_create(self):
        """Проверка создания нового вопроса"""
        url = reverse("disciplines:create_quiz")
        data = {"question": "Сколько подвигов совершил Геракл?", "lesson": self.lesson.pk}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)

