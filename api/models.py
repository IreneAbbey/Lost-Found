from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE = [
        ('admin', 'admin'),
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
    ]
    email = models.EmailField(unique= True),
    phone_number = models.CharField(max_length= 10),
    role = models.CharField(max_length= 10, choices=ROLE, default='passenger')

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

class LostItem(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('matched', 'Matched'),
        ('recorved', 'Recovered')
    ]
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item_name = models.CharField(max_length=200),
    description = models.TextField(),
    date_lost = models.DateTimeField(null=True),
    location = models.CharField(max_length=200),
    vehicle_type = models.CharField(max_length=100),
    vehicle_description = models.TextField(),
    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    def __str__(self):
        return self.item_name

class FoundItem(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('matched', 'Matched'),
        ('returned', 'Returned')
    ]
    user = models.ForeignKey(User, on_delete= models.CASCADE),
    item_name = models.CharField(max_length=200),
    description = models.TextField(),
    date_found = models.DateTimeField(null=False),
    location = models.CharField(max_length=200),
    vehicle_type = models.CharField(max_length=100, null=True),
    vehicle_description = models.TextField(null=True),
    status = models.CharField(max_length=10, choices=STATUS, default='pending')