from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE Shipper (
#     shipper_id INT AUTO_INCREMENT PRIMARY KEY,
#     company_name VARCHAR(100),
#     phone VARCHAR(15)
# );

# Define el esquema de salida para las categorias
shipper_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'shipper_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del transportista'),
        'company_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la empresa'),
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono'),
    }
)
class ShipperGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all shippers",
        responses={200: openapi.Response(description="List of shippers", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=shipper_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_shippers')
            shippers = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        shipper_list = [
            {
                'shipper_id': row[0],
                'company_name': row[1],
                'phone': row[2],
            }
            for row in shippers
        ]
        return Response(shipper_list)
    
    @swagger_auto_schema(
        operation_description="Add a new shipper",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'company_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la empresa'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono'),
            },
            required=['company_name', 'phone']
        ),
        responses={201: "Shipper added successfully"}
    )
    
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_shipper', [
                    data.get('company_name'),
                    data.get('phone'),
                ])
            return Response({'message': 'Shipper added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ShipperPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a shipper by ID",
        manual_parameters=[
            openapi.Parameter(
                'shipper_id',
                openapi.IN_PATH,
                description="ID of the shipper to retrieve",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: openapi.Response(description="Shipper details", schema=shipper_schema)}
    )
    def put(self, request, shipper_id):
        with connection.cursor() as cursor:
            cursor.callproc('sp_update_shipper', [shipper_id])
            shipper = cursor.fetchone()
        
        if shipper:
            shipper_data = {
                'shipper_id': shipper[0],
                'company_name': shipper[1],
                'phone': shipper[2],
            }
            return Response(shipper_data)
        else:
            return Response({'error': 'Shipper not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_description="Delete a shipper by ID",
        manual_parameters=[
            openapi.Parameter(
                'shipper_id',
                openapi.IN_PATH,
                description="ID of the shipper to delete",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="Shipper deleted successfully"),
            404: openapi.Response(description="Shipper not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, shipper_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_shipper', [shipper_id])
            return Response({'message': 'Shipper deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)