from celery import shared_task

from django.utils import timezone
from django.db import transaction, DatabaseError

from datetime import timedelta
from .models import ActionLog


@shared_task
def clean_logs():
    """
    Логи которые существуют больше 7 дней удаляются.
    """
    seven_days_ago = timezone.now() - timedelta(days=7)

    try:
        with transaction.atomic():

            old_logs = ActionLog.objects.filter(created_at__lt=seven_days_ago)
            count = old_logs.count()
            if count > 0:
                old_logs.delete()
                return f'Удалено {count} записей'        
            else:
                return f'Нет записей для удаления'

    except DatabaseError as e:
        return f'Ошибка базы данных при удалении логов: {e}'
    except Exception as e:
        return f'Неожиданная ошибка: {e}'