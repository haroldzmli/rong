import os
import time
# import requests
import simplejson
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication

from account.models import CstdUser
from cstddataplatform.settings import maptileserver, vectordataserver
from tilecloud import TileCoord, Tile, TileStore
from tilecloud.filter.contenttype import ContentTypeAdder
from tileserver.models import Map, MapData
from tileserver.serializers import CstdMapSerializer, MapDataSerializer


class MapViewSet(APIView):
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    # @action(methods=['get'], detail=False)
    def get(self, request, format='json'):
        # token = request.data['token']
        # from rest_framework_jwt.utils import jwt_decode_handler
        # toke_user = []
        # toke_user = jwt_decode_handler(token)
        # 获得user_id
        # user_id = toke_user["user_id"]
        # 通过user_id查询用户信息
        # user_info = CstdUser.objects.get(pk=user_id)
        queryset = Map.objects.all()
        serializer = CstdMapSerializer(queryset, many=True)
        return Response({'code': 0, 'data': serializer.data, 'msg': ''},
                        status=status.HTTP_200_OK)
        # user = request.user
        # print('username:', user.username)
        # if user.is_admin:
        #     queryset = CstdUser.objects.all()
        #     serializer = CstdUserSerializer(queryset, many=True)
        #     return Response({'code': 0, 'data': serializer.data, 'msg': ''},
        #                 status=status.HTTP_200_OK)
        # else:
        #     return Response({'code': 0, 'data': "no Authentication,must admin", 'msg': ''},
        #                     status=status.HTTP_200_OK)


class IsAdmin(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        print('cest')
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in SAFE_METHODS:
        #     return True

        # Write permissions are only allowed to the owner of the snippet.
        print(obj.owner)
        return obj.owner == request.user



class UserLayerViewSet(ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    # queryset = MapData.objects.all()
    # serializer_class = MapDataSerializer
    # authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    # authentication_classes = [TokenAuthentication]

    def list(self, request, user_id=None):
        print(user_id)
        # queryset = MapData.objects.all()
        queryset = MapData.objects.filter(author_id=user_id)
        serializer = MapDataSerializer(queryset, many=True)
        return Response({'code': 0, 'data': serializer.data, 'msg': ''},
                        status=status.HTTP_200_OK)

    def create(self, request, user_id=None):
        user = request.user
        print('user_id:', user_id)
        user_info = CstdUser.objects.get(pk=user_id)
        print(user_info)
        mapdata = request.data
        mapdata['author'] = user_info.username
        mapdata['author_id'] = user_id
        print('mapdata:',mapdata)
        serializer = MapDataSerializer(data=mapdata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, user_id=None):
        user = request.user
        serializer = MapDataSerializer(data=request.data)
        try:
            mapdata = MapData.objects.get(pk=request.data['id'])
        except mapdata.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MapDataSerializer(mapdata, data=mapdata)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        # if request.method == 'GET':
        #     serializer = SnippetSerializer(snippet)
        #     return Response(serializer.data)
        #
        # elif request.method == 'PUT':
        #     serializer = SnippetSerializer(snippet, data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, user_id=None):
        user = request.user
        mapdata = MapData.objects.get(pk=request.data['id'])
        mapdata.delete()
        try:
            mapdata = MapData.objects.get(pk=request.data['id'])
            # serializer = MapDataSerializer(data=request.data)
        except mapdata.DoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        mapdata.delete()
        return Response(data={'data':1}, status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.delete()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['post'])
    # def set_password(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = PasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user.set_password(serializer.data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    # @action(detail=False)
    # def recent_users(self, request):
    #     recent_users = User.objects.all().order_by('-last_login')
    #
    #     page = self.paginate_queryset(recent_users)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(recent_users, many=True)
    #     return Response(serializer.data)

# class LayerViewSet(APIView):
#     # authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
#     permission_classes = [IsOwnerOrReadOnly]
#     #
#     # @action(detail=True, methods=['get'], permission_classes=[IsAdmin])
#     # def list(self, request):
#     #     queryset = MapData.objects.all()
#     #     serializer = CstdMapSerializer(queryset, many=True)
#     #     return Response({'code': 0, 'data': serializer.data, 'msg': ''},
#     #                     status=status.HTTP_200_OK)
#
#     def post(self, request):
#         user = request.user
#         serializer = MapDataSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # def retrieve(self, request, pk=None):
#     #     pass
#     #
#     # def update(self, request, pk=None):
#     #     pass
#     #
#     # def partial_update(self, request, pk=None):
#     #     pass
#     #
#     # def destroy(self, request, pk=None):
#     #     pass
#

def format_file_name(name):
    '''
    去掉名称中的url关键字
    '''
    URL_KEY_WORDS = ['#', '?', '/', '&', '.', '%']
    for key in URL_KEY_WORDS:
        name_list = name.split(key)
        name = ''.join(name_list)
    return name


def upload_file(file_obj):
    image_format = 'mbtiles|zip|png|jpg'
    filename = file_obj.name
    filename_list = filename.split('.')
    file_postfix = filename_list[-1]  # 后缀
    if file_postfix.lower() in image_format:
        filename_list_clean = filename_list[:-1]
        file_name = ''.join(filename_list_clean) + str(int(time.time() * 1000))
        file_name = format_file_name(file_name)
        sub_folder = time.strftime("%Y%m")
        upload_folder = os.path.join(settings.MEDIA_ROOT, 'upload', sub_folder)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        absolute_path = os.path.join(upload_folder, file_name) + '.%s' % file_postfix
        destination = open(absolute_path, 'wb+')
        for chunk in file_obj.chunks():
            destination.write(chunk)
        destination.close()
        real_url = os.path.join('/media/', 'upload', sub_folder, file_name) + '.%s' % file_postfix
        response_dict = {'original': filename, 'url': real_url, 'title': 'source_file_tile', 'state': 'SUCCESS',
                         'msg': ''}
    else:
        response_dict = {'original': filename, 'url': '', 'title': 'source_file_tile', 'state': 'FAIL',
                         'msg': 'invalid file format'}
    return response_dict


class UploadDataSet(APIView):
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    """
    todo 断点续传 Breakpoint resume
    上传文件为***.mbtiles ***.zip ****文件夹
    
    其中zip 和 瓦片文件夹要导入到sqltie数据库中，数据库的命名为zip文件名和文件夹名字
    
    保存路径为 /media/upload/用户名/年月/文件名+时间
    同时要保存数据库
    """

    def post(self, request, format=None):
        # token = request.data['token']
        # from rest_framework_jwt.utils import jwt_decode_handler
        # toke_user = []
        # toke_user = jwt_decode_handler(token)
        # 获得user_id
        # user_id = toke_user["user_id"]
        # 通过user_id查询用户信息
        # user_info = CstdUser.objects.get(pk=user_id)
        fileObj = request.FILES.get('upfile', None)
        filename = fileObj.name
        print(filename)
        response = upload_file(fileObj)
        return Response(response, status=status.HTTP_200_OK)
        # user = request.user
        # print('username:', user.username)
        # if user.is_admin:
        #     queryset = CstdUser.objects.all()
        #     serializer = CstdUserSerializer(queryset, many=True)
        #     return Response({'code': 0, 'data': serializer.data, 'msg': ''},
        #                 status=status.HTTP_200_OK)
        # else:
        #     return Response({'code': 0, 'data': "no Authentication,must admin", 'msg': ''},
        #                     status=status.HTTP_200_OK)


def tile(request):
    # token = request.GET.get('token')
    # print(token)
    group = request.GET.get('group')
    layer = request.GET.get('layer')
    z = int(request.GET.get('l'))
    x = int(request.GET.get('x'))
    y = int(request.GET.get('y'))
    token = request.GET.get('access_token')
    print('token:', token)
    dbfile = ''
    if group is not None:
        dbfile = maptileserver[group][layer]
    else:
        dbfile = maptileserver[layer]

    content_type_adder = ContentTypeAdder()
    tilestore = TileStore.load(dbfile)
    if tilestore is None:
        HttpResponse(404)
    else:
        tilecoord = TileCoord(z, x, y)
        tile = Tile(tilecoord)
        tile = tilestore.get_one(tile)
        if tile is None:
            HttpResponse(404)
        if tile.data is None:
            HttpResponse(204)

        tile = content_type_adder(tile)

        # if tile.content_type is not None:
        #     response = HttpResponse(tile.data, content_type=tile.content_type)
        #     response['Access-Control-Allow-Origin'] = "*"
        # if tile.content_encoding is not None:
        #     bottle.response.set_header('Content-Encoding', tile.content_encoding)
        response = HttpResponse(tile.data, content_type=tile.content_type)
        response['Access-Control-Allow-Origin'] = "*"
        return response


def vectordata(request, layer, filename):
    group = request.GET.get('group')
    # layer = request.GET.get('layer')
    # filename = request.GET.get('datafile')
    # print('layer:',layer, ' filename:', filename)
    datapath = ''
    if group is not None:
        datapath = vectordataserver[group][layer]
    else:
        datapath = vectordataserver[layer]
    abfilename = os.path.join(datapath, filename)
    # print(abfilename)
    with open(abfilename, 'rb') as file:
        suffix = os.path.splitext(filename)[1]
        # print('suffix:', suffix)
        if(suffix == '.json'):
            # print('json file')
            response = HttpResponse(file.read())
        else:
            response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['content-Disposition'] = 'attachment;filename='+filename
        response['Access-Control-Allow-Origin'] = "*"
    return response

# https://github.com/shiyunbo/django-file-upload-download/blob/master/file_download/views.py
def vectordatafont(request, layer, font, fontid):
    group = request.GET.get('group')
    # layer = request.GET.get('layer')
    # filename = request.GET.get('datafile')
    # print('layer:',layer, ' filename:', font)
    datapath = ''
    if group is not None:
        datapath = vectordataserver[group][layer]
    else:
        datapath = vectordataserver[layer]
    abfilename = os.path.join(datapath, font, fontid)
    # print(abfilename)
    with open(abfilename, 'rb') as file:
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['content-Disposition'] = 'attachment;filename='+fontid
        response['Access-Control-Allow-Origin'] = "*"
    return response



