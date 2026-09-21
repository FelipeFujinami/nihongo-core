from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.register, name='register'),
    path('entrar/', views.login_view, name='login'),
    path('entrar/verificar-acesso/', views.verify_2fa, name='verify_2fa'),
    path('sair/', views.logout_view, name='logout'),
]