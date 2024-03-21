from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'list', UserViewSet, basename='list')
router.register(r'info', UserInfoViewSet, basename='info')
router.register(r'authentication_rest', authentication_rest, basename='authentication_rest')
router.register(r'register_user', RegisterViewSet, basename='register')



