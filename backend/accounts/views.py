from rest_framework import viewsets, permissions, generics, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from people.models import Student


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


class ParentChildSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="prenom1", read_only=True)
    last_name = serializers.CharField(source="nom", read_only=True)
    contact = serializers.CharField(source="user.contact", read_only=True, default="")
    photo = serializers.ImageField(source="photo", read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "matricule",
            "contact",
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