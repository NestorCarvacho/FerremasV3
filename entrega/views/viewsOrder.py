from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE `Order` (
#     order_id INT AUTO_INCREMENT PRIMARY KEY,
#     customer_id INT,
#     order_date DATETIME,
#     required_date DATETIME,
#     shipped_date DATETIME NULL,
#     freight DECIMAL(10,2),
#     shipper_id INT,
#     FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE,
#     FOREIGN KEY (shipper_id) REFERENCES Shipper(shipper_id) ON DELETE CASCADE
# );

# Define el esquema de salida para las Orders
order_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
        'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
        'order_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha de la orden'),
        'required_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha requerida'),
        'shipped_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha de envío'),
        'freight': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Costo de envío'),
        'shipper_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del transportista'),
    }
)

class OrderGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all orders",
        responses={200: openapi.Response(description="List of orders", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=order_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_orders')
            orders = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        order_list = [
            {
                'order_id': row[0],
                'customer_id': row[1],
                'order_date': row[2],
                'required_date': row[3],
                'shipped_date': row[4],
                'freight': row[5],
                'shipper_id': row[6],
            }
            for row in orders
        ]
        return Response(order_list)

    @swagger_auto_schema(
        operation_description="Add a new Order",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
                'order_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha de la orden'),
                'required_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha requerida'),
                'shipped_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha de envío'),
                'freight': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Costo de envío'),
                'shipper_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del transportista'),
            },
            required=['customer_id', 'order_date', 'required_date', 'freight', 'shipper_id']
        ),
        responses={201: "Order added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_order', [
                    data.get('customer_id'),
                    data.get('order_date'),
                    data.get('required_date'),
                    data.get('shipped_date'),
                    data.get('freight'),
                    data.get('shipper_id'),
                ])
            return Response({'message': 'Order added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing order by ID",
        manual_parameters=[
            openapi.Parameter(
                'order_id',
                openapi.IN_PATH,
                description="ID of the order to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
                'order_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha de la orden'),
                'required_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha requerida'),
                'shipped_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha de envío'),
                'freight': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Costo de envío'),
                'shipper_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del transportista'),
            },
            required=['order_id']
        ),
        responses={
            200: openapi.Response(description="Order updated successfully"),
            404: openapi.Response(description="Order not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, order_id):
        data = request.data  # Obtén los datos enviados en la solicitud PUT
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_order', [
                    order_id,
                    data.get('customer_id'),
                    data.get('order_date'),
                    data.get('required_date'),
                    data.get('shipped_date'),
                    data.get('freight'),
                    data.get('shipper_id'),
                ])
            return Response({'message': 'Order updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Delete an existing order",
        responses={
            200: openapi.Response(description="Order deleted successfully"),
            404: openapi.Response(description="Order not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, order_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_order', [order_id])
            return Response({'message': 'Order deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)