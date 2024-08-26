from api.serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, UserSendpasswordResetMailSerializer, UserPasswordResetSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return{
        'refresh': str(refresh),
        'access' : str(refresh.access_token),
              }

# Create your views here.

class UserRegisterView(APIView):
     def post(self, request):
       serializer = UserRegisterSerializer(data=request.data)
       if serializer.is_valid(raise_exception=True):
           user = serializer.save()
           token = get_tokens_for_user(user)
           data = {'token': token, 'msg': 'Registration Successsul'}
           return Response(data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
class userLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user =authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                data = {'token':token,'msg':'login succcessful'}
                return Response(data,status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['email or password incorrect']}}, status=status.HTTP_404_NOT_FOUND)
            
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
      serializer = UserProfileSerializer(data=request.user)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserChangepasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserChangePasswordSerializer(data = request.data, context= {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            data ={'msg':'password changed successfully'}
            return Response(data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserSendPasswordResetMailView(APIView):
    def post(self, request):
        serializer = UserSendpasswordResetMailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          data = {'msg':'password reset link sent to your email successfully'},
          return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class userpasswordresetview(APIView):
    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
          return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

