from .dependancies import *

class RecetteViewset(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Recette.objects.select_related("produit")
	serializer_class = RecetteSerializer

	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		recette = self.get_object()
		recette.is_active = False
		recette.save()
		return Response({'status': 'success'}, 204)

