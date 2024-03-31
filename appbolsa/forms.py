from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import RespostasQuestionarioInicial, CustomUser



class NewUserForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=3, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Primeiro nome', max_length=150)
    last_name = forms.CharField(label='Último nome', max_length=150)

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name',)

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = CustomUser.objects.filter(username=username)
        if new.count():
            raise ValidationError("Usuário já cadastrado.")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = CustomUser.objects.filter(email=email)
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
        user = CustomUser.objects.create_user(
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


class RespostasQuestionarioInicialForm(forms.ModelForm):
    pergunta1 = forms.ChoiceField(choices=RespostasQuestionarioInicial.PERGUNTA_CHOICES, widget=forms.RadioSelect,
                                  initial='S', label='1. Você se sente seguro para efetuar cálculos envolvendo matemática financeira?')

    pergunta2 = forms.ChoiceField(choices=RespostasQuestionarioInicial.PERGUNTA_CHOICES, widget=forms.RadioSelect,
                                    initial='S', label='2. Na sua opinião, o conhecimento matemático \n pode ajudar a lidar melhor com o dinheiro?')

    pergunta3 = forms.ChoiceField(choices=RespostasQuestionarioInicial.PERGUNTA_CHOICES, widget=forms.RadioSelect,
                                    initial='S', label='3. Qual o grau de importância que você \n atribui à Educação Financeira nas escolas?')

    pergunta4 = forms.ChoiceField(choices=RespostasQuestionarioInicial.PERGUNTA4_CHOICES, widget=forms.RadioSelect,
                                    initial='NA', label='4. Como você organiza seus gastos?')

    pergunta5 = forms.ChoiceField(choices=RespostasQuestionarioInicial.PERGUNTA_CHOICES, widget=forms.RadioSelect,
                                    initial='S', label='5. Você conhece a dinâmica da Bolsa de Valores de São Paulo [B3]?')

    pergunta6 = forms.ChoiceField(choices=RespostasQuestionarioInicial.PERGUNTA6_CHOICES, widget=forms.RadioSelect,
                                    initial='DGNI', label='6. Se você tivesse dinheiro para investir, \n em qual das alternativas adiante você investiria?')

    pergunta7 = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), label='7. Resolução de Problema: Suponha-se que você tenha um capital R$2.000,00  \n e pretende investir seu dinheiro numa Renda Fixa que rende 12% ao ano, pergunta-se: \n ao final de 30 meses qual será o valor do seu capital?')


    class Meta:
        model = RespostasQuestionarioInicial
        fields = ['pergunta1', 'pergunta2', 'pergunta3', 'pergunta4', 'pergunta5', 'pergunta6', 'pergunta7']


