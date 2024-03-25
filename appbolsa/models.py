from django.db import models
from django.contrib.auth.models import User

class RespostasQuestionarioInicial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    PERGUNTA_CHOICES = [
        ('S', 'Sim'),
        ('MM', 'Mais ou menos'),
        ('N', 'Não'),
    ]
    pergunta1 = models.CharField(max_length=2, choices=PERGUNTA_CHOICES)
    pergunta2 = models.CharField(max_length=2, choices=PERGUNTA_CHOICES)
    pergunta3 = models.CharField(max_length=2, choices=PERGUNTA_CHOICES)

    PERGUNTA4_CHOICES = [
        ('NA', 'Não organizo'),
        ('NAV', 'Não organizo, pois tenho acesso a valores financeiros muito baixos'),
        ('MS', 'Me organizo somente para os gastos mais altos'),
        ('RPM', 'Registro em planilhas todos os meus gastos mensais'),
        ('O', 'Outros'),
    ]
    pergunta4 = models.CharField(max_length=3, choices=PERGUNTA4_CHOICES)
    pergunta5 = models.CharField(max_length=2, choices=PERGUNTA_CHOICES)
    PERGUNTA6_CHOICES = [
        ('DGNI', 'Deixaria guardado e não investiria, pois desconheço qualquer tipo de investimento'),
        ('IB', 'Investiria em bens (casa, carro, apartamento, etc.)'),
        ('IA', 'Investiria em ações, pela possibilidade de altos ganhos, mesmo sabendo do risco elevado de perdas'),
        ('IRF', 'Investiria em renda fixa de risco médio, porém com retornos acima da inflação'),
        ('ITG', 'Investiria em títulos do governo, como títulos do Tesouro, mesmo com possíveis turbulências governamentais e/ou crise instalada no país'),
        ('IP', 'Investiria em poupança, mesmo rendendo a mesma taxa de inflação, pois priorizo a segurança em relação ao meu dinheiro'),
    ]
    pergunta6 = models.CharField(max_length=4, choices=PERGUNTA6_CHOICES)
    pergunta7 = models.TextField()
