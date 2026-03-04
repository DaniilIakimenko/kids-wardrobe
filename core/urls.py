from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChildViewSet, CategoryViewSet, ClothingItemViewSet,
    RegisterView
)

router = DefaultRouter()
router.register(r'children', ChildViewSet, basename='child')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'clothes', ClothingItemViewSet, basename='clothing-item')

urlpatterns = [
    path('', include(router.urls)),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]