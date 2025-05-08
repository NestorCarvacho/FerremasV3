from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderdetails
        fields = '__all__'
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class BillingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billinginfo
        fields = '__all__'
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ShipperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipper
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserSerializerWithToken(serializers.ModelSerializer): 
    token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'token')
