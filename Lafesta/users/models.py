from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Choices
USER_TYPES = [
    ('customer', 'Customer'),
    ('owner', 'Dress Owner'),
]

SAUDI_CITIES = [
    ('riyadh', 'Riyadh'),
    ('jeddah', 'Jeddah'),
    ('dammam', 'Dammam'),
    ('abha', 'Abha'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    phone_number = PhoneNumberField(region='SA', blank=True, null=True)
    city = models.CharField(max_length=20, choices=SAUDI_CITIES, blank=True, null=True)
    profile_image = models.ImageField(upload_to="images/avatars/", default="images/avatars/avatar.webp")
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

# Create your models here.
