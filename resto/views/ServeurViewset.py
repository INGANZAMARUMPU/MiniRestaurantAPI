from .dependancies import *

class ServeurViewset(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = Serveur.objects.all()
	serializer_class = ServeurSerializer

	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		serveur = self.get_object()
		serveur.is_active = False
		serveur.save()
		return Response({'status': 'success'}, 204)

