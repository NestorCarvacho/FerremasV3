from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE OrderDetails (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     order_id INT,
#     product_id INT,
#     unit_price DECIMAL(10,2),
#     quantity INT,
#     discount DECIMAL(5,2),
#     FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE,
#     FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
# );

# Define el esquema de salida para las categorias
orderDetails_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del detalle de la orden'),
        'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
        'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del producto'),
        'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Precio unitario'),
        'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cantidad'),
        'discount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Descuento'),
    }
)
class OrderDetailsGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all order details",
        responses={200: openapi.Response(description="List of order details", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=orderDetails_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_OrderDetails')
            order_details = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        order_details_list = [
            {
                'id': row[0],
                'order_id': row[1],
                'product_id': row[2],
                'unit_price': row[3],
                'quantity': row[4],
                'discount': row[5],
            }
            for row in order_details
        ]
        return Response(order_details_list)
    
    @swagger_auto_schema(
        operation_description="Add a new order detail",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del producto'),
                'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Precio unitario'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cantidad'),
                'discount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Descuento'),
            },
            required=['order_id', 'product_id', 'unit_price', 'quantity', 'discount']
        ),
        responses={201: "Order detail added successfully"}
    )
    
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_OrderDetail', [
                    data.get('order_id'),
                    data.get('product_id'),
                    data.get('unit_price'),
                    data.get('quantity'),
                    data.get('discount'),
                ])
            return Response({'message': 'Order detail added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

class OrderDetailsPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing order detail by ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the order detail to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del producto'),
                'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Precio unitario'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Cantidad'),
                'discount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Descuento'),
            },
            required=['id']
        ),
        responses={
            200: openapi.Response(description="Order detail updated successfully"),
            404: openapi.Response(description="Order detail not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    
    def put(self, request, id):
        try:
            data = request.data  # Obtén los datos enviados en la solicitud PUT
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_OrderDetail', [
                    id,
                    data.get('order_id'),
                    data.get('product_id'),
                    data.get('unit_price'),
                    data.get('quantity'),
                    data.get('discount'),
                ])
            return Response({'message': 'Order detail updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        operation_description="Delete an existing order detail",
        responses={
            200: openapi.Response(description="Order detail deleted successfully"),
            404: openapi.Response(description="Order detail not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_OrderDetail', [id])
            return Response({'message': 'Order detail deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  