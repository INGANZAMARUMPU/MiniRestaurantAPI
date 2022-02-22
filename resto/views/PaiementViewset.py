from .dependancies import *

class PaiementViewset(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Paiement.objects.select_related("commande")
	serializer_class = PaiementSerializer

	@transaction.atomic
	def create(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		data = serializer.validated_data

		commande:Commande = data.get("commande")
		montant = data.get("somme")
		serializer.save()
		
		payee = Paiement.objects.filter(
			commande = commande
		).aggregate(somme=models.Sum("somme"))["somme"] or 0

		if int(payee) > commande.a_payer:
			commande.payee = commande.a_payer
		else:
			commande.payee = int(payee)
		commande.save()

		return Response(serializer.data, 201)