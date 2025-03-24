from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="DRF React Demo Backend API",
      default_version='v1',
      description="Demo backend API for the test assessment.",
      terms_of_service="https://what.digital/privacy-policy-terms-of-use/",
      contact=openapi.Contact(email="bojan@wolfinne.com"),
      license=openapi.License(name="The GNU General Public License v3.0"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path('api/', include('api.urls')),
]