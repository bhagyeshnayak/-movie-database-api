from django.contrib import admin
from django.urls import path, include
from movies.views_frontend import home

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ================= FRONTEND =================#
    path('', home, name='home'),
    # ================= ADMIN & API =================#

    path('admin/', admin.site.urls),
    path('api/v1/', include('movies.urls')),
# ================= AUTH =================#
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ================= API DOCS =================#
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]