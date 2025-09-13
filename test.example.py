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

    def test_lesson_create(self):
        """ Проверка создания нового занятия"""
        url = reverse("disciplines:create_lesson")
        data = {"name": "физика", "description": "Отдел физики"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_list(self):
        """ Проверка получения списка всех занятий"""
        url = reverse("disciplines:lessons")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "История Древней Греции")

    def test_lesson_detail(self):
        """Проверка получения конкретного занятия"""
        url = reverse("disciplines:lesson", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "История Древней Греции")

    def test_lesson_update(self):
        """Проверка изменения названия занятия"""
        url = reverse("disciplines:update_lesson", kwargs={"pk": self.lesson.pk})
        data = {"name": "Литература"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(pk=self.lesson.pk).name, "Литература")

    def test_lesson_delete(self):
        """Проверка удаления занятия"""
        url = reverse("disciplines:delete_lesson", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_quiz_create(self):
        """Проверка создания нового вопроса"""
        url = reverse("disciplines:create_quiz")
        data = {"question": "Сколько подвигов совершил Геракл?", "lesson": self.lesson.pk}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)

    def test_quiz_list(self):
        """Проверка получения списка всех вопросов"""
        url = reverse("disciplines:quiz")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["question"], "Кто такой Геракл?")

    def test_quiz_update(self):
        """Проверка изменения вопроса"""
        url = reverse("disciplines:update_quiz", kwargs={"pk": self.questions.pk})
        data = {"question": "Кто такой Зевс?"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Quiz.objects.get(pk=self.questions.pk).question,
            "Кто такой Геракл?",
        )

    def test_quiz_delete(self):
        """Проверка удаления вопроса"""
        url = reverse("disciplines:delete_quiz", kwargs={"pk": self.questions.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quiz.objects.count(), 0)

    def test_create_answers(self):
        """Проверка создания нового ответа"""
        url = reverse("disciplines:create_answers")
        data = {
            "question": self.questions.pk,
            "answer": "Сын Зевса",
            "correct": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answers.objects.count(), 2)

    def test_answers_list(self):
        """Проверка получения списка всех ответов"""
        url = reverse("disciplines:answers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["answer"], "Число, умноженное на само себя")

    def test_update_answers(self):
        """Проверка изменения ответа"""
        url = reverse("disciplines:update_answers", kwargs={"pk": self.answers.pk})
        data = {"answer": "Число (новый ответ)"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Answers.objects.get(pk=self.answers.pk).answer, "Число (новый ответ)"
        )

    def test_delete_answers(self):
        """Проверка удаления ответа"""
        url = reverse("disciplines:delete_answers", kwargs={"pk": self.answers.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answers.objects.count(), 0)

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

    def test_student_answer_delete(self):
        """Проверка удаления ответа студента"""
        self.answer_student = StudentAnswers.objects.create(answer=self.answers, question=self.questions, owner=self.user)

        url = reverse("disciplines:delete_student_answers", kwargs={"pk": self.student_answers.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(StudentAnswers.objects.count(), 0)
