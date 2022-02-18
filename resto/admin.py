from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Serveur)
class ServeurAdmin(admin.ModelAdmin):
	list_display = ("firstname", "lastname", "tel", "avatar")
	list_filter = ("firstname", "lastname", "tel")
	search_field = ("firstname", "lastname", "tel")
	ordering = ("firstname", "lastname", "tel")

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ("nom", "tel")
	list_filter = ("nom", "tel")
	search_field = ("nom", "tel")
	ordering = ("nom", "tel")

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
	list_display = ("table", "serveur", "user", "date", "a_payer", "payee")
	list_filter = ("table", "serveur", "user", "date", "payee")
	search_field = ("table", "serveur", "user", "date", "a_payer", "payee")
	ordering = ("table", "serveur", "user", "date", "payee")

	select_related = True

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
	list_display = "produit", "prix", "quantite", "user", "date"
	list_filter = "produit", "prix", "quantite", "user", "date"
	search_field = "produit", "prix", "quantite", "user", "date"
	ordering = "produit", "prix", "quantite", "user", "date"

	select_related = True

	@transaction.atomic
	def delete_queryset(self, request, queryset):
		for achat in queryset:
			produit:Produit = achat.produit
			if produit:
				produit.quantite -= achat.quantite
				produit.save()
		queryset.delete()

	@transaction.atomic
	def delete_model(self, request, obj):
		produit:Produit = obj.produit
		if produit:
			produit.quantite -= obj.quantite
			produit.save()
		obj.delete()

@admin.register(Sortie)
class SortieAdmin(admin.ModelAdmin):
	list_display = "produit", "quantite", "user", "date"
	list_filter = "produit", "quantite", "user", "date"
	search_field = "produit", "quantite", "user", "date"
	ordering = "produit", "quantite", "user", "date"

	select_related = True

	@transaction.atomic
	def delete_queryset(self, request, queryset):
		for sortie in queryset:
			produit:Produit = sortie.produit
			produit.quantite += sortie.quantite
			produit.save()
		queryset.delete()

	@transaction.atomic
	def delete_model(self, request, obj):
		produit:Produit = obj.produit
		produit.quantite += obj.quantite
		produit.save()
		obj.delete()

admin.site.register(Table)
