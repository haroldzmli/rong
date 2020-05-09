from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken
from django.utils import timezone

from account.models import CstdUser, CstdUserRole, CstdRole
from account.serializers import CstdUserSerializer
from rest_framework_jwt.settings import  api_settings

class CstdObtainJSONWebToken(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print('is user')
            userObj = serializer.object.get('user') or request.user
            userObj.last_login = timezone.datetime.now()
            userObj.save()
            print('userObj:'+userObj.username)
            from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
            token = jwt_encode_handler(jwt_payload_handler(userObj))
            return Response({'code': 20000, 'data': {'token': token}, 'msg': ''},
                            status=status.HTTP_200_OK)
        else:
            return Response({'code': 0, 'data': "no User", 'msg': ''},
                            status=status.HTTP_200_OK)
        # else:
        #     return JsonResponse({'failed': 'reason'})


        # print('token:', CstdObtainJSONWebToken)
        # # if super(CstdObtainJSONWebToken, self).post(request, *args, **kwargs)
        #
        # return Response({'code': 0, 'data': super(CstdObtainJSONWebToken, self).post(request, *args, **kwargs).data, 'msg': ''},
        #                 status=status.HTTP_200_OK)


class CstdTokenVerifyUser(VerifyJSONWebToken):

    def post(self, request, *args, **kwargs):
        token = request.data['token']
        from rest_framework_jwt.utils import jwt_decode_handler
        toke_user = []
        toke_user = jwt_decode_handler(token)
        # 获得user_id
        user_id = toke_user["user_id"]
        # 通过user_id查询用户信息
        user_info = CstdUser.objects.get(pk=user_id)
        serializer = CstdUserSerializer(user_info)
        return Response({'code': 0, 'data': serializer.data, 'msg': ''},
                        status=status.HTTP_200_OK)
        # token_obj = models.UserToken.objects.filter(token=token).first()
        # if not token_obj:
        #     raise exceptions.AuthenticationFailed('用户认证失败')
        # return (token_obj.user, token_obj.token)
        # serializer = self.get_serializer(data=request.data)
        # print(serializer)
        # print(request.user)
        # if serializer.is_valid():
        #     userObj = serializer.object.get('user') or request.user
        #     # userObj.last_login = timezone.datetime.now()
        #     # userObj.save()
        # return super(CstdTokenVerifyUser, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token', None)
        from rest_framework_jwt.utils import jwt_decode_handler
        toke_user = []
        toke_user = jwt_decode_handler(token)
        # 获得user_id
        user_id = toke_user["user_id"]
        # 通过user_id查询用户信息
        user_info = CstdUser.objects.get(pk=user_id)
        hehe = CstdUserRole.objects.get(pk=1)
        print('hehehe:', hehe)
        cstd_user_roles = CstdUserRole.objects.filter(user=user_id)
        print('serializer:', cstd_user_roles)
        cstd_user_role_list = []
        for cstd_user_role in cstd_user_roles:
            print('cstd_user_role:', cstd_user_role.role)
            role = CstdRole.objects.get(id=cstd_user_role.role)
            print('role:', role)
            cstd_user_role_list.append(role.name)

        serializer = CstdUserSerializer(user_info)

        print('serializer:', cstd_user_role_list)
        data = serializer.data

        data['roles'] = cstd_user_role_list
        data['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
        data['introduction'] = 'I am a super administrator',
        # print
        # 'JSON', json.dumps(data)
        # serializer = CstdUserRoleInfoSerializer(user_info, context={'id': user_id})
        return Response({'code': 20000, 'data': data, 'msg': ''},
                        status=status.HTTP_200_OK)


# class AccountUserLogout(APIView):
#     # authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         return Response({'code': 20000, 'data': "success", 'msg': ''},
#                         status=status.HTTP_200_OK)


# class AccountUserLogout(ViewSet):
#     # authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#     # @method_decorator(ensure_csrf_cookie)
#     def create(self, request):
#         return Response({'code': 20000, 'data': "success", 'msg': ''},
#                         status=status.HTTP_200_OK)


def AccountUserLogout(request):
    return JsonResponse({'code': 20000, 'data': "success", 'msg': ''}, status=status.HTTP_200_OK)


class AccountUserViewSet(ViewSet):
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        print('create :', user.username)
        if user.is_admin:
            serializer = CstdUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'code': 0, 'data': "no Authentication,must admin", 'msg': ''},
                            status=status.HTTP_200_OK)

    def list(self, request, format='json'):
        user = request.user
        print('username:', user.username)
        if user.is_admin:
            queryset = CstdUser.objects.all()
            serializer = CstdUserSerializer(queryset, many=True)
            return Response({'code': 0, 'data': serializer.data, 'msg': ''},
                            status=status.HTTP_200_OK)
        else:
            return Response({'code': 0, 'data': "no Authentication,must admin", 'msg': ''},
                            status=status.HTTP_200_OK)


class AccountUserDetailViewSet(ViewSet):
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = CstdUser.objects.filter(id=pk)
        serializer = CstdUserSerializer(queryset, many=True)
        return Response({'code': 0, 'data': serializer.data, 'msg': ''},status=status.HTTP_200_OK)

    # def update(self, request):
    #     user = request.user
    #     print('username:', user.username)
    #     if user.is_admin:
    #         queryset = CstdUser.objects.all()
    #         serializer = CstdUserSerializer(queryset, many=True)
    #         return Response({'code': 0, 'data': serializer.data, 'msg': ''},
    #                         status=status.HTTP_200_OK)
    #     else:
    #         return Response({'code': 0, 'data': "no Authentication,must admin", 'msg': ''},
    #                         status=status.HTTP_200_OK)
    #
    # def partial_update(self, request, format='json'):
    #     user = request.user
    #     print('username:', user.username)
    #     if user.is_admin:
    #         queryset = CstdUser.objects.all()
    #         serializer = CstdUserSerializer(queryset, many=True)
    #         return Response({'code': 0, 'data': serializer.data, 'msg': ''},
    #                         status=status.HTTP_200_OK)
    #     else:
    #         return Response({'code': 0, 'data': "no Authentication,must admin", 'msg': ''},
    #                         status=status.HTTP_200_OK)
    #
    # def destroy(self, request, format='json'):
    #     user = request.user
    #     print('username:', user.username)
    #     if user.is_admin:
    #         queryset = CstdUser.objects.all()
    #         serializer = CstdUserSerializer(queryset, many=True)
    #         return Response({'code': 0, 'data': serializer.data, 'msg': ''},
    #                         status=status.HTTP_200_OK)
    #     else:
    #         return Response({'code': 0, 'data': "no Authentication,must admin", 'msg': ''},
    #                         status=status.HTTP_200_OK)
