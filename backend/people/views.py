from rest_framework import viewsets, permissions
from .models import Student, Teacher, Parent
from .serializers import StudentSerializer, TeacherSerializer, ParentSerializer

# La vue 'bulletin_view' a été supprimée car elle est maintenant gérée
# par 'BulletinDetailAPIView' dans l'application 'grading'.

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
