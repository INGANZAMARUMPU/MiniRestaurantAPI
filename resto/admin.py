from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
	list_display = ("user", "tel", "avatar")
	list_filter = ("user", "tel")
	search_field = ("user", "tel")
	ordering = ("user", "tel")

@admin.register(Serveur)
class ServeurAdmin(admin.ModelAdmin):
	list_display = ("firstname", "lastname", "tel", "avatar")
	list_filter = ("firstname", "lastname", "tel")
	search_field = ("firstname", "lastname", "tel")
	ordering = ("firstname", "lastname", "tel")

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
	list_display = ("nom", "unite", "unite_sortant", "quantite")
	list_filter = ("nom", "unite", "unite_sortant", "quantite")
	search_field = ("nom", "unite", "unite_sortant")
	ordering = ("nom", "unite", "unite_sortant")

@admin.register(Recette)
class RecetteAdmin(admin.ModelAdmin):
	list_display = ("nom", "dispo", "prix", "details")
	list_filter = ("nom", "prix", "details")
	search_field = ("nom", "dispo", "prix", "details")
	ordering = ("nom", "prix", "details")

	def dispo(self, obj):
		value = False
		if(obj.produit):
			value = obj.produit.quantite > 0
		else:
			value = obj.disponible
		if value:
			return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
		return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
	list_display = ("table", "serveur", "personnel", "date", "a_payer", "payee", "reste")
	list_filter = ("table", "serveur", "personnel", "date", "payee", "reste")
	search_field = ("table", "serveur", "personnel", "date", "a_payer", "payee", "reste")
	ordering = ("table", "serveur", "personnel", "date", "payee", "reste")

	select_related = True

	def a_payer(self, obj):
		return obj.a_payer()

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
	list_display = ("commande","somme","date")
	list_filter = ("commande","somme","date")
	search_field = ("commande","somme","date")
	ordering = ("commande","somme","date")

	select_related = True

@admin.register(DetailCommande)
class DetailCommandeAdmin(admin.ModelAdmin):
	list_display = ("recette", "commande", "quantite", "somme", "date")
	list_filter = ("recette", "commande", "quantite", "somme", "date")
	search_field = ("recette", "commande", "quantite", "somme", "date")
	ordering = ("recette", "commande", "quantite", "somme", "date")

	select_related = True

@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
	list_display = "produit", "prix", "quantite", "personnel", "date"
	list_filter = "produit", "prix", "quantite", "personnel", "date"
	search_field = "produit", "prix", "quantite", "personnel", "date"
	ordering = "produit", "prix", "quantite", "personnel", "date"

	select_related = True

admin.site.register(Table)
admin.site.register(PrixRecette)
