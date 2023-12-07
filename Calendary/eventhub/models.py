from django.db import models
from accounts.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#FFFFFF')

    def __str__(self) -> str:
        return self.name
    
class Task(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Diariamente'),
        ('weekly', 'Semanalmente'),
        ('monthly', 'Mensualmente'),
        ('yearly', 'Anualmente'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    tags = models.ManyToManyField(Tag, blank=True)
    users = models.ManyToManyField(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    has_frequency = models.BooleanField(default=False)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, blank=True, null=True, default=None)
    frequency_detail = models.CharField(max_length=100, blank=True, null=True, default=None)

    def __str__(self) -> str:
        return self.title