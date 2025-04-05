from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
ROLE_CHOICES = [
        ('admin', 'admin'),
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
    ]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Driver(models.Model):
    driver_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=100)
    vehicle_description = models.TextField()

    def __str__(self):
        return f"{self.user.name} - {self.vehicle_type}"

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

    def __str__(self):
        return self.item_name
    
class Match(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='lost_item_matches')
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, related_name='found_item_matches')
    match_score = models.FloatField()
    date_matched = models.DateTimeField(auto_now_add=True)