from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_request, name='register'),
    path('myaccount/', views.MyAccountView.as_view(), name='my-account'),
    path('my-actions', views.my_actions, name='my-actions'),
    path('questionario', views.questionario, name='questionario'),
    path('questionario/update', views.update_questionario, name='update-questionario'),
    path('resposta', views.questionario_resposta, name='questionario-resposta'),
    path('comparar-respostas-pdf', views.comparar_respostas_pdf, name='comparar-respostas-pdf'),
    path('sobre', views.sobre, name='sobre'),
    path('conceitos-basicos', views.conceitos_basicos, name='conceitos-basicos'),
    path('conceitos-intermediarios', views.conceitos_intermediarios, name='conceitos-intermediarios'),
    path('conceitos-avancados', views.conceitos_avancados, name='conceitos-avancados'),
    path('explorar-acoes', views.explorar_acoes, name='explorar-acoes'),
    path('explorar-moedas', views.explorar_moedas, name='explorar-moedas'),
    path('explorar-indices', views.explorar_indices, name='explorar-indices'),
]
