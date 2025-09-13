from django.db import models
from config import settings


NULLABLE = {"blank": "True", "null": "True"}


class EducationalModule(models.Model):
    """ Модель образовательного модуля """
    name = models.CharField(max_length=150, verbose_name="Название образовательного модуля",
                            help_text="Введите название модуля")
    description = models.TextField(verbose_name="Описание образовательного модуля",
                                   help_text="Введите описание модуля", **NULLABLE)

    class Meta:
        verbose_name = "Образовательный модуль"
        verbose_name_plural = "Образовательные модули"

    def __str__(self):
        return self.name


class Topic(models.Model):
    """ Модель темы образовательного модуля """
    name = models.CharField(max_length=150, verbose_name="Название темы", help_text="Введите название темы")
    description = models.TextField(verbose_name="Описание темы", help_text="Введите описание темы", **NULLABLE)
    educational_module = models.ForeignKey(EducationalModule, on_delete=models.CASCADE, help_text="Выберите модуль",
                                           verbose_name="Образовательный модуль", related_name="topics", **NULLABLE)

    class Meta:
        verbose_name = "Образовательная тема"
        verbose_name_plural = "Образовательные темы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """ Модель занятия """
    name = models.CharField(max_length=150, verbose_name="Название занятия", help_text="Введите название занятия")
    description = models.TextField(verbose_name="Описание занятия", help_text="Введите описание занятия", **NULLABLE)
    video_link = models.URLField(max_length=200, verbose_name="Ссылка на урок", help_text="Добавьте ссылку на урок")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Тема",
                              help_text="Выберите образовательную тему", related_name="lessons", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Преподаватель",
                              help_text="Выберите преподавателя", related_name="lessons", **NULLABLE)

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    def __str__(self):
        return self.name


class Quiz(models.Model):
    """ Вопросы теста к занятию """
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Занятие")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name="Преподаватель", **NULLABLE)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class Answers(models.Model):
    """ Ответы на вопросы теста """
    question = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer = models.CharField(max_length=255, verbose_name="Ответ")
    correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name="Преподаватель", **NULLABLE)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = "Правильный ответ"
        verbose_name_plural = "Правильные ответы"


class StudentAnswers(models.Model):
    """Ответы студента"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name="Студент", **NULLABLE)
    question = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE, verbose_name="Ответ", **NULLABLE)
    is_correct = models.BooleanField(default=False, verbose_name="Верно")
    count_of_questions = models.IntegerField(default=0, verbose_name="Количество вопросов теста")
    count_of_correct_answers = models.IntegerField(default=0, verbose_name="Количество правильных ответов")

    def __str__(self):
        return f"{self.owner} - {self.question} - {self.answer}"

    class Meta:
        verbose_name = "Ответ студента"
        verbose_name_plural = "Ответы студента"
