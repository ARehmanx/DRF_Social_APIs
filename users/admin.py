from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):
#
#     form = UserChangeForm
#     add_form = UserCreationForm
#     fieldsets = (
#                     ("User", {"fields": ("name", "profile_picture")}),
#                 ) + auth_admin.UserAdmin.fieldsets
#     list_display = ["id", "email", "name", "is_superuser"]
#     ordering = ["-id"]
#     search_fields = ["name", "email"]
#     list_per_page = 50
