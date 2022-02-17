from .dependancies import *

class DetailCommandeViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = DetailCommande.objects.select_related("commande", "recette")
	serializer_class = DetailCommandeSerializer

