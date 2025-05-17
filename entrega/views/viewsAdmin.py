from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE Admin (
#     admin_id INT AUTO_INCREMENT PRIMARY KEY,
#     admin_name VARCHAR(100),
#     admin_password VARCHAR(100)
# );

# Define el esquema de salida para las categorias
admin_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'admin_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del administrador'),
        'admin_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del administrador'),
        'admin_password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del administrador'),
    }
)

class AdminGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all admins",
        responses={200: openapi.Response(description="List of admins", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=admin_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_admins')
            admins = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        admin_list = [
            {
                'admin_id': row[0],
                'admin_name': row[1],
                'admin_password': row[2],
            }
            for row in admins
        ]
        return Response(admin_list)
    
    @swagger_auto_schema(
        operation_description="Add a new admin",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'admin_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del administrador'),
                'admin_password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del administrador'),
            },
            required=['admin_name', 'admin_password']
        ),
        responses={201: "Admin added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_admin', [
                    data.get('admin_name'),
                    data.get('admin_password'),
                ])
            return Response({'message': 'Admin added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class AdminPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing admin by ID",
        manual_parameters=[
            openapi.Parameter(
                'admin_id',
                openapi.IN_PATH,
                description="ID of the admin to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'admin_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del administrador'),
                'admin_password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del administrador'),
            },
            required=['admin_id']
        ),
        responses={
            200: openapi.Response(description="Admin updated successfully"),
            404: openapi.Response(description="Admin not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, admin_id):
        try:
            data = request.data  # Obtén los datos enviados en la solicitud PUT
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_admin', [
                    admin_id,
                    data.get('admin_name'),
                    data.get('admin_password'),
                ])
            return Response({'message': 'Admin updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_description="Delete an existing admin",
        responses={
            200: openapi.Response(description="Admin deleted successfully"),
            404: openapi.Response(description="Admin not found"),
            400: openapi.Response(description="Bad request"),
        }   
    )
    
    def delete(self, request, admin_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_admin', [admin_id])
            return Response({'message': 'Admin deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)