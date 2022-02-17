from .dependancies import *

class PaiementViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Paiement.objects.select_related("commande")
	serializer_class = PaiementSerializer

