
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Scan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scans')
    timestamp = models.DateTimeField(default=timezone.now)
    image_path = models.CharField(max_length=200)
    extracted_text = models.TextField()

    def __str__(self):
        return f"Scan by {self.user.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Medicine(models.Model):
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, null=True, blank=True)
    frequency = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name