from .dependancies import *

class ClientViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Client.objects.all()
	serializer_class = ClientSerializer

