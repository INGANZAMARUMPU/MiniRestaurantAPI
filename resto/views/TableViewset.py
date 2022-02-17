from .dependancies import *

class TableViewset(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, JWTAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Table.objects.all()
	serializer_class = TableSerializer

