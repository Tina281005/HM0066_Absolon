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
    status = models.CharField(
        max_length=10, 
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")], 
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

class GAD7Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gad7_responses",default= None)
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()
    q5 = models.IntegerField()
    q6 = models.IntegerField()
    q7 = models.IntegerField()
    total_score = models.IntegerField(editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Automatically calculate total score before saving"""
        self.total_score = self.q1 + self.q2 + self.q3 + self.q4 + self.q5 + self.q6 + self.q7
        super().save(*args, **kwargs)

    def get_severity(self):
        """Returns severity level based on score"""
        if self.total_score <= 4:
            return "Minimal Anxiety"
        elif self.total_score <= 9:
            return "Mild Anxiety"
        elif self.total_score <= 14:
            return "Moderate Anxiety"
        else:
            return "Severe Anxiety"

    def __str__(self):
        return f"GAD-7 Score: {self.total_score} (User: {self.user.first_name})"
    
class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=[
        ('happy', 'Happy'), ('neutral', 'Neutral'), ('sad', 'Sad'),
        ('anxious', 'Anxious'), ('excited', 'Excited'), ('tired', 'Tired')
    ])
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} - {self.date.strftime('%Y-%m-%d')}"
    


class JournalEntry(models.Model):
    user = models.ForeignKey(UserCreds, on_delete=models.CASCADE)  # Directly reference UserCreds model
    entry_text = models.TextField()
    image = models.ImageField(upload_to='journal_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
         return f"Journal Entry by {self.user.first_name} on {self.created_at}"
    
    