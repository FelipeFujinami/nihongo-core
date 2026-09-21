from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, label='Nome')
    last_name = forms.CharField(max_length=150, label='Sobrenome')
    email = forms.EmailField()

    date_of_birth = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    GENDER_CHOICES = [
        ('', 'Selecione uma opção'),
        ('Feminino', 'Feminino'),
        ('Masculino', 'Masculino'),
        ('Outro', 'Outro'),
        ('Prefiro não informar', 'Prefiro não informar'),
    ]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        label='Gênero',
        error_messages={'required': 'Por favor, selecione uma opção de gênero.'}
    )

    has_taken_jlpt = forms.BooleanField(required=False, label='Já fiz a prova do JLPT')
    has_certificate = forms.BooleanField(required=False, label='Fui aprovado(a) e tenho o certificado')

    JLPT_CHOICES = [
        ('N5', 'N5'), ('N4', 'N4'), ('N3', 'N3'), ('N2', 'N2'), ('N1', 'N1'),
    ]
    jlpt_level = forms.ChoiceField(choices=JLPT_CHOICES, required=False, label='Qual nível você foi aprovado?')

    accept_terms = forms.BooleanField(
        required=True,
        label='Li e aceito os Termos de Uso e a Política de Privacidade (LGPD)',
        error_messages={'required': 'Você precisa aceitar os termos e a política de privacidade (LGPD) para se cadastrar.'}
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'password1', 'password2',
            'has_taken_jlpt', 'has_certificate', 'jlpt_level',
            'accept_terms'
        ]

    def clean(self):
        cleaned_data = super().clean()
        has_taken_jlpt = cleaned_data.get('has_taken_jlpt')
        has_certificate = cleaned_data.get('has_certificate')
        jlpt_level = cleaned_data.get('jlpt_level')

        if has_certificate and not has_taken_jlpt:
            self.add_error('has_certificate', 'Isso não é possível sem ter feito a prova.')

        if has_taken_jlpt and has_certificate and not jlpt_level:
            self.add_error('jlpt_level', 'Selecione o nível que você foi aprovado.')

        return cleaned_data