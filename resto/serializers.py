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
	personnel = serializers.SerializerMethodField()

	def get_personnel(self, obj):
		return str(obj.personnel)

	def to_representation(self, obj):
		data = super().to_representation(obj)
		data["produit"] = str(obj.produit)
		return data

	class Meta:
		model = Achat
		fields = "__all__"

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
			print(obj.produit)
			return obj.produit.quantite > 0
		return obj.disponible

	class Meta:
		model = Recette
		fields = "id","nom", "image", "details", "prix", "disponible", "produit"
		read_only_fields = 'produit', 

class DetailCommandeSerializer(serializers.ModelSerializer):
	nom = serializers.SerializerMethodField()
	prix = serializers.SerializerMethodField()
	
	def get_nom(self, obj):
		return obj.recette.nom

	def get_prix(self, obj):
		return obj.recette.prix

	class Meta:
		model = DetailCommande
		fields = "__all__"

class CommandeSerializer(serializers.ModelSerializer):
	details = DetailCommandeSerializer(many=True, read_only=True)
	a_payer = serializers.SerializerMethodField()
	serveur_name = serializers.SerializerMethodField()

	class Meta:
		model = Commande
		fields = "__all__"

	def get_a_payer(self, obj):
		return obj.a_payer()

	def get_serveur_name(self, obj):
		return str(obj.serveur)

class TokenPairSerializer(TokenObtainPairSerializer):
	
	# @classmethod
	# def get_token(cls, user):
	# 	token = super(TokenPairSerializer, cls).get_token(user)
	# 	token['services'] = [group.name for group in user.groups.all()]
	# 	try:
	# 		token['username'] = user.username
	# 		token['phone'] = user.profile.phone
	# 		token['email'] = user.email
	# 	except Exception as e:
	# 		print(e)
	# 	return token

	def validate(self, attrs):
		data = super(TokenPairSerializer, self).validate(attrs)
		data['services'] = [group.name for group in self.user.groups.all()]
		data['is_admin'] = self.user.is_superuser
		data['id'] = self.user.personnel.id
		return data