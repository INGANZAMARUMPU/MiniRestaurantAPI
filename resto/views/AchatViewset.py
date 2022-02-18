from .dependancies import *

class AchatViewset(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Achat.objects.select_related("produit", "user")
	serializer_class = AchatSerializer

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		data = request.data
		achat = Achat(
			produit = Produit.objects.get(id=data["produit"]),
			quantite = float(data["quantite"]),
			prix = float(data["prix"]),
			user = request.user
		)
		achat.save()
		produit:Produit = achat.produit
		produit.quantite += achat.quantite
		produit.save()
		serializer = self.serializer_class(achat, many=False)
		return Response(serializer.data, 201)

