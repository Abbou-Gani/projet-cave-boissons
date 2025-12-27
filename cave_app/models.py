from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Boisson(models.Model):
    VIN = 'VIN'
    BIERE = 'BIERE'
    SPIRITUEUX = 'SPIRITUEUX'
    SOFT = 'SOFT'
    CATEGORIES = [
        (VIN, 'Vin'),
        (BIERE, 'Bière'),
        (SPIRITUEUX, 'Spiritueux'),
        (SOFT, 'Boisson douce'),
    ]
    nom = models.CharField(max_length=200, verbose_name="Nom")
    categorie = models.CharField(max_length=20, choices=CATEGORIES, verbose_name="Catégorie")
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    seuil_alerte = models.PositiveIntegerField(default=5)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} - {self.categorie}"

    def stock_bas(self):
        return self.stock <= self.seuil_alerte

    class Meta:
        ordering = ['nom']
        verbose_name = "Boisson"
        verbose_name_plural = "Boissons"
 
class Commande(models.Model):
    EN_ATTENTE = 'EN_ATTENTE'
    CONFIRMEE = 'CONFIRMEE'
    LIVREE = 'LIVREE'
    ANNULEE = 'ANNULEE'

    STATUT_CHOICES = [
        (EN_ATTENTE, "En attente"),
        (CONFIRMEE, "Confirmée"),
        (LIVREE, "Livrée"),
        (ANNULEE, "Annulée"),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commandes")
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default=EN_ATTENTE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculer_total(self):
        total = sum(ligne.sous_total() for ligne in self.lignes.all())
        self.total = total
        self.save()
        return total
    
    def __str__(self):
        return f"Commande #{self.id} - {self.client.username}"

    class Meta:
        ordering = ['-date']
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        
class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    boisson = models.ForeignKey(Boisson, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def sous_total(self):
        return self.quantite * self.prix_unitaire

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.commande.calculer_total()

    def __str__(self):
        return f"{self.quantite} x {self.boisson.nom}"                