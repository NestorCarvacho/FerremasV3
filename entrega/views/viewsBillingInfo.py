from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE BillingInfo (
#     billing_id INT AUTO_INCREMENT PRIMARY KEY,
#     customer_id INT UNIQUE,
#     billing_address VARCHAR(255),
#     credit_card_number VARCHAR(16),
#     credit_card_pin VARCHAR(4),
#     credit_card_exp_date DATE,
#     bill_date DATE,
#     FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE
# );

# Define el esquema de salida para las BillingInfo
billingInfo_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'billing_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la información de facturación'),
        'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
        'billing_address': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de facturación'),
        'credit_card_number': openapi.Schema(type=openapi.TYPE_STRING, description='Número de tarjeta de crédito'),
        'credit_card_pin': openapi.Schema(type=openapi.TYPE_STRING, description='PIN de la tarjeta de crédito'),
        'credit_card_exp_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de expiración de la tarjeta de crédito'),
        'bill_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de la factura'),
    }
)

class BillingInfoGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all billing information",
        responses={200: openapi.Response(description="List of billing information", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=billingInfo_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_BillingInfos')
            billingInfo = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        billingInfo_list = [
            {
                'billing_id': row[0],
                'customer_id': row[1],
                'billing_address': row[2],
                'credit_card_number': row[3],
                'credit_card_pin': row[4],
                'credit_card_exp_date': row[5],
                'bill_date': row[6],
            }
            for row in billingInfo
        ]
        return Response(billingInfo_list)
    
    @swagger_auto_schema(
        operation_description="Add a new billing information",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
                'billing_address': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de facturación'),
                'credit_card_number': openapi.Schema(type=openapi.TYPE_STRING, description='Número de tarjeta de crédito'),
                'credit_card_pin': openapi.Schema(type=openapi.TYPE_STRING, description='PIN de la tarjeta de crédito'),
                'credit_card_exp_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de expiración de la tarjeta de crédito'),
                'bill_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de la factura'),
            },
            required=['customer_id', 'billing_address', 'credit_card_number', 'credit_card_pin', 'credit_card_exp_date', 'bill_date']
        ),
        responses={201: "Billing information added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_BillingInfo', [
                    data.get('customer_id'),
                    data.get('billing_address'),
                    data.get('credit_card_number'),
                    data.get('credit_card_pin'),
                    data.get('credit_card_exp_date'),
                    data.get('bill_date'),
                ])
            return Response({'message': 'Billing information added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BillingInfoPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing billing information by ID",
        manual_parameters=[
            openapi.Parameter(
                'billing_id',
                openapi.IN_PATH,
                description="ID of the billing information to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
                'billing_address': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de facturación'),
                'credit_card_number': openapi.Schema(type=openapi.TYPE_STRING, description='Número de tarjeta de crédito'),
                'credit_card_pin': openapi.Schema(type=openapi.TYPE_STRING, description='PIN de la tarjeta de crédito'),
                'credit_card_exp_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de expiración de la tarjeta de crédito'),
                'bill_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Fecha de la factura'),
            },
            required=['billing_id']
        ),
        responses={
            200: openapi.Response(description="Billing information updated successfully"),
            404: openapi.Response(description="Billing information not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, billing_id):
        try:
            data = request.data  # Obtén los datos enviados en la solicitud PUT
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_BillingInfo', [
                    billing_id,
                    data.get('customer_id'),
                    data.get('billing_address'),
                    data.get('credit_card_number'),
                    data.get('credit_card_pin'),
                    data.get('credit_card_exp_date'),
                    data.get('bill_date'),
                ])
            return Response({'message': 'Billing information updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete an existing billing information",
        responses={
            200: openapi.Response(description="Billing information deleted successfully"),
            404: openapi.Response(description="Billing information not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, billing_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_BillingInfo', [billing_id])
            return Response({'message': 'Billing information deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)