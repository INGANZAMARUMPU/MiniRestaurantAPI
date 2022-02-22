from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ProduitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Produit
		fields = "__all__"

class ServeurSerializer(serializers.ModelSerializer):
	class Meta:
		model = Serveur
		fields = "__all__"

class ClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields = "__all__"

class TableSerializer(serializers.ModelSerializer):
	class Meta:
		model = Table
		fields = "__all__"

class AchatSerializer(serializers.ModelSerializer):

	def to_representation(self, obj):
		data = super().to_representation(obj)
		data["produit"] = str(obj.produit)
		data["user"] = f"{obj.user.first_name} {obj.user.last_name}"
		return data

	class Meta:
		model = Achat
		fields = "__all__"
		read_only_fields = "user", 

class SortieSerializer(serializers.ModelSerializer):

	def to_representation(self, obj):
		data = super().to_representation(obj)
		data["produit"] = str(obj.produit)
		data["user"] = f"{obj.user.first_name} {obj.user.last_name}"
		return data

	class Meta:
		model = Sortie
		fields = "__all__"
		read_only_fields = "user", 

class PaiementSerializer(serializers.ModelSerializer):
	date = serializers.SerializerMethodField()

	def get_date(self, obj):
		return str(obj.date)

	class Meta:
		model = Paiement
		fields = "__all__"

class RecetteSerializer(serializers.ModelSerializer):
	disponible = serializers.SerializerMethodField()

	def get_disponible(self, obj):
		if(obj.produit):
			return obj.produit.quantite > 0
		return obj.disponible

	class Meta:
		model = Recette
		fields = "__all__"
		read_only_fields = 'produit', 

class DetailCommandeSerializer(serializers.ModelSerializer):
	nom = serializers.SerializerMethodField()
	prix = serializers.SerializerMethodField()
	
	def get_nom(self, obj):
		if(obj.recette):
			return obj.recette.nom
		return ""

	def get_prix(self, obj):
		if(obj.recette):
			return obj.recette.prix
		return ""

	class Meta:
		model = DetailCommande
		fields = "__all__"

class CommandeSerializer(serializers.ModelSerializer):
	details = DetailCommandeSerializer(many=True, read_only=True)

	class Meta:
		model = Commande
		fields = "__all__"

	def to_representation(self, obj):
		representation = super().to_representation(obj)
		representation['user'] = f"{obj.user.first_name} {obj.user.last_name}"
		representation['serveur'] = str(obj.serveur)
		return representation

class ServiceSerializer(serializers.Serializer):
	nom = serializers.CharField()
	prenom = serializers.CharField()
	fois = serializers.IntegerField()
	du = serializers.DateTimeField()
	au = serializers.DateTimeField()
	prix = serializers.IntegerField()
	payee = serializers.IntegerField()

class StatRecetteSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	nom = serializers.CharField()
	fois = serializers.IntegerField()
	du = serializers.DateTimeField()
	au = serializers.DateTimeField()
	quantite = serializers.IntegerField()
	prix = serializers.IntegerField()

class TokenPairSerializer(TokenObtainPairSerializer):

	def validate(self, attrs):
		data = super(TokenPairSerializer, self).validate(attrs)
		data['services'] = [group.name for group in self.user.groups.all()]
		data['is_admin'] = self.user.is_superuser
		data['id'] = self.user.id
		return data