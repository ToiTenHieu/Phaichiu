from django.contrib import admin
from .models import UserProfile
from .models import Book 

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone', 'occupation', 'gender', 'date_of_birth', 'address','role')
    search_fields = ('name', 'user__username', 'phone', 'occupation', 'address')
    list_filter = ('gender', 'occupation')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Book)