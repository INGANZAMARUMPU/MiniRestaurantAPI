from .dependancies import *

class SortieViewset(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Sortie.objects.select_related("produit", "personnel")
	serializer_class = SortieSerializer

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		data = request.data
		sortie:Sortie = Sortie(
			produit = Produit.objects.get(id=data["produit"]),
			quantite = float(data["quantite"]),
			motif = data["motif"],
			user = request.user
		)
		sortie.save()
		produit:Produit = sortie.produit
		produit.quantite -= sortie.quantite
		produit.save()
		serializer = self.serializer_class(sortie, many=False)
		return Response(serializer.data, 201)

