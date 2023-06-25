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
    ordering = ('email',)
    list_display = ('email', 'date_joined', 'last_login')
    list_filter = ()
    add_form = RegisterForm
    inlines = auth_admin.UserAdmin = (ProfileInline,)

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
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
