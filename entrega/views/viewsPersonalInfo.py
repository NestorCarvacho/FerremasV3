from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE PersonalInfo (
#     personal_id INT AUTO_INCREMENT PRIMARY KEY,
#     county VARCHAR(100),
#     address VARCHAR(255),
#     phone VARCHAR(15),
#     email VARCHAR(254),
#     city VARCHAR(100),
#     postal_code VARCHAR(20)
# );

# Define el esquema de salida para las PersonalInfo
personalInfo_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'personal_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='nombre de la informacion personal'),
        'county': openapi.Schema(type=openapi.TYPE_STRING, description='nombre de la informacion personal'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Direccion de la informacion personal'),
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefono de la informacion personal'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email de la informacion personal'),
        'city': openapi.Schema(type=openapi.TYPE_STRING, description='Ciudad de la informacion personal'),
        'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description='Codigo postal de la informacion personal'),
        
    }
)

class PersonalInfoGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all PersonalInfo",
        responses={200: openapi.Response(description="List of PersonalInfo", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=personalInfo_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_PersonalInfos')
            personalInfo = cursor.fetchall()
               
        # Convierte los resultados en un formato JSON
        personalInfo_list = [
                {
                    'personal id': row[0],
                    'county': row[1],
                    'address': row[2],
                    'phone': row[3],
                    'email': row[4],
                    'city': row[5],
                    'postal code': row[6],
                }
                for row in personalInfo
            ]
        return Response(personalInfo_list)

    @swagger_auto_schema(
        operation_description="Add a new personalInfo",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'county': openapi.Schema(type=openapi.TYPE_STRING, description='nombre de la informacion personal'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Direccion de la informacion personal'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefono de la informacion personal'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email de la informacion personal'),
                'city': openapi.Schema(type=openapi.TYPE_STRING, description='Ciudad de la informacion personal'),
                'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description='Codigo postal de la informacion personal'),
            },
            required=['county', 'address', 'phone', 'email', 'city', 'postal_code']
        ),
        responses={201: "Personal id added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_PersonalInfo', [
                    data.get('county'),
                    data.get('address'),
                    data.get('phone'),
                    data.get('email'),
                    data.get('city'),
                    data.get('postal_code'),
                ])
            return Response({'message': 'Personal id added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PersonalInfoPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing personalInfo by ID",
        manual_parameters=[
            openapi.Parameter(
                'personal_id',
                openapi.IN_PATH,
                description="ID of the personalInfo to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'county': openapi.Schema(type=openapi.TYPE_STRING, description='nombre de la informacion personal'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Direccion de la informacion personal'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefono de la informacion personal'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email de la informacion personal'),
                'city': openapi.Schema(type=openapi.TYPE_STRING, description='Ciudad de la informacion personal'),
                'postal_code': openapi.Schema(type=openapi.TYPE_STRING, description='Codigo postal de la informacion personal'),
            },
            required=['personal_id']
        ),
        responses={
            200: openapi.Response(description="personalInfo updated successfully"),
            404: openapi.Response(description="personalInfo not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, personal_id):
        data = request.data  # Obtén los datos enviados en la solicitud PUT
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_personalInfo', [
                    personal_id,
                    data.get('county'),
                    data.get('address'),
                    data.get('phone'),
                    data.get('email'),
                    data.get('city'),
                    data.get('postal_code'),
                ])
            return Response({'message': 'personalInfo updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Delete an existing personalInfo",
        responses={
            200: openapi.Response(description="personalInfo deleted successfully"),
            404: openapi.Response(description="personalInfo not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, personal_id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_PersonalInfo', [personal_id])
            return Response({'message': 'PersonalInfo deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   
    