from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('worker', 'Support Worker'),
        ('coordinator', 'Coordinator'),
        ('practitioner', 'Behaviour Practitioner'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='worker',
        help_text="User role in the system"
    )
    
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_worker(self):
        return self.role == 'worker'
    
    @property
    def is_coordinator(self):
        return self.role == 'coordinator'
    
    @property
    def is_practitioner(self):
        return self.role == 'practitioner'