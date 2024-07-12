from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from blog.models import Blog
from users.models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "avatar", "phone", "is_superuser")
    search_fields = ("phone_number", "first_name", "last_name")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    exclude = ('content_id', )
    search_fields = ('user',)
