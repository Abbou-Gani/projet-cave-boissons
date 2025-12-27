from django.shortcuts import render
from django.http import HttpResponse 
from .models import Boisson

def accueil(request):
    boissons = Boisson.objects.all()
    return render(request, 'accueil.html', {'boissons': boissons})

def test_page(request):
    return HttpResponse("TEST RÉUSSI") 