import requests
import threading
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .tasks import enrich_data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserSignupView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            raise ValidationError('Email is required')
        response = requests.get(f'https://emailvalidation.abstractapi.com/v1/?api_key=31af24109bb24db1a71b8d3e95d9ad0a&email={email}')
        if response.status_code == 200:
            data = response.json()
            if data.get('is_smtp_valid').get('value') == False:
                raise ValidationError('Enter a valid email address.')
        if not User.objects.filter(email=email).exists():
            with transaction.atomic():
                user = User.objects.create_user(
                    email = email,
                    username = request.data.get('username'),
                    password = request.data.get('password')
                )
                thread = threading.Thread(target=enrich_data, args=(user.id, request.META.get('REMOTE_ADDR')))
                thread.start()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError('Email already exists')

class UserDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user