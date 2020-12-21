from .models import *
from rest_framework import serializers

class ProduitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Produit
		fields = "__all__"

class ServeurSerializer(serializers.ModelSerializer):
	class Meta:
		model = Serveur
		fields = "__all__"

class TableSerializer(serializers.ModelSerializer):
	class Meta:
		model = Table
		fields = "__all__"

class DetailStockSerializer(serializers.ModelSerializer):
	class Meta:
		model = DetailStock
		fields = "__all__"

class OffreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Offre
		fields = "__all__"

class PaiementSerializer(serializers.ModelSerializer):
	class Meta:
		model = Paiement
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
		fields = "__all__"

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
		fields = "__all__"