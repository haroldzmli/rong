import datetime
import os
import time
from django.conf import settings

from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.models import CstdUser
from cstddataplatform.settings import maptileserver, vectordataserver
from tilecloud import TileCoord, Tile, TileStore
from tilecloud.filter.contenttype import ContentTypeAdder
from tileserver.models import Map, MapData
from tileserver.serializers import CstdMapSerializer, MapDataSerializer, MapDataUserSerializer
from utils.format_response import api_response
from rest_framework_jwt.utils import check_payload, check_user


class MapDataViewSet(ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    # queryset = MapData.objects.all()
    # serializer_class = MapDataSerializer
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        print('regquesr:', request.GET)
        token = request.GET.get('token')
        if token:
            user = check_user(check_payload(token))
            creator = CstdUser.objects.filter(pk=user.id)
        else:
            # if re
            creator = CstdUser.objects.filter(pk=request.user.id)



        queryset = MapData.objects.filter(author_id=creator[0].id)
        serializer = MapDataUserSerializer(queryset, many=True)

        response = Response({'data': {'items': serializer.data, 'total': queryset.count()}, 'code': 20000})
        return response
        #
        # return Response({'code': 0, 'data': serializer.data, 'msg': ''},
        #                 status=status.HTTP_200_OK)

    # 可以上传多个mbtiles zip数据
    #todo 超大型文件的分片传输 目前测试10G数据有报错
    # https://blog.csdn.net/susuzhe123/article/details/90718931
    # https://www.cnblogs.com/linjiqin/p/3731751.html
    def create(self, request):
        token = request.GET.get('token')
        if token:
            user = check_user(check_payload(token))
            creator = CstdUser.objects.filter(pk=user.id)
        else:
            # if re
            creator = CstdUser.objects.filter(pk=request.user.id)

        # print('token:', request.user)
        # print('auth:', request.auth)
        # creator_name = request.user
        # try:
        #     creator = CstdUser.objects.filter(username=creator_name)
        # except CstdUser.DoesNotExist:
        #     user_result_object_format_list = [{"error": "no user authority"}]
        #     code, msg, = 0, status.HTTP_400_BAD_REQUEST
        #     data = dict(value=user_result_object_format_list)
        #     return api_response(code, msg, data)
        #     raise Http404

        files = request.FILES.getlist('file', None)
        if not files:
            return Response({'status': 'file dont null'})
        else:
            returndata = []
            mapdata = request.data
            mapdata['author'] = creator[0].username
            mapdata['author_id'] = creator[0].id
            for file_obj in files:
                print(file_obj)
                response = upload_file(file_obj, str(creator[0].id))
                mapdata['save_path'] = response['url']
                mapdata['save_name'] = response['original']
                # if len(mapdata['name']) == '':
                if 'name' not in mapdata:
                    mapdata['name'] = os.path.splitext(mapdata['save_name'])[0]  # 分割，不带后缀名
                serializer = MapDataSerializer(data=mapdata)
                if serializer.is_valid():
                    serializer.save()
                    returndata.append(serializer.data)
            serializer = MapDataUserSerializer(returndata, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class MapDataDetailViewSet(APIView):
    """
    Retrieve, update or delete a code map data.
    """
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object_username(self, pk, username):
        try:
            return MapData.objects.get(pk=pk, author=username)
        except MapData.DoesNotExist:
            raise Http404

    def get_object_pk(self, pk):
        try:
            return MapData.objects.get(pk=pk)
        except MapData.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if request.user.is_staff:
            user_data = self.get_object_pk(pk)
            serializer = MapDataSerializer(user_data)
        else:
            user_data = self.get_object_username(pk, request.user)
            serializer = MapDataUserSerializer(user_data)
        return JsonResponse(serializer.data)

    def put(self, request, pk):
        if request.user.is_staff:
            map_data = self.get_object_pk(pk)
            serializer = MapDataSerializer(map_data, data=request.data)
        else:
            map_data = self.get_object_username(pk, request.user)
            serializer = MapDataUserSerializer(map_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # delete 此处可能需要增加判断，目前这样别的登陆用户可能删除不是自己的数据
    def delete(self, request, pk):
        try:
            map_data = MapData.objects.get(pk=pk)
        except map_data.DoesNotExist:
            return HttpResponse(status=404)
        map_data.delete()
        return HttpResponse(status=204)


class MapViewSet(APIView):
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """
    列出用户创建的地图
    """

    def get(self, request, format='json'):
        creator_name = request.user
        try:
            creator = CstdUser.objects.filter(username=creator_name)
        except CstdUser.DoesNotExist:
            user_result_object_format_list = [{"error": "no user authority"}]
            code, msg, = 0, status.HTTP_400_BAD_REQUEST
            data = dict(value=user_result_object_format_list)
            return api_response(code, msg, data)
            raise Http404

        maps = Map.objects.filter(creator_id=creator[0].id)
        serializer = CstdMapSerializer(maps, many=True)
        return Response(serializer.data)

    def post(self, request):
        creator_name = request.user
        try:
            creator = CstdUser.objects.filter(username=creator_name)
        except CstdUser.DoesNotExist:
            user_result_object_format_list = [{"error": "no user authority"}]
            code, msg, = 0, status.HTTP_400_BAD_REQUEST
            data = dict(value=user_result_object_format_list)
            return api_response(code, msg, data)
            raise Http404
        map_data = request.data
        map_data['creator'] = creator[0].username
        map_data['creator_id'] = creator[0].id
        serializer = CstdMapSerializer(data=map_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MapDetailViewSet(APIView):
    """
    Retrieve, update or delete a code map data.
    """
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object_username(self, pk, username):
        try:
            return Map.objects.get(pk=pk, author=username)
        except MapData.DoesNotExist:
            raise Http404

    def get_object_pk(self, pk):
        try:
            return Map.objects.get(pk=pk)
        except MapData.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if request.user.is_staff:
            user_data = self.get_object_pk(pk)
            serializer = CstdMapSerializer(user_data)
        else:
            user_data = self.get_object_username(pk, request.user)
            serializer = CstdMapSerializer(user_data)
        return JsonResponse(serializer.data)

    def put(self, request, pk):
        if request.user.is_staff:
            map_data = self.get_object_pk(pk)
            serializer = CstdMapSerializer(map_data, data=request.data)
        else:
            map_data = self.get_object_username(pk, request.user)
            serializer = CstdMapSerializer(map_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # delete 此处可能需要增加判断，目前这样别的登陆用户可能删除不是自己的数据
    def delete(self, request, pk):
        try:
            user_map = Map.objects.get(pk=pk)
        except user_map.DoesNotExist:
            return HttpResponse(status=404)
        user_map.delete()
        return HttpResponse(status=204)

#
# @csrf_exempt
# def map_detail(request, pk):
#     """
#     Retrieve, update or delete a code map data.
#     """
#     try:
#         map_data = Map.objects.get(pk=pk)
#     except map_data.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = CstdMapSerializer(map_data)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = CstdMapSerializer(map_data, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         map_data.delete()
#         return HttpResponse(status=204)


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


def format_file_name(name):
    '''
    去掉名称中的url关键字
    '''
    URL_KEY_WORDS = ['#', '?', '/', '&', '.', '%']
    for key in URL_KEY_WORDS:
        name_list = name.split(key)
        name = ''.join(name_list)
    return name


def upload_file(file_obj, user_id):
    image_format = 'mbtiles|zip'
    # 目前只支持sqlite zip(天地图）格式
    # image_format = 'mbtiles|zip|png|jpg'
    filename = file_obj.name
    filename_list = filename.split('.')
    file_postfix = filename_list[-1]  # 后缀
    if file_postfix.lower() in image_format:
        filename_list_clean = filename_list[:-1]
        file_name = ''.join(filename_list_clean) + str(int(time.time() * 1000))
        file_name = format_file_name(file_name)
        sub_folder = time.strftime("%Y%m")
        upload_folder = os.path.join(settings.MEDIA_ROOT, 'upload', sub_folder, user_id)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        absolute_path = os.path.join(upload_folder, file_name) + '.%s' % file_postfix
        destination = open(absolute_path, 'wb+')
        for chunk in file_obj.chunks():
            # print('111111')
            destination.write(chunk)
        destination.close()
        # real_url = os.path.join('/media/', 'upload', sub_folder, file_name) + '.%s' % file_postfix
        response_dict = {'original': filename, 'url': absolute_path, 'title': 'source_file_tile', 'state': 'SUCCESS'}
    else:
        response_dict = {'original': '', 'url': '', 'title': 'source_file_tile', 'state': 'FAIL',
                         'msg': 'invalid file format'}
    return response_dict


class TestViewSet(APIView):
    def get(self, request, layer=None, filename=None, tileid=None):
        print(layer, " ", filename,  str(tileid))


class TileViewSet(APIView):
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, userid=None, mapname=None):
        z = int(request.GET.get('l'))
        x = int(request.GET.get('x'))
        y = int(request.GET.get('y'))
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTk1MjkyMzk5LCJleHAiOjE1OTc4ODQzOTksInVzZXJfaWQiOjF9.IulCkLFv4GtBf6BXfRozgyMHbA0GEEUhx5br-5qDtVo'#request.GET.get('access_token')
        if token:
            user = check_user(check_payload(token))
            if user.id == userid:
                maps = Map.objects.filter(name=mapname, creator_id=userid)
                mapdatastr = maps[0].map_data
                mapdataids = [int(v) for v in mapdatastr.split(',')]
                for mapdataid in mapdataids:
                    # , author=request.user
                    mapdata = MapData.objects.filter(id=mapdataid, author_id=userid)
                    dbfile = mapdata[0].save_path
                    content_type_adder = ContentTypeAdder()
                    # tilestore = TileStore.load(dbfile)
                    tilestore = TileStore.load('/work/cstd/rong/cstddataplatform/media/upload/202006/1/chn16y20191591065855765.mbtiles')
                    if tilestore is None:
                        HttpResponse(404)
                    else:
                        tilecoord = TileCoord(z, x, y)
                        tile = Tile(tilecoord)
                        tile = tilestore.get_one(tile)
                        if tile is None:
                            HttpResponse(404)
                        if tile.data is None:
                            HttpResponse(404)

                        tile = content_type_adder(tile)

                        # if tile.content_type is not None:
                        #     response = HttpResponse(tile.data, content_type=tile.content_type)
                        #     response['Access-Control-Allow-Origin'] = "*"
                        # if tile.content_encoding is not None:
                        #     bottle.response.set_header('Content-Encoding', tile.content_encoding)
                        response = HttpResponse(tile.data, content_type=tile.content_type)
                        response['Access-Control-Allow-Origin'] = "*"
                        return response
        elif request.user.id == userid:
            maps = Map.objects.filter(name=mapname, creator_id=userid)
            mapdatastr = maps[0].map_data
            mapdataids = [int(v) for v in mapdatastr.split(',')]
            for mapdataid in mapdataids:
                # , author=request.user
                mapdata = MapData.objects.filter(id=mapdataid, author_id=userid)
                dbfile = mapdata[0].save_path
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
                        HttpResponse(404)

                    tile = content_type_adder(tile)

                    # if tile.content_type is not None:
                    #     response = HttpResponse(tile.data, content_type=tile.content_type)
                    #     response['Access-Control-Allow-Origin'] = "*"
                    # if tile.content_encoding is not None:
                    #     bottle.response.set_header('Content-Encoding', tile.content_encoding)
                    response = HttpResponse(tile.data, content_type=tile.content_type)
                    response['Access-Control-Allow-Origin'] = "*"
                    return response
        elif request.auth:
            user = check_user(check_payload(request.auth))
            if user.id == userid:
                maps = Map.objects.filter(name=mapname, creator_id=userid)
                mapdatastr = maps[0].map_data
                mapdataids = [int(v) for v in mapdatastr.split(',')]
                for mapdataid in mapdataids:
                    # , author=request.user
                    mapdata = MapData.objects.filter(id=mapdataid, author_id=userid)
                    dbfile = mapdata[0].save_path
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
                            HttpResponse(404)

                        tile = content_type_adder(tile)

                        # if tile.content_type is not None:
                        #     response = HttpResponse(tile.data, content_type=tile.content_type)
                        #     response['Access-Control-Allow-Origin'] = "*"
                        # if tile.content_encoding is not None:
                        #     bottle.response.set_header('Content-Encoding', tile.content_encoding)
                        response = HttpResponse(tile.data, content_type=tile.content_type)
                        response['Access-Control-Allow-Origin'] = "*"
                        return response
        else:
            return JsonResponse({'error': 'no authority'}, status=400)


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



