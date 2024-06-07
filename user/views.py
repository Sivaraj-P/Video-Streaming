from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User
from .serializers import LoginSerializer,UserSerializer



class LoginAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        try:
            serializer=LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = authenticate(username=serializer.validated_data.get('email_id'), password=serializer.validated_data.get('password'))
                if not user:
                    return Response( {'detail':"Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({"token":token.key},status=status.HTTP_200_OK)
            else:
                
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response( {'detail':'Something went wrong please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UserApiView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
    
    def get(self,request):
        try:
            user=UserSerializer(User.objects.get(id=request.user.id)).data
            return Response(user,status=status.HTTP_200_OK)
        except:
            return Response({'detail':'User not found'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def post(self,request):
        try:
            user=UserSerializer(data=request.data)
            if user.is_valid():
                user.save()
                return Response(user.data,status=status.HTTP_201_CREATED)
            else:
                 return Response(user.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except :            
            return Response({'detail':'Something went wrong please try again later'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
