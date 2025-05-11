from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE Supplier (
#     supplier_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT UNIQUE,
#     contact_name VARCHAR(100),
#     contact_title VARCHAR(100),
#     address VARCHAR(255),
#     phone VARCHAR(15),
#     FOREIGN KEY (user_id) REFERENCES `User`(id) ON DELETE CASCADE
# );

# Define el esquema de salida para las categorias
suppliers_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'supplier_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del proveedor'),
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
        'contact_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del proveedor'),
        'contact_title': openapi.Schema(type=openapi.TYPE_STRING, description='Cargo del proveedor'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Direccion del proveedor'),
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefono del proveedor'),
    }
)

class SupplierGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all Supplier",
        responses={200: openapi.Response(description="List of Supplier", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=suppliers_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_suppliers')
            suppliers = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        suppliers_list = [
            {
                'supplier_id': row[0],
                'user_id': row[1],
                'contact_name': row[2],
                'contact_title': row[3],
                'address': row[4],
                'phone': row[5],
            }
            for row in suppliers
        ]
        return Response(suppliers_list)

    @swagger_auto_schema(
        operation_description="Add a new Supplier",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
                'contact_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del proveedor'),
                'contact_title': openapi.Schema(type=openapi.TYPE_STRING, description='Cargo del proveedor'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Direccion del proveedor'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefono del proveedor'),
            },
            required=['user_id','supplier_name', 'contact_name', 'contact_title', 'address', 'phone']
        ),
        responses={201: "Supplier added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_supplier', [
                    data.get('supplier_name'),
                    data.get('description'),
                    data.get('contact_name'),
                    data.get('contact_title'),
                    data.get('address'),
                    data.get('phone'),
                ])
            return Response({'message': 'Supplier added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SupplierPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing supplier by ID",
        manual_parameters=[
            openapi.Parameter(
                'supplier_id',
                openapi.IN_PATH,
                description="ID of the supplier to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
                'contact_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del proveedor'),
                'contact_title': openapi.Schema(type=openapi.TYPE_STRING, description='Cargo del proveedor'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Direccion del proveedor'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefono del proveedor'),
            },
            required=['supplier_id']
        ),
        responses={
            200: openapi.Response(description="supplier updated successfully"),
            404: openapi.Response(description="supplier not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, supplier_id):
        data = request.data  # Obtén los datos enviados en la solicitud PUT
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_supplier', [
                    supplier_id,
                    data.get('supplier_name'),
                    data.get('description'),
                    data.get('contact_name'),
                    data.get('contact_title'),
                    data.get('address'),
                    data.get('phone'),
                ])
            return Response({'message': 'supplier updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Delete an existing supplier",
        responses={
            200: openapi.Response(description="supplier deleted successfully"),
            404: openapi.Response(description="supplier not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, supplier_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_supplier', [supplier_id])
            return Response({'message': 'supplier deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   
    