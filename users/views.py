from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer,MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

# register
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response({
            'user': serializer.data,
            'tokens': tokens
        },status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Вход
@api_view(['POST'])
def login_user(request):
    token_view = TokenObtainPairView.as_view()
    response = token_view(request)

    if response.status_code == status.HTTP_200_OK:
        user = User.objects.get(username=response.data['username'])
        user_data = UserSerializer(user).data
        response.data['user'] = user_data
    return Response(response.data, status=response.status_code)