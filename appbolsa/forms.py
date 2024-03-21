from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
class NewUserForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=3, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Primeiro nome', max_length=150)
    last_name = forms.CharField(label='Último nome', max_length=150)

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("Usuário já cadastrado.")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email já cadastrado.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Senhas não conferem.")
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].capitalize()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].capitalize()
        return last_name

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )

        # Send welcome email after user creation
        send_mail(
            'Bem-vindo ao EducaBolsa+ ',
            'Olá, ' + self.cleaned_data['first_name'] + '!\n\n' +
            'Seja bem-vindo ao EducaBolsa+! '
            'Estamos aqui para ajudar você a entender e explorar o mundo da bolsa de valores. \n\n'
            'Atenciosamente,\n\n'
            'Equipe do EducaBolsa+',
            'EducaBolsa+ <naoresponda@educabolsa.com>',
            [self.cleaned_data['email']],
            fail_silently=False,
        )

        return user
