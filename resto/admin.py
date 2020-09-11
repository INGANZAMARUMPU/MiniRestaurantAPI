from django.contrib import admin
from .models import *

class PersonnelAdmin(admin.ModelAdmin):
	list_display = ("user", "tel", "avatar")
	list_filter = ("user", "tel")
	search_field = ("user", "tel")
	ordering = ("user", "tel")

class ServeurAdmin(admin.ModelAdmin):
	list_display = ("firstname", "lastname", "tel", "avatar")
	list_filter = ("firstname", "lastname", "tel")
	search_field = ("firstname", "lastname", "tel")
	ordering = ("firstname", "lastname", "tel")

class ProduitAdmin(admin.ModelAdmin):
	list_display = ("nom", "unite", "unite_sortant", "quantite")
	list_filter = ("nom", "unite", "unite_sortant", "quantite")
	search_field = ("nom", "unite", "unite_sortant")
	ordering = ("nom", "unite", "unite_sortant")

class OffreAdmin(admin.ModelAdmin):
	list_display = ('produit', 'fournisseur', "prix")
	list_filter = ('produit', 'fournisseur', "prix")
	search_field = ('produit', 'fournisseur', "prix")
	ordering = ('produit', 'fournisseur', "prix")

class StockAdmin(admin.ModelAdmin):
	list_display = ("produit", "quantite_initiale", "quantite_actuelle", "offre", "somme", "personnel", "date", "expiration_date")
	list_filter = ("produit", "quantite_initiale", "quantite_actuelle", "offre", "personnel", "date", "expiration_date")
	search_field = ("produit", "quantite_initiale", "quantite_actuelle", "offre", "personnel", "date", "expiration_date")
	ordering = ("produit", "quantite_initiale", "quantite_actuelle", "offre", "personnel", "date", "expiration_date")

	def somme(self, obj):
		return obj.somme()

class FournisseurAdmin(admin.ModelAdmin):
	list_display = ('nom', 'adresse', 'tel')
	list_filter = ('nom', 'adresse', 'tel')
	search_field = ('nom', 'adresse', 'tel')
	ordering = ('nom', 'adresse', 'tel')

class RecetteAdmin(admin.ModelAdmin):
	list_display = ("nom", "image", "details")
	list_filter = ("nom", "image", "details")
	search_field = ("nom", "image", "details")
	ordering = ("nom", "image", "details")

class CommandeAdmin(admin.ModelAdmin):
	list_display = ("table", "serveur", "date", "a_payer", "payee", "reste")
	list_filter = ("table", "serveur", "date", "a_payer", "payee", "reste")
	search_field = ("table", "serveur", "date", "a_payer", "payee", "reste")
	ordering = ("table", "serveur", "date", "a_payer", "payee", "reste")

class PaiementAdmin(admin.ModelAdmin):
	list_display = ("commande","somme","date")
	list_filter = ("commande","somme","date")
	search_field = ("commande","somme","date")
	ordering = ("commande","somme","date")

class PlaceAdmin(admin.ModelAdmin):
	list_display = ("nom",)
	list_filter = ("nom",)
	search_field = ("nom",)
	ordering = ("nom",)

class DetailCommandeAdmin(admin.ModelAdmin):
	list_display = ("recette", "commande", "quantite", "somme", "date")
	list_filter = ("recette", "commande", "quantite", "somme", "date")
	search_field = ("recette", "commande", "quantite", "somme", "date")
	ordering = ("recette", "commande", "quantite", "somme", "date")

admin.site.register(Produit, ProduitAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(Recette, RecetteAdmin)
admin.site.register(DetailCommande, DetailCommandeAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(Paiement, PaiementAdmin)
admin.site.register(Offre, OffreAdmin)
admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(Serveur, ServeurAdmin)
admin.site.register(Table)
admin.site.register(PrixRecette)
admin.site.register(DetailStock)
