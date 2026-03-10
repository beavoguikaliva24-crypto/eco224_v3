from rest_framework import viewsets, permissions, generics
from .models import Student, Teacher, Parent
from .serializers import StudentSerializer, TeacherSerializer, ParentSerializer, ParentChildSerializer

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

class MyChildrenAPIView(generics.ListAPIView):
    serializer_class = ParentChildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != "PARENT":
            return Student.objects.none()

        parent_profile = getattr(user, "parent_profile", None)
        if not parent_profile:
            return Student.objects.none()

        return Student.objects.filter(parents=parent_profile, is_active=True).select_related("user")