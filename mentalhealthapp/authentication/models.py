from django.db import models

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
    

from django.db import models

class GAD7Response(models.Model):
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()
    q5 = models.IntegerField()
    q6 = models.IntegerField()
    q7 = models.IntegerField()
    total_score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GAD-7 Score: {self.total_score} (ID: {self.id})"

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
        return f"GAD-7 Test - {self.user.first_name} - {self.date_taken.strftime('%Y-%m-%d')}"

