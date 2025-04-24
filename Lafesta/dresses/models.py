from django.db import models
from django.contrib.auth.models import User

class Dress(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    CATEGORY_CHOICES = [
        ('wedding', 'Wedding'),
        ('party', 'Party'),
        ('evening', 'Evening'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('unavailable', 'Unavailable'),
    ]

    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    #image = models.ImageField(upload_to='dress_images/')
    image = models.ImageField(upload_to='images/dresses/dress_img/')

    video = models.FileField(upload_to='dress_videos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')  # ✅ الحالة

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dresses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    dress = models.ForeignKey('Dress', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dress_reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.dress.name} ({self.rating} stars)"


class Rental(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    dress = models.ForeignKey('Dress', on_delete=models.CASCADE, related_name='rentals')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        days = (self.end_date - self.start_date).days + 1
        self.total_price = self.dress.price_per_day * days
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.username} - {self.dress.name} ({self.status})"
