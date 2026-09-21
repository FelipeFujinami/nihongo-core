from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER_CHOICES = [
        ('', 'Selecione uma opção'),
        ('Feminino', 'Feminino'),
        ('Masculino', 'Masculino'),
        ('Outro', 'Outro'),
        ('-', 'Prefiro não informar'),
    ]

    JLPT_CHOICES = [
        ('N5', 'N5'), 
        ('N4', 'N4'), 
        ('N3', 'N3'), 
        ('N2', 'N2'), 
        ('N1', 'N1'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    has_taken_jlpt = models.BooleanField(default=False)
    has_certificate = models.BooleanField(default=False)
    jlpt_level = models.CharField(max_length=2, choices=JLPT_CHOICES, blank=True)

    def __str__(self):
        return self.user.username