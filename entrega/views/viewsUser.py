from urllib import request
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# CREATE TABLE `User` (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     personal_info_id INT UNIQUE,
#     FOREIGN KEY (personal_info_id) REFERENCES PersonalInfo(personal_id) ON DELETE CASCADE
# );

# Define el esquema de salida para las user
user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
        'personal_info_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
    }
)

class UserGetPostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve all users",
        responses={200: openapi.Response(description="List of users", schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=user_schema
        ))}
    )
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.callproc('sp_get_users')
            user = cursor.fetchall()
               
        # Convierte los resultados en un formato JSON
        user_list = [
            {
                'id': row[0],
                'personal_info_id': row[1],
            }
            for row in user
        ]
        return Response(user_list)

    @swagger_auto_schema(
        operation_description="Add a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'personal_info_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
            },
            required=['personal_info_id']
        ),
        responses={201: "User added successfully"}
    )
    def post(self, request):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_add_user', [
                    data.get('personal_info_id'),
                ])
            return Response({'message': 'User added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserPutDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Update an existing user by ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the user to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'personal_info_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
            },
            required=['personal_info_id']
        ),
        responses={
            200: openapi.Response(description="User updated successfully"),
            404: openapi.Response(description="User not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def put(self, request, id):
        data = request.data
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_update_user', [
                    id,
                    data.get('personal_info_id'),
                ])
            return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_description="Delete an existing user",
        responses={
            200: openapi.Response(description="User deleted successfully"),
            404: openapi.Response(description="User not found"),
            400: openapi.Response(description="Bad request"),
        }
    )
    def delete(self, request, id):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_delete_user', [id])
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
