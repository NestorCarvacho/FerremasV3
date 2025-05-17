from django.urls import path, include, re_path
from .views import viewsProducts, viewsCategories, viewsSuppliers, viewsCustomer, viewsPersonalInfo, viewsUser, viewsCart, viewsShipper, viewsOrder, viewsOrderDetails, viewsAdmin, viewsBillingInfo, viewsPayment, viewsOrderShipper, viewsOrderStatus
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
    path('orderStatus/', viewsOrderStatus.OrderStatusGetPostView.as_view(), name='orderStatus-get-post'),
    path('orderStatus/<int:order_id>/', viewsOrderStatus.OrderStatusPutDeleteView.as_view(), name='orderStatus-put-delete'),
    
    path('orderShipper/', viewsOrderShipper.OrderShipperGetPostView.as_view(), name='orderShipper-get-post'),
    path('orderShipper/<int:order_id>/', viewsOrderShipper.OrderShipperPutDeleteView.as_view(), name='orderShipper-put-delete'),
    
    path('payment/', viewsPayment.PaymentGetPostView.as_view(), name='payment-get-post'),
    path('payment/<int:payment_id>/', viewsPayment.PaymentPutDeleteView.as_view(), name='payment-put-delete'),
    
    path('billingInfo/', viewsBillingInfo.BillingInfoGetPostView.as_view(), name='billingInfo-get-post'),
    path('billingInfo/<int:billing_id>/', viewsBillingInfo.BillingInfoPutDeleteView.as_view(), name='billingInfo-put-delete'),
    
    path('administrators/', viewsAdmin.AdminGetPostView.as_view(), name='admin-get-post'),
    path('administrators/<int:admin_id>/', viewsAdmin.AdminPutDeleteView.as_view(), name='admin-put-delete'),
    
    path('orderDetails/', viewsOrderDetails.OrderDetailsGetPostView.as_view(), name='orderDetails-get-post'),
    path('orderDetails/<int:orderDetails_id>/', viewsOrderDetails.OrderDetailsPutDeleteView.as_view(), name='orderDetails-put-delete'),
        
    path('order/', viewsOrder.OrderGetPostView.as_view(), name='order-get-post'),
    path('order/<int:order_id>/', viewsOrder.OrderPutDeleteView.as_view(), name='order-put-delete'),
    
    path('shipper/', viewsShipper.ShipperGetPostView.as_view(), name='shipper-get-post'),
    path('shipper/<int:shipper_id>/', viewsShipper.ShipperPutDeleteView.as_view(), name='shipper-put-delete'),
    
    path('cart/', viewsCart.CartGetPostView.as_view(), name='cart-get-post'),
    path('cart/<int:id>/', viewsCart.CartPutDeleteView.as_view(), name='cart-put-delete'),
    
    path('user/', viewsUser.UserGetPostView.as_view(), name='user-get-post'),
    path('user/<int:id>/', viewsUser.UserPutDeleteView.as_view(), name='user-put-delete'),
    
    path('PersonalInfo/', viewsPersonalInfo.PersonalInfoGetPostView.as_view(), name='PersonalInfo-get-post'),
    path('PersonalInfo/<int:personal_id>/', viewsPersonalInfo.PersonalInfoPutDeleteView.as_view(), name='PersonalInfo-put-delete'),
    
    path('customers/', viewsCustomer.CustomerGetPostView.as_view(), name='customers-get-post'),
    path('customers/<int:suppliers_id>/', viewsCustomer.CustomerPutDeleteView.as_view(), name='customers-put-delete'),
    
    path('suppliers/', viewsSuppliers.SupplierGetPostView.as_view(), name='suppliers-get-post'),
    path('suppliers/<int:suppliers_id>/', viewsSuppliers.SupplierPutDeleteView.as_view(), name='supplier-put-delete'),
    
    path('products/', viewsProducts.ProductGetPostView.as_view(), name='product-get-post'),
    path('products/<int:product_id>/', viewsProducts.ProductPutDeleteView.as_view(), name='product-put'),
    
    path('categories/', viewsCategories.CategoryGetPostView.as_view(), name='category-get-post'),
    path('categories/<int:category_id>/', viewsCategories.CategoryPutDeleteView.as_view(), name='category-put-delete'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
