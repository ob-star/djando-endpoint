from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request


from user.models import User
from user.serializers.user import UserSerializer
from user.utils.jwt.token import get_tokens_for_user
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class SignUpView(generics.GenericAPIView):
    permission_classes =[]
    serializer_class = UserSerializer
        
    def post(self, request:Request):
        data=request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response ={"message":"Signup successfull","data":serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes =[]
    def post(self,request:Request):
        email =request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        # token=get_tokens_for_user(user_obj)
        
        if user is not None:
            response ={"message":"login successfull","user":str(request.user),"token":user.auth_token.key}
            return Response(data=response, status=status.HTTP_200_OK)
        

        return Response(data={"message":"Invalid email or password"})
    
    def get(self,request:Request):
        response ={"message":"List users successfull","user":str(request.user),"token":str(request.auth)}

        return Response(data=response, status=status.HTTP_200_OK)


class GetView(APIView):
    def get(self, request, format=None):
        content = {
        'user': str(request.user.username), # `django.contrib.auth.User` instance.
        'auth': str(request.auth), # None
        }
        return Response(content)
            