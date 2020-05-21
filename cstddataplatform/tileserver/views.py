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
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from cstddataplatform.settings import maptileserver, vectordataserver
from tilecloud import TileCoord, Tile, TileStore
from tilecloud.filter.contenttype import ContentTypeAdder
from tileserver.models import Map
from tileserver.serializers import CstdMapSerializer


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



