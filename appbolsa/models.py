from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class RespostasQuestionarioInicial(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    PERGUNTA_CHOICES = [
        ('S', 'Sim'),
        ('MM', 'Mais ou menos'),
        ('N', 'Não'),
    ]
    pergunta1 = models.CharField(max_length=2, choices=PERGUNTA_CHOICES, blank=False, null=False, )
    pergunta2 = models.CharField(max_length=2, choices=PERGUNTA_CHOICES, blank=False, null=False, )
    pergunta3 = models.CharField(max_length=2, choices=PERGUNTA_CHOICES, blank=False, null=False, )

    PERGUNTA4_CHOICES = [
        ('NA', 'Não organizo'),
        ('NAV', 'Não organizo, pois tenho acesso a valores financeiros muito baixos'),
        ('MS', 'Me organizo somente para os gastos mais altos'),
        ('RPM', 'Registro em planilhas todos os meus gastos mensais'),
        ('O', 'Outros'),
    ]
    pergunta4 = models.CharField(max_length=3, choices=PERGUNTA4_CHOICES, blank=False, null=False, )
    pergunta5 = models.CharField(max_length=2, choices=PERGUNTA_CHOICES, blank=False, null=False, )
    PERGUNTA6_CHOICES = [
        ('DGNI', 'Deixaria guardado e não investiria, pois desconheço qualquer tipo de investimento'),
        ('IB', 'Investiria em bens (casa, carro, apartamento, etc.)'),
        ('IA', 'Investiria em ações, pela possibilidade de altos ganhos, mesmo sabendo do risco elevado de perdas'),
        ('IRF', 'Investiria em renda fixa de risco médio, porém com retornos acima da inflação'),
        ('ITG', 'Investiria em títulos do governo, como títulos do Tesouro'),
        ('IP', 'Investiria em poupança, mesmo rendendo a mesma taxa de inflação, pois priorizo a segurança em relação ao meu dinheiro'),
    ]
    pergunta6 = models.CharField(max_length=4, choices=PERGUNTA6_CHOICES, blank=False, null=False, )
    pergunta7 = models.TextField(max_length=500)


class CustomUser(AbstractUser):
    is_answered = models.BooleanField(default=False)

    # Adicione related_name aos campos groups e user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="user",
    )