from rest_framework import viewsets, permissions, generics, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer

class IsDevOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["DEV", "ADMIN"]

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        return Response(self.get_serializer(request.user).data)

    def get_permissions(self):
        if self.action in ["destroy", "create"]:
            return [IsDevOrAdmin()]
        return [permissions.IsAuthenticated()]
