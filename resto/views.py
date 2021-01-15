from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from django.db.models import Count, F
from django.db import connection

from datetime import datetime, date, timedelta

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

class AchatViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Achat.objects.select_related("produit", "personnel")
	serializer_class = AchatSerializer

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

class CommandeViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Commande.objects.select_related("table", "serveur", "personnel")
	serializer_class = CommandeSerializer

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
