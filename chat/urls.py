from django.urls import path, re_path
from . import views
from django.urls import path, include
from .router import router

urlpatterns = [
    path('chat/', include(router.urls)),
]


