from rest_framework.routers import DefaultRouter
from .views import LogActionViewSet, MesNotificationsViewSet

router = DefaultRouter()
router.register(r"logs", LogActionViewSet, basename="logs")
router.register(r"notifications", MesNotificationsViewSet, basename="notifications")

urlpatterns = router.urls