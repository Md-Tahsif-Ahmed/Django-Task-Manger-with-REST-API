from django.db import models
from django.contrib.auth.models import User

PRIORITIES = (
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    photos = models.ManyToManyField('Photo', blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITIES)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Photo(models.Model):
    image = models.ImageField(upload_to='task_photos/')
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)
