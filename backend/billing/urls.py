from rest_framework.routers import DefaultRouter
from .views import FraisScolariteViewSet, PaiementViewSet, VersementViewSet

router = DefaultRouter()
router.register(r"frais-scolarite", FraisScolariteViewSet, basename="frais-scolarite")
router.register(r"paiements", PaiementViewSet, basename="paiements")
router.register(r"versements", VersementViewSet, basename="versements")

urlpatterns = router.urls