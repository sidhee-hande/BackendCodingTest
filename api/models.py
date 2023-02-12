from django.db import models

# Create your models here.

class Messages(models.Model):
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    sender_delete_status = models.BooleanField(default=False)
    receiver_delete_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.sender






