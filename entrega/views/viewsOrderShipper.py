from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE OrderShipper (
#     order_id INT,
#     shipper_id INT,
#     tracking_number VARCHAR(50),
#     PRIMARY KEY (order_id, shipper_id),
#     FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE,
#     FOREIGN KEY (shipper_id) REFERENCES Shipper(shipper_id) ON DELETE CASCADE
# );

# Define el esquema de salida para las ordenes de envío
order_shipper_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
        'shipper_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del transportista'),
        'tracking_number': openapi.Schema(type=openapi.TYPE_STRING, description='Número de seguimiento'),
    }
)
class OrderShipperGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all order shippers",
        responses={200: openapi.Response(description="List of order shippers", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=order_shipper_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_orderShippers')
            order_shippers = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        order_shipper_list = [
            {
                'order_id': row[0],
                'shipper_id': row[1],
                'tracking_number': row[2],
            }
            for row in order_shippers
        ]
        return Response(order_shipper_list)
    
    @swagger_auto_schema(
        operation_description="Add a new order shipper",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
                'shipper_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del transportista'),
                'tracking_number': openapi.Schema(type=openapi.TYPE_STRING, description='Número de seguimiento'),
            },
            required=['order_id', 'shipper_id', 'tracking_number']
        ),
        responses={201: "Order shipper added successfully"}
    )
    
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_orderShipper', [
                    data.get('order_id'),
                    data.get('shipper_id'),
                    data.get('tracking_number'),
                ])
            return Response({'message': 'Order shipper added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderShipperPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing order shipper by ID",
        manual_parameters=[
            openapi.Parameter(
                'order_id',
                openapi.IN_PATH,
                description="ID of the order shipper to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'shipper_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del transportista'),
                'tracking_number': openapi.Schema(type=openapi.TYPE_STRING, description='Número de seguimiento'),
            },
            required=['order_id']
        ),
        responses={
            200: openapi.Response(description="Order shipper updated successfully"),
            404: openapi.Response(description="Order shipper not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    
    def put(self, request, order_id):
        try:
            data = request.data  # Obtén los datos enviados en la solicitud PUT
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_orderShipper', [
                    order_id,
                    data.get('shipper_id'),
                    data.get('tracking_number'),
                ])
            return Response({'message': 'Order shipper updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        operation_description="Delete an existing order shipper",
        responses={
            200: openapi.Response(description="Order shipper deleted successfully"),
            404: openapi.Response(description="Order shipper not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, order_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_orderShipper', [order_id])
            return Response({'message': 'Order shipper deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)        