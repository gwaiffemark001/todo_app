from django.conf import settings
from django.db import models

# Create your models here.
class TodoItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='todos')
    category_choices = ['Work','Personal']
    category=models.CharField(max_length=20, choices=[(choice, choice) for choice in category_choices], default='Personal')
    title=models.CharField(max_length=100)
    description=models.TextField()
    date_due=models.DateTimeField()
    is_completed=models.BooleanField(default=False)
    def __str__(self):
        return self.title

