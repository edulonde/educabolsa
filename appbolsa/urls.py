from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_request, name='register'),
    path('myaccount/', views.MyAccountView.as_view(), name='my-account'),
    path('my-actions', views.my_actions, name='my-actions'),
]
