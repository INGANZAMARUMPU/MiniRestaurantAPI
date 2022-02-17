from .dependancies import *

class ClientViewset(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Client.objects.all()
	serializer_class = ClientSerializer

