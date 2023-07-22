from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls import handler500, handler400, handler403
from ..apps.core.views import bad_request, permission_denied, server_error


urlpatterns = [
    # Django Jet Admin customization
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    # project urls
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.core.urls')),
    path('forum/', include('apps.forum.urls')),
    # password reset urls
    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]

if not settings.DEBUG:
    handler400 = bad_request
    handler403 = permission_denied
    handler500 = server_error

if settings.DEBUG:
    from django.conf.urls.static import static

    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
