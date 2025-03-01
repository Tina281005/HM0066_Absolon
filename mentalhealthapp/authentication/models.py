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
