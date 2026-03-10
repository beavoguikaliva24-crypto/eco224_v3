from rest_framework import viewsets, permissions
from .models import Student, Teacher, Parent
from .serializers import StudentSerializer, TeacherSerializer, ParentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def bulletin_view(request, affectation_id: int, periode_id: int | None = None):
    return Response(
        {
            "detail": "bulletin_view stub - à implémenter",
            "affectation_id": affectation_id,
            "periode_id": periode_id,
        }
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def bulletin_view(request, affectation_id: int, periode_id: int | None = None):
    """
    Stub pour débloquer les URLs.
    Plus tard: appeler grading.services pour calculer le bulletin.
    """
    return Response(
        {
            "detail": "bulletin_view stub - à implémenter",
            "affectation_id": affectation_id,
            "periode_id": periode_id,
        }
    )

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ParentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer