from .dependancies import *

class DetailCommandeViewset(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = DetailCommande.objects.select_related("commande", "recette")
	serializer_class = DetailCommandeSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter]
	search_fields = []
	filterset_fields = {
		'recette': ['exact'],
		'recette__nom': ['icontains'],
		'date': ['gte', 'lte', 'range'],
	}

	@action(methods=['GET'], detail=False, url_name=r'stats', url_path=r"stats")
	def statistiques(self, request):
		dates = request.GET.get("date__range")
		date_req = ""
		if dates:
			dates = dates.split(",")
			date_req = f"AND date BETWEEN '{dates[0]}' AND '{dates[1]}'"
		queryset = self.get_queryset()
		query = """
			SELECT
				resto_recette.id,
				resto_recette.nom,
				COUNT(resto_detailcommande.recette_id) AS fois,
				MIN(resto_detailcommande.date) AS du,
				MAX(resto_detailcommande.date) AS au,
				SUM(resto_detailcommande.quantite) AS quantite,
				SUM(resto_detailcommande.somme) AS prix
			FROM ({}) as resto_detailcommande, resto_recette
			WHERE
				resto_detailcommande.recette_id = resto_recette.id
				{}
			GROUP BY resto_detailcommande.recette_id
			ORDER BY resto_detailcommande.somme DESC
		""".format(str(queryset.query), date_req)
		print(query)
		stats = queryset.raw(query)
		serializer = StatRecetteSerializer(stats, many=True)
		return Response(serializer.data, 200)


