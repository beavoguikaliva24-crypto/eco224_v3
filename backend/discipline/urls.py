from rest_framework.routers import DefaultRouter
from .views import DisciplineViewSet

router = DefaultRouter()
router.register(r"discipline", DisciplineViewSet, basename="discipline")

urlpatterns = router.urls