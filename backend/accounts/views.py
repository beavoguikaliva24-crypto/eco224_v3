# backend/accounts/views.py

from rest_framework import viewsets, permissions, generics, serializers
from rest_framework.decorators import action  # <--- AJOUTEZ CETTE LIGNE
from rest_framework.response import Response # Assurez-vous que Response est aussi là
from .models import User, Student
from .serializers import UserSerializer, ChildSerializer
from people.models import Student 

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Permet au frontend de récupérer les infos de l'utilisateur connecté
        via GET /api/accounts/users/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['destroy', 'create']:
            return [IsDevOrAdmin()] # Seuls les chefs peuvent supprimer/créer
        return [permissions.IsAuthenticated()]
    
class IsDevOrAdmin(permissions.BasePermission):
    """Accès réservé aux Développeurs et Admins"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['DEV', 'ADMIN']

class IsDevOnly(permissions.BasePermission):
    """Accès strictement réservé au Développeur"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'DEV'

class ParentChildSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="prenom1", read_only=True)
    last_name = serializers.CharField(source="nom", read_only=True)
    contact = serializers.CharField(source="user.contact", read_only=True, default="")
    photo = serializers.ImageField(source="photo", read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "full_name",
            "matricule",
            "photo",
            "date_naissance",
            "lieu_naissance",
        ]


class ParentChildrenListView(generics.ListAPIView):
    serializer_class = ParentChildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        if u.role != "PARENT":
            return Student.objects.none()

        parent_profile = getattr(u, "parent_profile", None)
        if not parent_profile:
            return Student.objects.none()

        return Student.objects.filter(parents=parent_profile, is_active=True).select_related("user")
    
