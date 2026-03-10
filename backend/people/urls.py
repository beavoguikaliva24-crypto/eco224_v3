from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, TeacherViewSet, ParentViewSet

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="students")
router.register(r"teachers", TeacherViewSet, basename="teachers")
router.register(r"parents", ParentViewSet, basename="parents")

urlpatterns = [
    path("api/", include(router.urls)),

    path("bulletin/<int:affectation_id>/periode/<int:periode_id>/", views.bulletin_view, name="bulletin_periode"),
    path("bulletin-annuel/<int:affectation_id>/", views.bulletin_view, name="bulletin_annuel"),
]