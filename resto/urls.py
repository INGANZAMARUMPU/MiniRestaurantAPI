from django.urls import path, include
from rest_framework import routers
from .views import *
from .api import *

router = routers.DefaultRouter()
router.register("produit", ProduitViewset)
router.register("stock", StockViewset)
router.register("fournisseur", FournisseurViewset)
router.register("recette", RecetteViewset)
router.register("commande", CommandeViewset)
router.register("chart_menus", ChartRecetteViewset, basename='chart_menus')
router.register("chart_perso", ChartPersonnelViewset, basename='chart_perso')

urlpatterns = [
    path("api/", include(router.urls)),
	path("", include(router.urls)),
]
