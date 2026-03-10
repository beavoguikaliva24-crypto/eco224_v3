from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, TeacherViewSet, ParentViewSet
# Importer la vue des bulletins depuis l'application 'grading'
from grading.views import BulletinDetailAPIView

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="students")
router.register(r"teachers", TeacherViewSet, basename="teachers")
router.register(r"parents", ParentViewSet, basename="parents")

urlpatterns = [
    path("api/", include(router.urls)),

    # Ces URLs pointent maintenant vers la bonne vue qui calcule les bulletins
    path(
        "bulletin/<int:affectation_id>/periode/<int:periode_id>/", 
        BulletinDetailAPIView.as_view(), 
        name="bulletin_periode"
    ),
    path(
        "bulletin-annuel/<int:affectation_id>/", 
        BulletinDetailAPIView.as_view(), 
        name="bulletin_annuel"
    ),
]