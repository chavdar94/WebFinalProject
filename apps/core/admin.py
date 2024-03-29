from django.contrib import admin

from django.contrib.auth import admin as auth_admin, get_user_model
from .forms import RegisterForm
from .models import UserProfile
from ..forum.models import Like

UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    model = UserProfile


@admin.register(UserModel)
class AppUserAdmin(auth_admin.UserAdmin):
    ordering = ('pk', 'email',)
    list_display = ('pk', 'email', 'date_joined', 'last_login',
                    'is_superuser', 'is_staff')
    list_filter = ()
    add_form = RegisterForm
    inlines = auth_admin.UserAdmin = (ProfileInline,)
    search_fields = ('email',)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
