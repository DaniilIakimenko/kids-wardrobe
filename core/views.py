from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

from .models import Child, Category, ClothingItem
from .serializers import (
    UserSerializer, ChildSerializer, CategorySerializer, ClothingItemSerializer,
    RegisterSerializer
)


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Категории (общие для всех)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    # Можно разрешить только чтение категорий обычным юзерам, если нужно
    # http_method_names = ['get', 'head', 'options'] 


class ChildViewSet(viewsets.ModelViewSet):
    """Дети пользователя"""
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Child.objects.filter(parent=self.request.user)

    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)


class ClothingItemViewSet(viewsets.ModelViewSet):
    """Вещи гардероба"""
    serializer_class = ClothingItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ClothingItem.objects.filter(child__parent=user)
        
        child_id = self.request.query_params.get('child_id')
        if child_id:
            queryset = queryset.filter(child_id=child_id)
            
        return queryset


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)