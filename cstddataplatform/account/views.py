from django.db import IntegrityError
from django.http import Http404
from django.utils import timezone
from rest_framework import status, authentication, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.models import CstdUser, MapDataUser
from account.serializers import CstdUserSerializer, CstdUserRegistorSerializer, MapDataUserSerializer
from utils.format_response import api_response


class UserDetailView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object_pk(self, pk):
        try:
            return CstdUser.objects.get(pk=pk)
        except CstdUser.DoesNotExist:
            raise Http404

    def get_object_username(self, pk, username):
        try:
            return CstdUser.objects.get(pk=pk, username=username)
        except CstdUser.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if request.user.is_staff:
            user_data = self.get_object_pk(pk)
            serializer = CstdUserSerializer(user_data)
        else:
            user_data = self.get_object_username(pk, request.user)
            serializer = CstdUserRegistorSerializer(user_data)

        user_result_object_format_list = [serializer.data]
        code, msg, = 1, status.HTTP_201_CREATED
        data = dict(value=user_result_object_format_list)
        return api_response(code, msg, data)

    def put(self, request, pk):
        if request.user.is_staff:
            user_data = self.get_object_pk(pk)
            serializer = CstdUserSerializer(user_data, data=request.data)
        else:
            user_data = self.get_object_username(pk, request.user)
            serializer = CstdUserRegistorSerializer(user_data, data=request.data)

        if serializer.is_valid():
            serializer.save()
            user_result_object_format_list = [serializer.data]
            code, msg, = 1, status.HTTP_201_CREATED
            data = dict(value=user_result_object_format_list)
            return api_response(code, msg, data)

        user_result_object_format_list = [serializer.errors]
        code, msg, = 0, status.HTTP_400_BAD_REQUEST
        data = dict(value=user_result_object_format_list)
        return api_response(code, msg, data)

    def delete(self, request, pk):
        user_data = self.get_object_pk(pk)
        user_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegisterView(APIView):

    def post(self, request):
        user_result_object_format_list = []
        code, msg, = 1, status.HTTP_201_CREATED
        serializer = CstdUserRegistorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                user_result_object_format_list = [{"register": "successful"}]
                code, msg, = 1, status.HTTP_201_CREATED
                data = dict(value=user_result_object_format_list)
                return api_response(code, msg, data)
            except IntegrityError as Argument:
                user_result_object_format_list = [{"error":  Argument.args[0]}]
                code, msg, = 0, status.HTTP_201_CREATED
                data = dict(value=user_result_object_format_list)
                return api_response(code, msg, data)

        user_result_object_format_list = [{"error": serializer.errors}]
        code, msg, = 0, status.HTTP_400_BAD_REQUEST
        data = dict(value=user_result_object_format_list)
        return api_response(code, msg, data)


class UsersView(APIView):
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        # print('token:', request.user)
        # print('auth:', request.auth)
        user_data = CstdUser.objects.all()
        serializer = CstdUserSerializer(user_data, many=True)
        return Response(serializer.data)


class UsersMapDataDetailView(APIView):

    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            if request.user.is_staff:
                return MapDataUser.objects.get(pk=pk)
            else:
                return MapDataUser.objects.get(pk=pk, username=request.user)
        except CstdUser.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        user_data = self.get_object(request, pk)
        serializer = MapDataUserSerializer(user_data)

        user_result_object_format_list = [serializer.data]
        code, msg, = 1, status.HTTP_201_CREATED
        data = dict(value=user_result_object_format_list)
        return api_response(code, msg, data)

    def put(self, request, pk):
        user_data = self.get_object(request, pk)
        serializer = CstdUserSerializer(user_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_data = self.get_object(request, pk)
        user_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
