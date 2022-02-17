from .dependancies import *

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
					A.id, A.nom, SUM(B.quantite) AS quantite,
					SUM(B.quantite*A.prix) AS total 
				FROM 
					resto_detailcommande AS B, resto_recette AS A
				WHERE
					date between "{du}" AND "{au}" AND
					A.id = B.recette_id
				GROUP BY B.recette_id;
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
