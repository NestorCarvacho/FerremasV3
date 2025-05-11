from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE Customer (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT UNIQUE,
#     last_name VARCHAR(100),
#     contact_name VARCHAR(100),
#     FOREIGN KEY (user_id) REFERENCES `User`(id) ON DELETE CASCADE
# );

# Define el esquema de salida para las categorias
customer_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del cliente'),
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user id del cliente'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del cliente'),
        'contact_name': openapi.Schema(type=openapi.TYPE_STRING, description='nobre del cliente'),
    }
)

class CustomerGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all customers",
        responses={200: openapi.Response(description="List of customers", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=customer_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_customers')
            customers = cursor.fetchall()
        
    # SELECT 	cu.last_name,
	# 	cu.contact_name,
    #     pein.address,
    #     pein.phone,
    #     pein.email,
    #     pein.county,
    #     pein.city,
    #     pein.postal_code
    # FROM Customer cu
    # JOIN `user` us on cu.user_id = us.id
    # JOIN personalInfo pein on us.personal_info_id = pein.personal_id;
        
        # Convierte los resultados en un formato JSON
        customer_list = [
            {
                'last_name': row[0],
                'contact_name': row[1],
                'address': row[2],
                'phone': row[3],
                'email': row[4],
                'county': row[5],
                'city': row[6],
                'postal_code': row[7],
            }
            for row in customers
        ]
        return Response(customer_list)

    @swagger_auto_schema(
        operation_description="Add a new Customer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user id del cliente'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del cliente'),
                'contact_name': openapi.Schema(type=openapi.TYPE_STRING, description='nobre del cliente'),
            },
            required=['user_id', 'last_name', 'contact_name']
        ),
        responses={201: "Customer added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_customer', [
                    data.get('user_id'),
                    data.get('last_name'),
                    data.get('contact_name'),
                ])
            return Response({'message': 'customer added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CustomerPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing customer by ID",
        manual_parameters=[
            openapi.Parameter(
                'customer_id',
                openapi.IN_PATH,
                description="ID of the customer to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='user id del cliente'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del cliente'),
                'contact_name': openapi.Schema(type=openapi.TYPE_STRING, description='nobre del cliente'),
            },
            required=['customer_id']
        ),
        responses={
            200: openapi.Response(description="customer updated successfully"),
            404: openapi.Response(description="customer not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, customer_id):
        data = request.data  # Obtén los datos enviados en la solicitud PUT
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_customer', [
                    customer_id,
                    data.get('customer_name'),
                    data.get('description'),
                ])
            return Response({'message': 'customer updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Delete an existing customer",
        responses={
            200: openapi.Response(description="customer deleted successfully"),
            404: openapi.Response(description="customer not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, customer_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_customer', [customer_id])
            return Response({'message': 'customer deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   
    