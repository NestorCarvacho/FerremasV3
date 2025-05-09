from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Define el esquema de salida para los productos
product_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del producto'),
        'product_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del producto'),
        'supplier_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del proveedor'),
        'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la categoría'),
        'quantity_per_unit': openapi.Schema(type=openapi.TYPE_STRING, description='Cantidad por unidad'),
        'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Precio por unidad'),
        'units_in_order': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unidades en orden'),
        'units_in_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unidades en stock'),
        'reorder_level': openapi.Schema(type=openapi.TYPE_INTEGER, description='Nivel de reorden'),
        'discount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Descuento'),
    }
)

class ProductGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all products",
        responses={200: openapi.Response(description="List of products", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=product_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_products')
            products = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        product_list = [
            {
                'product_id': row[0],
                'product_name': row[1],
                'supplier_id': row[2],
                'category_id': row[3],
                'quantity_per_unit': row[4],
                'unit_price': row[5],
                'units_in_order': row[6],
                'units_in_stock': row[7],
                'reorder_level': row[8],
                'discount': row[9],
            }
            for row in products
        ]
        return Response(product_list)

    @swagger_auto_schema(
        operation_description="Add a new product",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del producto'),
                'supplier_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del proveedor'),
                'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la categoría'),
                'quantity_per_unit': openapi.Schema(type=openapi.TYPE_STRING, description='Cantidad por unidad'),
                'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Precio por unidad'),
                'units_in_order': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unidades en orden'),
                'units_in_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unidades en stock'),
                'reorder_level': openapi.Schema(type=openapi.TYPE_INTEGER, description='Nivel de reorden'),
                'discount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Descuento'),
            },
            required=['product_name', 'supplier_id', 'category_id']
        ),
        responses={201: "Product added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_product', [
                    data.get('product_name'),
                    data.get('supplier_id'),
                    data.get('category_id'),
                    data.get('quantity_per_unit'),
                    data.get('unit_price'),
                    data.get('units_in_order'),
                    data.get('units_in_stock'),
                    data.get('reorder_level'),
                    data.get('discount'),
                ])
            return Response({'message': 'Product added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing product by ID",
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_PATH,
                description="ID of the product to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del producto'),
                'supplier_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del proveedor'),
                'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la categoría'),
                'quantity_per_unit': openapi.Schema(type=openapi.TYPE_STRING, description='Cantidad por unidad'),
                'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Precio por unidad'),
                'units_in_order': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unidades en orden'),
                'units_in_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unidades en stock'),
                'reorder_level': openapi.Schema(type=openapi.TYPE_INTEGER, description='Nivel de reorden'),
                'discount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Descuento'),
            },
            required=['product_name', 'supplier_id', 'category_id']
        ),
        responses={
            200: openapi.Response(description="Product updated successfully"),
            404: openapi.Response(description="Product not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, product_id):
        data = request.data  # Obtén los datos enviados en la solicitud PUT
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_product', [
                    product_id,
                    data.get('product_name'),
                    data.get('supplier_id'),
                    data.get('category_id'),
                    data.get('quantity_per_unit'),
                    data.get('unit_price'),
                    data.get('units_in_order'),
                    data.get('units_in_stock'),
                    data.get('reorder_level'),
                    data.get('discount'),
                ])
            return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Delete an existing product",
        responses={
            200: openapi.Response(description="Product deleted successfully"),
            404: openapi.Response(description="Product not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, product_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_product', [product_id])
            return Response({'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   
    