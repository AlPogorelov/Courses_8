from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Habit(models.Model):
    DAILY = 1
    WEEKLY = 7
    FREQUENCY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
    ]

    user_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Место выполнения'
    )
    time = models.TimeField(
        verbose_name='Время выполнения'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )
    is_useful = models.BooleanField(
        default=False,
        verbose_name='Полезная привычка'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка'
    )
    frequency = models.PositiveSmallIntegerField(
        default=DAILY,
        choices=FREQUENCY_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name='Периодичность'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Вознаграждение'
    )
    execution_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name='Время на выполнение (секунды)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная привычка'
    )
    last_notification = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Последнее уведомление'
    )

    def clean(self):
        # Валидация для приятных привычек
        if not self.is_useful:
            if self.related_habit:
                raise ValidationError(
                    "Приятная привычка не может иметь связанную привычку!"
                )
            if self.reward.strip():
                raise ValidationError(
                    "Приятная привычка не может иметь вознаграждение!"
                )

        # Валидация для полезных привычек
        if self.is_useful:
            if self.related_habit and self.reward.strip():
                raise ValidationError(
                    "Нельзя указывать одновременно связанную привычку и вознаграждение!"
                )

            if self.related_habit and self.related_habit.is_useful:
                raise ValidationError(
                    "Связанная привычка должна быть приятной!"
                )

        # Общая валидация времени выполнения
        if self.execution_time > 120:
            raise ValidationError(
                "Время выполнения не может превышать 120 секунд!"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-id']
