from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail


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
