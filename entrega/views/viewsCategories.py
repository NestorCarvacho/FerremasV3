from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE Category (
#     category_id INT AUTO_INCREMENT PRIMARY KEY,
#     category_name VARCHAR(100),
#     description TEXT,
#     picture VARCHAR(255)  -- Para almacenar rutas de imagen si no usas blobs
# );

# Define el esquema de salida para las categorias
category_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la categoria'),
        'category_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la categoria'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción de la categoria'),
        'picture': openapi.Schema(type=openapi.TYPE_STRING, description='ruta de la imagen de la categoria'),
    }
)

class CategoryGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all categories",
        responses={200: openapi.Response(description="List of categories", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=category_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_categories')
            categorys = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        category_list = [
            {
                'category_id': row[0],
                'category_name': row[1],
                'description': row[2],
                'picture': row[3],
            }
            for row in categorys
        ]
        return Response(category_list)

    @swagger_auto_schema(
        operation_description="Add a new category",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'category_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la categoria'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción de la categoria'),
                'picture': openapi.Schema(type=openapi.TYPE_STRING, description='ruta de la imagen de la categoria'),
            },
            required=['category_name', 'description']
        ),
        responses={201: "Category added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_category', [
                    data.get('category_name'),
                    data.get('description'),
                ])
            return Response({'message': 'Category added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CategoryPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing category by ID",
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                openapi.IN_PATH,
                description="ID of the category to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'category_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la categoria'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción de la categoria'),
            },
            required=['category_id']
        ),
        responses={
            200: openapi.Response(description="category updated successfully"),
            404: openapi.Response(description="category not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, category_id):
        data = request.data  # Obtén los datos enviados en la solicitud PUT
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_category', [
                    category_id,
                    data.get('category_name'),
                    data.get('description'),
                ])
            return Response({'message': 'category updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Delete an existing category",
        responses={
            200: openapi.Response(description="category deleted successfully"),
            404: openapi.Response(description="category not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, category_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_category', [category_id])
            return Response({'message': 'category deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   
    