from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet,
    TeacherViewSet,
    ParentViewSet,
    MyChildrenAPIView,
    ParentChildrenByParentIdAPIView,
)
from grading.views import BulletinDetailAPIView

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="students")
router.register(r"teachers", TeacherViewSet, basename="teachers")
router.register(r"parents", ParentViewSet, basename="parents")

urlpatterns = [
    # Enfants du parent connecté
    path("children/", MyChildrenAPIView.as_view(), name="my-children"),

    # Optionnel pour admin/dev
    path("parents/<int:parent_id>/children/", ParentChildrenByParentIdAPIView.as_view(), name="parent-children-by-id"),

    path("bulletin/<int:affectation_id>/periode/<int:periode_id>/", BulletinDetailAPIView.as_view(), name="bulletin_periode"),
    path("bulletin-annuel/<int:affectation_id>/", BulletinDetailAPIView.as_view(), name="bulletin_annuel"),
] + router.urls