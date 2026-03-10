# backend/accounts/views.py

from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action  # <--- AJOUTEZ CETTE LIGNE
from rest_framework.response import Response # Assurez-vous que Response est aussi là
from .models import User
from .serializers import UserSerializer, ChildSerializer

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

class ParentChildrenListView(generics.ListAPIView):
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) != "PARENT":
            return User.objects.none()

        # Suppose relation parent -> children
        # Adapte selon ton modèle:
        # - user.children.all()
        # - User.objects.filter(parent=user)
        # - StudentProfile.objects.filter(parent=user)...
        return user.children.all().select_related("current_class")