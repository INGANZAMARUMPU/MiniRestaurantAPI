from .models import *
from rest_framework import serializers

class ProduitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Produit
		fields = "__all__"

class StockSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stock
		fields = "__all__"

class FournisseurSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fournisseur
		fields = "__all__"

class RecetteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recette

class DetailCommandeSerializer(serializers.ModelSerializer):
	nom = serializers.SerializerMethodField()
	def get_nom(self, obj):
		return obj.recette.nom

	class Meta:
		model = DetailCommande
		fields = "id", "quantite", "somme", "pret", "commande", "recette", 'nom', 'obligations'
		fields = "__all__"

class CommandeSerializer(serializers.ModelSerializer):
	details = DetailCommandeSerializer(many=True, read_only=True)
	class Meta:
		model = Commande
		fields = ("table", "details", "tel", "date", "servi", "commandee", "pret", "a_payer", "payee", "reste", "serveur")