from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from apps.core.views import PasswordResetView, PasswordResetDone, PasswordResetConfirm, PasswordResetComplete
# from django.conf.urls import handler500, handler400, handler403


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
    path('reset_password/', PasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_sent/', PasswordResetDone.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetComplete.as_view(),
         name='password_reset_complete'),
]

if not settings.DEBUG:
    handler400 = 'apps.core.views.bad_request'
    handler403 = 'apps.core.views.permission_denied'
    handler500 = 'apps.core.views.server_error'

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
