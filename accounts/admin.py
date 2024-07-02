from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, OTP
from .forms import UserCreationForm, UserChangeForm


admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin panel for user management with add and change forms plus password
    """
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ("email", "username", "is_verified", "is_superuser", "is_active")
    list_filter = ("is_superuser", "is_active", "is_verified")
    searching_fields = ("email", "username")
    actions = ('make_verify', )
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("username", "email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("user_permissions", ),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """
    """
    list_display = ("user_email", "code", "created_date")
    list_filter = ("created_date", )
    search_fields = ("user__email", "code")

    def user_phone_number(self, obj):
        return str(obj.user.phone_number) if obj.user.phone_number else '-'

    def user_email(self, obj):
        return str(obj.user.email)
