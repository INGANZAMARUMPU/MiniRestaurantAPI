from .dependancies import *

class PaiementViewset(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Paiement.objects.select_related("commande")
	serializer_class = PaiementSerializer

