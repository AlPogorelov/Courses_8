from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import Habit
from habit.services import send_tg_message

User = get_user_model()


@shared_task
def check_habits():
    '''Уведомление в телеграмм за час до выполнение привычки'''

    now = timezone.localtime(timezone.now())
    time_threshold = now + timedelta(hours=1)

    habits = Habit.objects.filter(
        time__hour=time_threshold.hour,
        time__minute=time_threshold.minute
    )

    for habit in habits:
        try:
            user = habit.user
            if not user.telegram_chat_id:
                continue

            if habit.last_notification:
                time_passed = now - habit.last_notification
                if time_passed.days < habit.frequency:
                    continue

            message = (
                f"🔔 Напоминание о привычке!\n"
                f"Через час ({habit.time.strftime('%H:%M')}) нужно:\n"
                f"• Действие: {habit.action}\n"
                f"• Место: {habit.place}\n"
                f"• Время на выполнение: {habit.execution_time} сек"
            )

            send_tg_message(
                chat_id=user.telegram_chat_id,
                message=message
            )

            habit.last_notification = now
            habit.save()
        except Exception as e:

            print(f"Error in habit {habit.id}: {str(e)}")