from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .models import Student, Teacher, Parent
from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    ParentSerializer,
    ParentChildSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Student.objects.all().select_related("user", "parents__user")
    serializer_class = StudentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class ParentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Parent.objects.all().select_related("user")
    serializer_class = ParentSerializer


class IsParentRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "PARENT"


class MyChildrenAPIView(generics.ListAPIView):
    """
    Retourne les enfants du parent connecté
    GET /api/people/children/
    """
    permission_classes = [permissions.IsAuthenticated, IsParentRole]
    serializer_class = ParentChildSerializer

    def get_queryset(self):
        parent_profile = getattr(self.request.user, "parent_profile", None)
        if not parent_profile:
            return Student.objects.none()

        return (
            Student.objects.filter(parents=parent_profile, is_active=True)
            .select_related("user", "parents__user")
            .order_by("nom", "prenom1")
        )


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