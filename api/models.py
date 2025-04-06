import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('passenger', 'Passenger'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    objects = UserManager()

    def __str__(self):
        return self.email


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    vehicle_description = models.TextField()

    def __str__(self):
        return f"{self.user.name} - {self.license_plate}"
    
class LostItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length= 50, blank= True, null=True)
    license_plate = models.CharField(max_length=50, blank= True, null=True)
    date_lost = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.item_name}"
    
class FoundItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length= 50, blank= True, null=True)
    license_plate = models.CharField(max_length=50, blank= True, null=True)
    date_found = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return super().__str__()