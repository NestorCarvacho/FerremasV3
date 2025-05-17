from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE Payment (
#     payment_id INT AUTO_INCREMENT PRIMARY KEY,
#     order_id INT,
#     payment_date DATETIME,
#     amount DECIMAL(10,2),
#     payment_method VARCHAR(50),
#     FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE
# );

# Define el esquema de salida para las Payment
payment_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'payment_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del pago'),
        'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
        'payment_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha del pago'),
        'amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Monto del pago'),
        'payment_method': openapi.Schema(type=openapi.TYPE_STRING, description='Método de pago'),
    }
)

class PaymentGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all payments",
        responses={200: openapi.Response(description="List of payments", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=payment_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_payments')
            payments = cursor.fetchall()
        
        # Convierte los resultados en un formato JSON
        payment_list = [
            {
                'payment_id': row[0],
                'order_id': row[1],
                'payment_date': row[2],
                'amount': row[3],
                'payment_method': row[4],
            }
            for row in payments
        ]
        return Response(payment_list)
    
    @swagger_auto_schema(
        operation_description="Add a new payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
                'payment_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha del pago'),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Monto del pago'),
                'payment_method': openapi.Schema(type=openapi.TYPE_STRING, description='Método de pago'),
            },
            required=['order_id', 'payment_date', 'amount', 'payment_method']
        ),
        responses={201: "Payment added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_payment', [
                    data.get('order_id'),
                    data.get('payment_date'),
                    data.get('amount'),
                    data.get('payment_method'),
                ])
            return Response({'message': 'Payment added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing payment by ID",
        manual_parameters=[
            openapi.Parameter(
                'payment_id',
                openapi.IN_PATH,
                description="ID of the payment to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la orden'),
                'payment_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha del pago'),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Monto del pago'),
                'payment_method': openapi.Schema(type=openapi.TYPE_STRING, description='Método de pago'),
            },
            required=['payment_id']
        ),
        responses={
            200: openapi.Response(description="Payment updated successfully"),
            404: openapi.Response(description="Payment not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, payment_id):
        try:
            data = request.data  # Obtén los datos enviados en la solicitud PUT
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_payment', [
                    payment_id,
                    data.get('order_id'),
                    data.get('payment_date'),
                    data.get('amount'),
                    data.get('payment_method'),
                ])
            return Response({'message': 'Payment updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_description="Delete an existing payment",
        responses={
            200: openapi.Response(description="Payment deleted successfully"),
            404: openapi.Response(description="Payment not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    
    def delete(self, request, payment_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_payment', [payment_id])
            return Response({'message': 'Payment deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)