from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE OrderStatus (
#     order_id INT,
#     status VARCHAR(50),
#     status_date DATETIME,
#     PRIMARY KEY (order_id, status),
#     FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE
# );

# Define el esquema de salida para los estados de la orden
order_status_schema = openapi.Schema(
    properties={
        'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Estado de la orden'),
        'status_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha del estado'),
    },
    type=openapi.TYPE_OBJECT
)
class OrderStatusGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all order statuses",
        responses={200: openapi.Response(description="List of order statuses", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=order_status_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_ordersStatus')
            order_statuses = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        order_status_list = [
            {
                'order_id': row[0],
                'status': row[1],
                'status_date': row[2],
            }
            for row in order_statuses
        ]
        return Response(order_status_list)
    
    @swagger_auto_schema(
        operation_description="Add a new order status",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Estado de la orden'),
                'status_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha del estado'),
            },
            required=['order_id', 'status', 'status_date']
        ),
        responses={201: "Order status added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_orderStatus', [
                    data.get('order_id'),
                    data.get('status'),
                    data.get('status_date'),
                ])
            return Response({'message': 'Order status added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderStatusPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing order status by ID",
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
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Estado de la orden'),
                'status_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha del estado'),
            },
            required=['order_id']
        ),
        responses={200: "Order status updated successfully"}
    )
    def put(self, request, order_id):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_orderStatus', [
                    order_id,
                    data.get('status'),
                    data.get('status_date'),
                ])
            return Response({'message': 'Order status updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        operation_description="Delete an existing order status by ID",
        manual_parameters=[
            openapi.Parameter(
                'order_id',
                openapi.IN_PATH,
                description="ID of the order to delete",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={204: "Order status deleted successfully"}
    )
    def delete(self, request, order_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_orderStatus', [order_id])
            return Response({'message': 'Order status deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        