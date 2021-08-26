from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from django.contrib import admin
from django.urls import path
from aiLooker_app import views_aiLooker
from aiLooker_app import views
from aiLooker_api import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/aiLookers/', views_aiLooker.aiLookers),
    path('api/aiLookers/<int:advtno>/', views_aiLooker.aiLookers),
    path('', views.index),
    path('login', views.login_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
