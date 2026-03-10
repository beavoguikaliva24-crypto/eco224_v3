from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Student, Teacher, Parent
from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    ParentSerializer,
    ParentChildSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Student.objects.all().select_related("user", "parents__user")
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ParentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Parent.objects.all().select_related("user")
    serializer_class = ParentSerializer

class MyChildrenAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParentChildSerializer

    def get_queryset(self):
        u = self.request.user
        if not u.is_authenticated or u.role != "PARENT":
            return Student.objects.none()

        parent_profile = getattr(u, "parent_profile", None)
        if not parent_profile:
            return Student.objects.none()

        return Student.objects.filter(parents=parent_profile, is_active=True).select_related("user", "parents__user")

class ParentChildrenByParentIdAPIView(generics.ListAPIView):
    """
    Optionnel (admin/dev): enfants d’un parent donné
    GET /api/people/parents/<parent_id>/children/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParentChildSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role not in ["DEV", "ADMIN", "STAFF"]:
            return Student.objects.none()

        parent_id = self.kwargs.get("parent_id")
        return (
            Student.objects.filter(parents_id=parent_id, is_active=True)
            .select_related("user", "parents__user")
            .order_by("nom", "prenom1")
        )