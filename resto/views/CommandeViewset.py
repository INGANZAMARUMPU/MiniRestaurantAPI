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

