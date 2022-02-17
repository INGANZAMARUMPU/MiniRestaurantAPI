from .dependancies import *

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
			personnel = request.user.personnel,
			client = client,
			serveur = Serveur.objects.get(id=data.get("serveur"))
		)
		commande.save()
		details_commandes = []
		for item in data.get("items"):
			recette:Recette = Recette.objects.get(id=item.get("recette"))
			produit:Produit = recette.produit
			quantite = float(item.get("quantite"))
			details = DetailCommande(
				recette = recette, commande = commande, quantite = quantite
			)
			details_commandes.append(details)
			if produit:
				produit.quantite -= quantite
				produit.save()
		Commande.objects.bulk_create(details_commandes)
		payee = int(data.get("payee"))
		if payee:
			Paiement(commande=commande, somme=payee, validated=True).save()
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

