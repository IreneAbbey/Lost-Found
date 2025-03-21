from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
    ]
    email = models.EmailField(unique= True),
    phone_number = models.CharField(max_length= 10),
    role = models.CharField(max_length= 10, choices=ROLE_CHOICES, default='passenger')

    groups =  models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return self.username
