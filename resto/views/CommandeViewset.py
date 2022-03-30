from .dependancies import *

class CommandeViewset(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Commande.objects.select_related("table", "serveur", "user")
	serializer_class = CommandeSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter]
	search_fields = []
	filterset_fields = {
		'user': ['exact'],
		'client__nom': ['icontains'],
		'serveur': ['exact'],
		'serveur__firstname': ['icontains'],
		'serveur__lastname': ['icontains'],
		'date': ['gte', 'lte', 'range'],
	}

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		data = request.data
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
			user = request.user, client = client,
			serveur = Serveur.objects.get(id=data.get("serveur"))
		)
		commande.save()
		details_commandes = []
		prix = 0
		for item in data.get("items"):
			recette:Recette = Recette.objects.get(id=item.get("recette"))
			produit:Produit = recette.produit
			quantite = float(item.get("quantite"))
			details = DetailCommande(
				recette=recette, commande=commande, quantite=quantite,
				somme = recette.prix*quantite
			)
			prix += details.somme
			details_commandes.append(details)
			if produit:
				produit.quantite -= quantite
				produit.save()
		DetailCommande.objects.bulk_create(details_commandes)
		payee = int(data.get("payee"))
		if payee:
			Paiement(commande=commande, somme=payee, validated=True).save()
		commande.payee = payee
		commande.a_payer = prix
		commande.save()
		serializer = self.serializer_class(commande, many=False)
		return Response(serializer.data, 201)

	@transaction.atomic
	def destroy(self, request, pk):
		commande:Commande = self.get_object()
		if(commande.payee > 0):
			return Response({'status': 'la commande payee ne peut pas être supprimé'}, 403)

		details:List[DetailCommande] = DetailCommande.objects.filter(commande=commande)
		for d in details:
			produit:Produit = d.recette.produit
			if(produit):
				produit.quantite += d.quantite
				produit.save()
		details.delete()
		commande.delete()
		return Response({'status': 'commande supprimée avec succes'}, 204)

	@transaction.atomic
	@action(methods=['POST'], detail=True, url_name=r'ajouter', url_path=r"ajouter",
		serializer_class=AddToCommandeSerializer)
	def ajouter(self, request, pk):
		commande = self.get_object()
		details_serializer = self.get_serializer(data=request.data)
		details_serializer.is_valid(raise_exception=True)
		data = details_serializer.validated_data
		recette = Recette.objects.get(id = data.get("recette_id"))
		quantite = data.get("quantite")
		details:DetailCommande = DetailCommande(
			commande = commande,
			recette = recette,
			quantite = quantite,
			somme = recette.prix*quantite
		)
		produit:Produit = recette.produit
		if produit:
			produit.quantite -= quantite
			produit.save()
		commande.a_payer += details.somme
		details.save()
		commande.save()
		serializer = CommandeSerializer(commande)
		return Response(serializer.data, 201)

	@transaction.atomic
	@action(methods=['GET'], detail=True, url_name=r'enlever/(?P<details_id>\d+)',
		url_path=r"enlever/(?P<details_id>\d+)",)
	def enlever(self, request, pk, details_id):
		commande = self.get_object()
		details = DetailCommande.objects.get(id=details_id)
		commande.a_payer -= details.somme
		produit:Produit = details.recette.produit
		if produit:
			produit.quantite -= details.quantite
			produit.save()
		details.delete()
		commande.save()
		serializer = CommandeSerializer(commande)
		return Response(serializer.data, 201)

	@action(methods=['GET'], detail=False, url_name=r'stats', url_path=r"stats")
	def statistiques(self, request):
		dates = request.GET.get("date__range")
		date_req = ""
		if dates:
			dates = dates.split(",")
			date_req = f"AND date BETWEEN '{dates[0]}' AND '{dates[1]}'"
		queryset = self.get_queryset()
		stats = queryset.raw("""
			SELECT
				resto_commande.id ,
				resto_serveur.id,
				resto_serveur.firstname as nom,
				resto_serveur.lastname as prenom,
				COUNT(resto_commande.id) AS fois,
				MIN(resto_commande.date) AS du,
				MAX(resto_commande.date) AS au,
				SUM(resto_commande.a_payer) AS prix,
				SUM(resto_commande.payee) AS payee
			FROM resto_commande, resto_serveur
			WHERE
				resto_commande.serveur_id = resto_serveur.id
				{}
			GROUP BY resto_commande.serveur_id
			ORDER BY resto_commande.id DESC
		""".format(date_req))
		serializer = ServiceSerializer(stats, many=True)
		return Response(serializer.data, 200)
