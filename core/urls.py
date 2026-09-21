from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('dictionary/', include('dictionary.urls')),
    path('forum/', include('forum.urls')),
    path('chat/', include('chat.urls')),
    path('terms', TemplateView.as_view(template_name='legal/terms.html'), name='terms'),
    path('privacy-policy/', TemplateView.as_view(template_name='legal/privacy_policy.html'), name='privacy_policy'),
]
