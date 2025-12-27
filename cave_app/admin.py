from django.contrib import admin
from .models import Boisson, Commande, LigneCommande

# Register your models here.
admin.site.register(Boisson)
admin.site.register(Commande)
admin.site.register(LigneCommande)

