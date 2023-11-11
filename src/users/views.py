from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404, redirect
from djoser import utils

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import ProfileSerializer, RegistrationcompleteSerializer
from rest_framework.permissions import IsAuthenticated


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )
    #

    def get_object(self):
        return self.request.user

    # def put(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


class ActivateAccountView(APIView):

    def post(self, request):
        serializer = RegistrationcompleteSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            user = Profile.objects.get(pk=utils.decode_uid(uid))
            if default_token_generator.check_token(user, token):
                if user.is_active:
                    return Response({'message': 'User already activated'}, status=status.HTTP_400_BAD_REQUEST)
                user.first_name = request.data.get('first_name')
                user.phone = request.data.get('phone')
                user.role = request.data.get('role')
                user.is_active = True
                user.status = 'active'
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user_id': user.pk,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        return Response({'message': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)