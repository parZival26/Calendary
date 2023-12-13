from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Task

def send_email(task, user):
    send_mail(
        'Recordatorio de tarea',
        f'La tarea "{task.title}" está programada para ser entregada pronto.',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )

def check_due_dates():
    for task in Task.objects.all():
        for user in task.users.all():
            if task.due_date - timedelta(days=3) <= timezone.now() <= task.due_date - timedelta(days=2):
                send_email(task, user)
            elif task.due_date - timedelta(days=2) <= timezone.now() <= task.due_date - timedelta(days=1):
                send_email(task, user)
            elif task.due_date - timedelta(days=1) <= timezone.now() <= task.due_date:
                send_email(task, user)

