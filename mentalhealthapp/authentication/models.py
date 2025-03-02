from django.db import models
from django.contrib.auth.models import User

class UserCreds(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('therapist', 'Therapist'),
    )

    email = models.EmailField(max_length=70, unique=True)
    password = models.CharField(max_length=100)  # Will be hashed, so no null/default
    first_name = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.first_name} ({self.role})"


class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class ChatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_chat")
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name="therapist_chat")
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class CallRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="caller")
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name="callee")
    status = models.CharField(max_length=10, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)