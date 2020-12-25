from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from django.db.models import Count, F

from .models import *
from .serializers import *

class TokenPairView(TokenObtainPairView):
	serializer_class = TokenPairSerializer

class ProduitViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Produit.objects.all()
	serializer_class = ProduitSerializer

class ServeurViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Serveur.objects.all()
	serializer_class = ServeurSerializer

class TableViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Table.objects.all()
	serializer_class = TableSerializer

class DetailStockViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = DetailStock.objects.select_related("stock", "personnel")
	serializer_class = DetailStockSerializer

class DetailCommandeViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = DetailCommande.objects.select_related("commande", "recette")
	serializer_class = DetailCommandeSerializer

class PaiementViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Paiement.objects.select_related("produit", "fournisseur")
	serializer_class = PaiementSerializer

class FournisseurViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Fournisseur.objects.all()
	serializer_class = FournisseurSerializer

class RecetteViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Recette.objects.all()
	serializer_class = RecetteSerializer

class CommandeViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Commande.objects.select_related("table", "serveur", "personnel")
	serializer_class = CommandeSerializer
