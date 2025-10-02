from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)  # Tên đầy đủ
    phone = models.CharField(max_length=15, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)  # Ngày sinh
    gender = models.CharField(max_length=25, blank=True, null=True)  # Giới tính
    address = models.CharField(max_length=255, blank=True, null=True)  # Địa chỉ
    ROLE_CHOICES = (
        ('user', 'user'),
        ('librarian', 'librarian'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.name or self.user.username
    def get_full_name(self):
        return self.name or self.user.get_full_name() or self.user.username

class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.title} - {self.author}"
    