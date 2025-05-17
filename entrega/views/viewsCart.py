from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE Cart (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     customer_id INT,
#     product_id INT,
#     num_of_products INT,
#     total_price DECIMAL(10,2),
#     FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE,
#     FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
# );

# Define el esquema de salida para las categorias
cart_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del carrito'),
        'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
        'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del producto'),
        'num_of_products': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número de productos'),
        'total_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Precio total'),
    }
)

class CartGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all carts",
        responses={200: openapi.Response(description="List of carts", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=cart_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_carts')
            carts = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        cart_list = [
            {
                'contact_name': row[0],
                'product_name': row[1],
                'unit_price': row[2],
                'num_of_products': row[3],
                'total_price': row[4],
            }
            for row in carts
        ]
        return Response(cart_list)
    
    @swagger_auto_schema(
        operation_description="Add a new cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del producto'),
                'num_of_products': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número de productos'),
                'total_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Precio total'),
            },
            required=['customer_id', 'product_id', 'num_of_products', 'total_price']
        ),
        responses={201: "Cart added successfully"}
    )
    
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_cart', [
                    data.get('customer_id'),
                    data.get('product_id'),
                    data.get('num_of_products'),
                    data.get('total_price'),
                ])
            return Response({'message': 'Cart added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CartPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing cart by ID",
        manual_parameters=[
            openapi.Parameter(
                'cart_id',
                openapi.IN_PATH,
                description="ID of the cart to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del producto'),
                'num_of_products': openapi.Schema(type=openapi.TYPE_INTEGER, description='Número de productos'),
                'total_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Precio total'),
            },
            required=['cart_id']
        ),
        responses={
            200: openapi.Response(description="Cart updated successfully"),
            404: openapi.Response(description="Cart not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    
    def put(self, request, cart_id):
        try:
            data = request.data  # Obtén los datos enviados en la solicitud PUT
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_cart', [
                    cart_id,
                    data.get('customer_id'),
                    data.get('product_id'),
                    data.get('num_of_products'),
                    data.get('total_price'),
                ])
            return Response({'message': 'Cart updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        operation_description="Delete an existing cart",
        responses={
            200: openapi.Response(description="Cart deleted successfully"),
            404: openapi.Response(description="Cart not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, cart_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_cart', [cart_id])
            return Response({'message': 'Cart deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        