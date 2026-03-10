from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ParentChildrenListView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("children/", ParentChildrenListView.as_view(), name="parent-children"),
]