from rest_framework.routers import DefaultRouter
from .views import AnneeScolaireViewSet, PeriodeViewSet, ClasseViewSet, MatiereViewSet, MatiereClasseViewSet

router = DefaultRouter()
router.register(r"annees", AnneeScolaireViewSet, basename="annees")
router.register(r"periodes", PeriodeViewSet, basename="periodes")
router.register(r"classes", ClasseViewSet, basename="classes")
router.register(r"matieres", MatiereViewSet, basename="matieres")
router.register(r"matieres-classe", MatiereClasseViewSet, basename="matieres-classe")

urlpatterns = router.urls