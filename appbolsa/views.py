from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from .forms import RespostasQuestionarioInicialForm
from .models import RespostasQuestionarioInicial


def index(request):
    return render(request, 'index.html')


def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, " Ocorreu um erro ao cadastrar o usuário.")
    else:
        form = NewUserForm()
    context = {"form": form}
    return render(request=request, template_name="registration/register.html", context=context)


@receiver(user_logged_in)
def send_welcome_email(sender, user, request, **kwargs):
    # Verifique se é a primeira vez que o usuário faz login
    if user.last_login is None:
        # Enviar e-mail de boas-vindas
        send_mail(
            'Bem-vindo ao EducaBolsa+ ',
            'Olá, ' + user.first_name + '!\n\n' +
            'Seja bem-vindo ao EducaBolsa+! '
            'Estamos aqui para ajudar você a entender e explorar o mundo da bolsa de valores. \n\n'
            'Atenciosamente,\n\n'
            'Equipe do EducaBolsa+',
            'EducaBolsa+ <naoresponda@educabolsa.com>',
            [user.email],
            fail_silently=False,
        )


def my_actions(request):
    return render(request, 'my_actions.html')


class MyAccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'my_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

def sobre(request):
    return render(request, 'sobre.html')

def conceitos_basicos(request):
    return render(request, 'conceitos-basicos.html')

def conceitos_intermediarios(request):
    return render(request, 'conceitos-intermediarios.html')

def conceitos_avancados(request):
    return render(request, 'conceitos-avancados.html')

def explorar_acoes(request):
    return render(request, 'explorar-acoes.html')

def explorar_moedas(request):
    return render(request, 'explorar-moedas.html')

def explorar_indices(request):
    return render(request, 'explorar-indices.html')

def questionario(request):
    if request.method == 'POST':
        form = RespostasQuestionarioInicialForm(request.POST)
        if form.is_valid():
            form.instance.usuario = request.user
            form.save()
            request.user.is_answered = True
            request.user.save()
            return redirect('questionario-resposta')
    else:
        form = RespostasQuestionarioInicialForm()

    return render(request, 'questionario.html', {'form': form})

def questionario_resposta(request):
    respostas = RespostasQuestionarioInicial.objects.filter(usuario=request.user).last()
    return render(request, 'questionario-resposta.html', {'respostas': respostas})