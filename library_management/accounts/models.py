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
    MEMBERSHIP_CHOICES = [
        ('basic', 'Cơ bản'),
        ('standard', 'Tiêu chuẩn'),
        ('premium', 'Cao cấp'),
    ]
    membership_level = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_CHOICES,
        default='basic'   # khi đăng ký mặc định là "Cơ bản"
    )
    membership_upgrade_date = models.DateTimeField(null=True, blank=True, verbose_name="Ngày nâng cấp gói")
    membership_expiry_date = models.DateTimeField(null=True, blank=True, verbose_name="Ngày hết hạn gói")
    def __str__(self):
        return self.name or self.user.username
    def get_full_name(self):
        return self.name or self.user.get_full_name() or self.user.username

    def upgrade_membership(self, new_level):
        """Hàm nâng cấp thành viên"""
        levels = ['basic', 'standard', 'premium']
        current_index = levels.index(self.membership_level)
        new_index = levels.index(new_level)
        if new_index > current_index:  # chỉ cho nâng cấp
            self.membership_level = new_level
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username} - {self.get_membership_level_display()}"
    def get_privileges(self):
        privileges = {
            "basic": {
                "max_books": 10,
                "max_days": 14,
                "free_extend": 0,
                "priority": False,
            },
            "standard": {
                "max_books": 20,
                "max_days": 30,
                "free_extend": 2,
                "priority": True,
            },
            "premium": {
                "max_books": "Không giới hạn",
                "max_days": 60,
                "free_extend": 5,
                "priority": True,
            },
        }
        return privileges.get(self.membership_level, {})

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
    