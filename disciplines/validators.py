from rest_framework import serializers
from rest_framework.serializers import ValidationError



def validate_video_link(value):
    """ Валидация ссылки на видео """
    if not value.startswith("https://www.youtube.com/") and not value.startswith("https://rutube.ru/"):

        raise serializers.ValidationError("Неверная ссылка на видео. Добавьте ссылку на видео с Youtube или Rutube")


class StudentAnswersValidators:

    def __call__(self, value):
        """Проверка валидности полей ответа студентов"""

        val = dict(value)

        # Проверка зависимости ответа к вопросу
        if val.get("answer").question != val.get("question"):
            raise ValidationError("Ответ должен быть к заданному вопросу")
