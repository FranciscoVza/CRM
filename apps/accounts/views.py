from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Account, AccountUser, Profile
from .serializers import (
    UserSerializer, UserCreateSerializer, UserDetailSerializer,
    AccountSerializer, AccountUserSerializer, ProfileSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        if user != request.user and not request.user.is_staff:
            return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')

        if not user.check_password(old_password):
            return Response({'error': 'Contraseña anterior incorrecta'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != new_password_confirm:
            return Response({'error': 'Las contraseñas no coinciden'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Contraseña actualizada exitosamente'})

    @action(detail=False, methods=['get'])
    def profile(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(
            users__user=user
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        account = self.get_object()
        members = account.users.all()
        serializer = AccountUserSerializer(members, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        account = self.get_object()
        user_email = request.data.get('email')
        role = request.data.get('role', 'agent')

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        account_user, created = AccountUser.objects.get_or_create(
            account=account,
            user=user,
            defaults={'role': role}
        )

        if not created:
            account_user.role = role
            account_user.save()

        serializer = AccountUserSerializer(account_user)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove_member(self, request, pk=None):
        account = self.get_object()
        user_id = request.data.get('user_id')

        try:
            account_user = AccountUser.objects.get(account=account, user_id=user_id)
            account_user.delete()
            return Response({'message': 'Miembro removido exitosamente'})
        except AccountUser.DoesNotExist:
            return Response({'error': 'Miembro no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def update_member_role(self, request, pk=None):
        account = self.get_object()
        user_id = request.data.get('user_id')
        role = request.data.get('role')

        try:
            account_user = AccountUser.objects.get(account=account, user_id=user_id)
            account_user.role = role
            account_user.save()
            serializer = AccountUserSerializer(account_user)
            return Response(serializer.data)
        except AccountUser.DoesNotExist:
            return Response({'error': 'Miembro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
