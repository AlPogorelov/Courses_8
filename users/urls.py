from django.urls import path
from .apps import UsersConfig
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, MyTokenObtainPairView, UserRegistrationView, MyTokenRefreshView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),

] + router.urls
