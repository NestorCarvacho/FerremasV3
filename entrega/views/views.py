from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProductListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all products",
        responses={200: "List of products"}
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