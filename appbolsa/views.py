from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from .forms import RespostasQuestionarioInicialForm
from .models import RespostasQuestionarioInicial
import seaborn
from bcb import sgs


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


@login_required(login_url='/login/')
def questionario(request):
    if request.method == 'POST':
        form = RespostasQuestionarioInicialForm(request.POST)
        if form.is_valid():
            request.user.is_answered = True
            request.user.save()  # Salve o CustomUser antes de tentar salvar o formulário

            respostas = RespostasQuestionarioInicial(**form.cleaned_data, usuario=request.user)
            respostas.save()

            return redirect('questionario-resposta')
    else:
        form = RespostasQuestionarioInicialForm()

    return render(request, 'questionario.html', {'form': form})


def questionario_resposta(request):
    respostas = RespostasQuestionarioInicial.objects.filter(usuario=request.user).last()
    # Buscar todas as respostas do questionário
    todas_respostas = RespostasQuestionarioInicial.objects.all()
    return render(request, 'questionario-resposta.html', {'respostas': respostas})


def update_questionario(request):
    respostas = RespostasQuestionarioInicial.objects.filter(usuario=request.user).last()
    if request.method == 'POST':
        form = RespostasQuestionarioInicialForm(request.POST, instance=respostas)
        if form.is_valid():
            form.save()
            return redirect('questionario-resposta')
    else:
        form = RespostasQuestionarioInicialForm(instance=respostas)

    return render(request, 'questionario.html', {'form': form})


def comparar_respostas_pdf(request):
    # Fetch all the responses to the questionnaire
    todas_respostas = RespostasQuestionarioInicial.objects.all()

    # Prepare the data for the plot
    dados = {}
    for resposta in todas_respostas:
        for field in resposta._meta.get_fields():
            if field.name not in ['id', 'usuario']:
                if field.name not in dados:
                    dados[field.name] = {}
                if getattr(resposta, field.name) not in dados[field.name]:
                    dados[field.name][getattr(resposta, field.name)] = 0
                dados[field.name][getattr(resposta, field.name)] += 1

    # Mapping of abbreviations to full form
    full_form_mapping = {
        'S': 'Sim',
        'MM': 'Mais ou menos',
        'N': 'Não',
        'NA': 'Não organizo',
        'NAV': 'Não organizo, pois tenho acesso a valores financeiros muito baixos',
        'MS': 'Me organizo somente para os gastos mais altos',
        'RPM': 'Registro em planilhas todos os meus gastos mensais',
        'O': 'Outros',
        'DGNI': 'Deixaria guardado e não investiria, pois desconheço qualquer tipo de investimento',
        'IB': 'Investiria em bens (casa, carro, apartamento, etc.)',
        'IA': 'Investiria em ações, pela possibilidade de altos ganhos, mesmo sabendo do risco elevado de perdas',
        'IRF': 'Investiria em renda fixa de risco médio, porém com retornos acima da inflação',
        'ITG': 'Investiria em títulos do governo, como títulos do Tesouro, mesmo com possíveis turbulências governamentais e/ou crise instalada no país',
        'IP': 'Investiria em poupança, mesmo rendendo a mesma taxa de inflação, pois priorizo a segurança em relação ao meu dinheiro',
        # Add other mappings here
    }

    # Generate the plot
    fig, axs = plt.subplots(len(dados) - 1, 1, figsize=(8, 4 * (len(dados) - 1)))  # Adjust the size of the plot
    fig.suptitle('GRÁFICO DE RESPOSTAS', fontsize=16)  # Add a title to the document
    plt.subplots_adjust(hspace=0.5)  # Add space between subplots

    for i, (pergunta, opcoes) in enumerate(dados.items()):
        if i == 6:  # index 6 corresponds to the 7th graph
            continue

        # Replace abbreviations with full form
        opcoes = {full_form_mapping.get(key, key): value for key, value in opcoes.items()}

        # Generate a list of colors
        cores = seaborn.color_palette('hsv', len(opcoes))

        bars = axs[i if i < 6 else i - 1].bar(opcoes.keys(), opcoes.values(), width=0.5,
                                              color=cores)  # Set bar width to 0.5 and add colors
        axs[i if i < 6 else i - 1].set_title(
            RespostasQuestionarioInicialForm().fields[pergunta].label,
            weight='bold')  # Set the title to the label of the form field
        axs[i if i < 6 else i - 1].yaxis.set_major_locator(
            MaxNLocator(integer=True))  # Set y-axis to display only integers
        axs[i if i < 6 else i - 1].set_ylabel('número de pessoas', fontsize=12)  # Set y-axis label
        axs[i if i < 6 else i - 1].grid(axis='y')  # Add a horizontal grid

        # Add legend for graph 6
        if i == 5:  # index 5 corresponds to the 6th graph

            axs[i].legend(bars, opcoes.keys(), loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True,
                          shadow=True, ncol=1, fontsize=8)  # Add legend
            axs[i].set_xticklabels([])  # Remove x-axis labels

    # Save the plot to a BytesIO object as a PDF
    buf = BytesIO()
    plt.savefig(buf, format='pdf')
    buf.seek(0)

    # Create a response with the PDF
    return FileResponse(buf, as_attachment=True, filename='comparar_respostas.pdf')


def explorar_indices(request):
    # Get the SELIC rate
    taxa_selic_atual = "{:.2f}".format(sgs.get(4189).iloc[-1, 0])
    taxa_selic_meta = "{:.2f}".format(sgs.get(432).iloc[-1, 0])

    return render(request, 'explorar-indices.html',
                  {'taxa_selic_atual': taxa_selic_atual, 'taxa_selic_meta': taxa_selic_meta})
