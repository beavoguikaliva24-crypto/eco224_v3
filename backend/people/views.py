from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Student, Teacher, Parent
from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    ParentSerializer,
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
