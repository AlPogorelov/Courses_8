from django.urls import path
from .apps import UsersConfig
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')


urlpatterns = [] + router.urls
