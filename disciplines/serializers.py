from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField, ValidationError)

from disciplines.models import EducationalModule, Lesson, Topic
from disciplines.validators import validate_video_link
from disciplines.models import Answers, StudentAnswers, Lesson, Quiz
from disciplines.validators import StudentAnswersValidators


class QuizSerializer(ModelSerializer):
    """Serializer для вопросов по занятию"""

    count_of_questions = SerializerMethodField()
    questions = SerializerMethodField()
    answers = SerializerMethodField()
    student_answers = SerializerMethodField()

    def get_questions(self, lesson):
        """Возвращает список вопросов по занятию"""

        return [
            {"id": obj.id, "question": obj.question}
            for obj in Quiz.objects.filter(lesson=lesson)
        ]

    def get_count_of_questions(self, lesson):
        """Возвращает количество вопросов по занятию"""

        return Quiz.objects.filter(lesson=lesson).count()

    def get_student_answers(self, instance):
        """Возвращает список студентов """

        # Получаем текущего пользователя
        user = self.context["request"].user

        # Получаем все AnswerStudent, связанные с текущим занятием
        try:
            student_answers = StudentAnswers.objects.filter(
                owner=user, question__lesson=instance
            ).latest("id")

            count_question = student_answers.count_of_questions
            count_correct = student_answers.count_of_correct
            percent_correct = 0
            if count_question != 0:
                percent_correct = count_correct * 100 / count_question
            return {
                "Кол-во отвеченных вопросов": count_question,
                "Кол-во правильных ответов": count_correct,
                "Процент правильных ответов": int(percent_correct),
            }
        except StudentAnswers.DoesNotExist:
            return {
                "Кол-во отвеченных вопросов": 0,
                "Кол-во правильных ответов": 0,
                "Процент правильных ответов": 0,
            }

    class Meta:
        model = Lesson
        fields = [
            "id",
            "name",
            "description",
            "count_of_questions",
            "questions",
            "student_answers",
            "owner",
        ]


    def get_answers(self, instance):
        """Возвращает список id ответов в вопросе теста"""
        return [
            {"id": obj.id, "answer": obj.answer}
            for obj in Answers.objects.filter(question=instance)
        ]

    class Meta:
        model = Quiz
        exclude = [
            "owner",
        ]
        ordering = ["question", "answer"]


class AnswersSerializer(ModelSerializer):
    """Serializer для ответа"""

    class Meta:
        model = Answers
        fields = "__all__"


class StudentAnswersSerializer(ModelSerializer):
    """Serializer для ответа"""

    info_lesson = SerializerMethodField()

    def get_info_lesson(self, instance):
        """Возвращает информацию о занятии"""

        if instance.count_of_questions != 0:
            percent_correct = (
                instance.count_of_correct * 100 / instance.count_of_questions
            )
            result = {
                "тема id": instance.answer.question.lesson.id,
                "Название темы": instance.answer.question.lesson.name,
                "Вопрос id": instance.answer.question.id,
                "Вопрос": instance.answer.question.question,
                "Дан ответ": instance.answer.answer,
                "Количество отвеченных вопросов": instance.count_of_questions,
                "Количество правильных ответов": instance.count_of_correct,
                "Процент правильных ответов": int(percent_correct),
            }
            return result
        else:
            result = {
                "id": instance.answer.question.lesson.id,
                "Название темы": instance.answer.question.lesson.name,
                "Количество отвеченных вопросов": instance.count_of_questions,
            }
            return result

    def validate(self, data):
        """Проверяет корректность ответа"""
        request = self.context.get("request")
        # Получаем текущего пользователя
        user = request.user

        # Если ответ есть и он принадлежит текущему пользователю,
        if StudentAnswers.objects.filter(
            owner=user, question=data.get("question")
        ).exists():
            raise ValidationError("Уже имеется ответ на вопрос")

        return data

    class Meta:
        model = StudentAnswers
        fields = "__all__"
        validators = [StudentAnswersValidators()]


class LessonSerializer(serializers.ModelSerializer):

    video_link = serializers.CharField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "topic", "video_link"]


class TopicSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Topic
        fields = ["id", "name", "description", "educational_module", "lessons_count", "lessons"]


class EducationalModuleSerializer(serializers.ModelSerializer):
    topics_count = serializers.SerializerMethodField(read_only=True)
    topics = TopicSerializer(many=True, read_only=True)

    def get_topics_count(self, obj):
        return obj.topics.count()

    class Meta:
        model = EducationalModule
        fields = ["id", "name", "description", "topics_count", "topics"]
