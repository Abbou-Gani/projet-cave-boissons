from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),  # Page d'accueil
    path('test/', views.test_page, name='test'),
]