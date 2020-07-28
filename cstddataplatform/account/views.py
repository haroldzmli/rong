from django.db import IntegrityError
from django.http import Http404
from django.utils import timezone
from rest_framework import status, authentication, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.utils import check_user, check_payload

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


class UserTokenView(GenericAPIView):

    permission_classes = ()
    authentication_classes = ()

    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user') or request.user
        print('user:', user)
        token = serializer.validated_data.get('token')
        issued_at = serializer.validated_data.get('issued_at')
        response_data = JSONWebTokenAuthentication. \
            jwt_create_response_payload(token, user, request, issued_at)
        # response_data.update(code=20000)
        response = Response({'data': response_data, 'code':20000})

        # if api_settings.JWT_AUTH_COOKIE:
        #     set_cookie_with_token(response, api_settings.JWT_AUTH_COOKIE, token)

        return response


class UserLogoutView(GenericAPIView):
    def post(self, request, *args, **kwargs):

        response = Response({'code': 20000})

        # if api_settings.JWT_AUTH_COOKIE:
        #     set_cookie_with_token(response, api_settings.JWT_AUTH_COOKIE, token)

        return response


class UsersView(APIView):
    # authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    # # permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.GET.get('token')
        print('token:', token)
        print('token:', request.user)
        print('auth:', request.auth)
        if token:
            user = check_user(check_payload(token))
            user_data = CstdUser.objects.filter(pk=user.id)
        else:
            # if re
            user_data = CstdUser.objects.filter(pk=request.user.id)
        #
        # pg = PageNumberPagination()
        # # 获取分页的数据
        # page_roles = pg.paginate_queryset(queryset=user_data, request=request, view=self)
        # # 对数据进行序列化
        # ser = CstdUserSerializer(instance=page_roles, many=True)
        # return pg.get_paginated_response(ser.data, {'code': 20000})






        serializer = CstdUserSerializer(user_data[0])
        serializer.data.update(roles=['admin'])
        data = serializer.data
        data.update({'roles': ['admin']})
        data = dict(data=data)
        data.update({'code': 20000})

        return Response(data)


class TestView(APIView):
    # authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    # # permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.GET.get('token')
        print('token:', token)
        print('token:', request.user)
        print('auth:', request.auth)
        if token:
            user = check_user(check_payload(token))
            user_data = CstdUser.objects.filter(pk=user.id)
        else:
            # if re
            user_data = CstdUser.objects.filter(pk=request.user.id)

        serializer = CstdUserSerializer(user_data, many=True)
        data = serializer.data
        # data = dict(data=data)
        # data.update({'code': 20000})  items total

        response = Response({'data': { 'items': data, 'total': user_data.count()}, 'code': 20000})
        return response


class UsersMapDataDetailView(APIView):

    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # 需要增加只有creator才能有此三种权限。

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
        serializer = MapDataUserSerializer(user_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_data = self.get_object(request, pk)
        user_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersMapDataView(APIView):

    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        map_user_data = JSONParser().parse(request)
        creator_name = request.user
        try:
            creator = CstdUser.objects.filter(username=creator_name)
            map_user_data['creator_id'] = creator.id
        except CstdUser.DoesNotExist:
            user_result_object_format_list = [{"error": "no user authority"}]
            code, msg, = 0, status.HTTP_400_BAD_REQUEST
            data = dict(value=user_result_object_format_list)
            return api_response(code, msg, data)
            raise Http404

        # 可以在map data里进行一次查找确认，此处省略。
        serializer = MapDataUserSerializer(map_user_data)
        user_result_object_format_list = []
        code, msg, = 1, status.HTTP_201_CREATED
        serializer = MapDataUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                user_result_object_format_list = [{"mapdatauser": "successful"}]
                code, msg, = 1, status.HTTP_201_CREATED
                data = dict(value=user_result_object_format_list)
                return api_response(code, msg, data)
            except IntegrityError as Argument:
                user_result_object_format_list = [{"error": Argument.args[0]}]
                code, msg, = 0, status.HTTP_201_CREATED
                data = dict(value=user_result_object_format_list)
                return api_response(code, msg, data)

        user_result_object_format_list = [{"error": serializer.errors}]
        code, msg, = 0, status.HTTP_400_BAD_REQUEST
        data = dict(value=user_result_object_format_list)
        return api_response(code, msg, data)

    def get(self, request):
        creator_name = request.user
        try:
            creator = CstdUser.objects.filter(username=creator_name)
        except CstdUser.DoesNotExist:
            user_result_object_format_list = [{"error": "no user authority"}]
            code, msg, = 0, status.HTTP_400_BAD_REQUEST
            data = dict(value=user_result_object_format_list)
            return api_response(code, msg, data)
            raise Http404
        map_data_user = MapDataUser.objects.get(user_id=creator.id, many=True)
        serializer = MapDataUserSerializer(map_data_user)
        user_result_object_format_list = [serializer.data]
        code, msg, = 1, status.HTTP_201_CREATED
        data = dict(value=user_result_object_format_list)
        return api_response(code, msg, data)



