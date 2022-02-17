from .dependancies import *

class AchatViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Achat.objects.select_related("produit", "personnel")
	serializer_class = AchatSerializer

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		data = request.data
		try:
			achat = Achat(
				produit = Produit.objects.get(id=data["produit"]),
				quantite = float(data["quantite"]),
				prix = float(data["prix"]),
				user = request.user
			)
			achat.save()
			serializer = self.serializer_class(achat, many=False)
			return Response(serializer.data, 201)
		except:
			traceback.print_exception(*sys.exc_info()) 
			return Response({'status': 'Quelque chose d\'incorrect'}, 400)

