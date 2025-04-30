from django.db import models
from django.utils import timezone
# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class EventReminder(models.Model):
    OCCASION_CHOICES = (
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Logged-in user
    sender_name = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    recipient_email = models.EmailField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES, default='birthday')
    custom_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    year_sent = models.IntegerField(null=True, blank=True)  # <- NEW


    def __str__(self):
        return f"{self.occasion.title()} for {self.recipient_name} on {self.date}"

class OccasionTemplate(models.Model):
    OCCASION_CHOICES = [
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    occasion = models.CharField(max_length=50, choices=OCCASION_CHOICES)

    def __str__(self):
        return self.name
