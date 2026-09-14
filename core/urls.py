from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('dictionary/', include('dictionary.urls')),
    path('forum/', include('forum.urls')),
    path('chat/', include('chat.urls')),
]
