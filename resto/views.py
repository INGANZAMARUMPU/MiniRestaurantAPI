from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from django.db import connection, transaction, IntegrityError

from datetime import datetime, date, timedelta

import traceback, sys

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

	def destroy(self, request, *args, **kwargs):
		serveur = self.get_object()
		serveur.is_active = False
		serveur.save()
		return Response({'status': 'success'}, 204)

class ClientViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Client.objects.all()
	serializer_class = ClientSerializer

class TableViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Table.objects.all()
	serializer_class = TableSerializer

class AchatViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Achat.objects.select_related("produit", "personnel")
	serializer_class = AchatSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		data = request.data
		try:
			achat = Achat(
				produit = Produit.objects.get(id=data["produit"]),
				quantite = float(data["quantite"]),
				prix = float(data["prix"]),
				personnel = request.user.personnel
			)
			achat.save()
			serializer = self.serializer_class(achat, many=False)
			return Response(serializer.data, 201)
		except:
			traceback.print_exception(*sys.exc_info()) 
			return Response({'status': 'Quelque chose d\'incorrect'}, 400)

class DetailCommandeViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = DetailCommande.objects.select_related("commande", "recette")
	serializer_class = DetailCommandeSerializer

class PaiementViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Paiement.objects.select_related("commande")
	serializer_class = PaiementSerializer

class RecetteViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Recette.objects.select_related("produit")
	serializer_class = RecetteSerializer

	def destroy(self, request, *args, **kwargs):
		recette = self.get_object()
		recette.is_active = False
		recette.save()
		return Response({'status': 'success'}, 204)

class CommandeViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Commande.objects.select_related("table", "serveur", "personnel")
	serializer_class = CommandeSerializer

	def list(self, request, *args, **kwargs):
		params = request.query_params
		unpaid = params.get("unpaid")
		if(unpaid):
			self.queryset = self.queryset.filter(
				table__id=unpaid, reste__gt=0.
			)
		return super().list(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):
		data = request.data
		try:
			with transaction.atomic():
				dict_client = data.get("client")
				client = None
				if(dict_client and dict_client.get("tel")):
					client, created = Client.objects.get_or_create(
						tel = dict_client.get("tel")
					)
					if(not client.nom):
						client.nom = dict_client.get("nom")
						client.save()
				commande = Commande(
					personnel = request.user.personnel,
					client = client,
					serveur = Serveur.objects.get(id=data.get("serveur"))
				)
				commande.save()
				for item in data.get("items"):
					recette = Recette.objects.get(id=item.get("recette"))
					DetailCommande(
						recette = recette, commande = commande,
						quantite=item.get("quantite")
					).save()
				payee = int(data.get("payee"))
				if payee:
					Paiement(commande=commande, somme=payee, validated=True).save()
				serializer = self.serializer_class(commande, many=False)
				return Response(serializer.data, 201)
		except Exception:
			traceback.print_exception(*sys.exc_info()) 
			return Response({'status': 'Quelque chose d\'incorrect'}, 400)

class StatisticViewset(viewsets.ViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]

	@action(methods=['GET'], detail=False,url_name="menu", url_path=r'menu')
	def todayMenu(self, request):
		la_date = date.today().strftime("%Y-%m-%d")
		return self.menu(request, la_date, la_date)

	@action(methods=['GET'], detail=False,url_name="service", url_path=r'service')
	def todayService(self, request):
		la_date = date.today().strftime("%Y-%m-%d")
		return self.service(request, la_date, la_date)

	@action(methods=['GET'], detail=False,url_name="menu",
		url_path=r'menu/(?P<du>\d{4}-\d{2}-\d{2})/(?P<au>\d{4}-\d{2}-\d{2})')
	def menu(self, request, du, au):
		du = datetime.strptime(du, "%Y-%m-%d").date()
		au = datetime.strptime(au, "%Y-%m-%d").date()+timedelta(days=1)
		details = []
		with connection.cursor() as cursor:
			cursor.execute(f"""
				SELECT
					A.id, A.nom, SUM (B.quantite) AS quantite 
				FROM 
					resto_detailcommande AS B, resto_recette AS A
				WHERE
					date between "{du}" AND "{au}" AND
					A.id = B.recette_id
				GROUP BY A.id;
			""")
			columns = [col[0] for col in cursor.description]
			details = [
				dict(zip(columns, row))
				for row in cursor.fetchall()
			]
		return Response(details)

	@action(methods=['GET'], detail=False, url_name=r'service',
		url_path=r"service/(?P<du>\d{4}-\d{2}-\d{2})/(?P<au>\d{4}-\d{2}-\d{2})")
	def service(self, request, du, au):
		du = datetime.strptime(du, "%Y-%m-%d").date()
		au = datetime.strptime(au, "%Y-%m-%d").date()+timedelta(days=1)
		details = []
		with connection.cursor() as cursor:
			cursor.execute(f"""SELECT
				A.id, A.firstname, A.lastname, COUNT(B.id) as quantite
			FROM 
				resto_commande AS B, resto_serveur AS A
			WHERE
				date between "{du}" AND "{au}" AND
				A.id = B.serveur_id
			GROUP BY A.id;
			""")
			columns = [col[0] for col in cursor.description]
			details = [
				dict(zip(columns, row))
				for row in cursor.fetchall()
			]
		return Response(details)
