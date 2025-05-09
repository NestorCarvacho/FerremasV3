from django.urls import path, include, re_path
from .views import viewsProducts, viewsCategories
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
        description="API documentation for the Ecommerce project",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('products/', viewsProducts.ProductGetPostView.as_view(), name='product-get'),
    path('products/<int:product_id>/', viewsProducts.ProductPutDeleteView.as_view(), name='product-put'),
    
    path('categories/', viewsCategories.CategoryGetPostView.as_view(), name='category-get'),
    path('categories/<int:category_id>/', viewsCategories.CategoryPutDeleteView.as_view(), name='category-put'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
