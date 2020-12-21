from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import *

router = routers.DefaultRouter()
router.register("produit", ProduitViewset)
router.register("serveur", ServeurViewset)
router.register("table", TableViewset)
router.register("detailstock", DetailStockViewset)
router.register("offre", OffreViewset)
router.register("paiement", PaiementViewset)
router.register("stock", StockViewset)
router.register("fournisseur", FournisseurViewset)
router.register("recette", RecetteViewset)
router.register("commande", CommandeViewset)
router.register("chart_menus", ChartRecetteViewset, basename='chart_menus')
router.register("chart_perso", ChartPersonnelViewset, basename='chart_perso')

urlpatterns = [
	path("api/", include(router.urls)),
	path("", include(router.urls)),
	path('api-auth/', include('rest_framework.urls')),
	path('login/', TokenObtainPairView.as_view()),
	path('refresh/', TokenRefreshView.as_view())
]