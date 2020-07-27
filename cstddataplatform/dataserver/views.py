from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.utils import check_user, check_payload

from account.models import CstdUser
from dataserver.models import UserLabelData
from dataserver.serializers import UserLabelDataSerializer
from utils import geobuf


class UserLabelDataViewSet(ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = UserLabelData.objects.all()
    serializer_class = UserLabelDataSerializer
    # authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        # print('regquesr:', request.GET)
        # token = request.GET.get('token')
        # if token:
        #     user = check_user(check_payload(token))
        #     creator = CstdUser.objects.filter(pk=user.id)
        # else:
        #     # if re
        #     creator = CstdUser.objects.filter(pk=request.user.id)
        print('heheeh')
        queryset = UserLabelData.objects.filter(creator_id=1)
        print('111111')
        serializer = UserLabelDataSerializer(queryset, many=True)
        print('222222')
        # response = Response({'data': {'items': serializer.data, 'total': queryset.count()}, 'code': 20000})
        print('333333', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request):
        userLabelData = request.data
        print('regquesr:', request.GET)
        print(userLabelData['label_data_geojson'])
        pbfbuf = geobuf.encode(userLabelData['label_data_geojson'])
        # userLabelData['label_data_pbf'] = pbfbuf
        decodejson = geobuf.decode(pbfbuf)
        print('decodejson:', decodejson)
        # str = json.dumps(j)
        userLabelData['label_data_geojson']= json.dumps(userLabelData['label_data_geojson'])
        serializer = UserLabelDataSerializer(data=userLabelData)
        if serializer.is_valid():
            print('is valid')
            serializer.save()
        else:
            print('is not valid')
            print(serializer.error_messages, serializer.errors)

        # token = request.GET.get('token')
        # if token:
        #     user = check_user(check_payload(token))
        #     creator = CstdUser.objects.filter(pk=user.id)
        # else:
        #     # if re
        #     creator = CstdUser.objects.filter(pk=request.user.id)
        # label_data = request.FILES.getlist('label_data', None)
        # if not label_data:
        #     return Response({'status': 'file dont null'})
        # else:
        #     returndata = []
        #     userLabelData = request.data
        #     userLabelData['creator'] = creator[0].username
        #     userLabelData["creator_id"] = creator[0].id
        #     userLabelData["label_data"] = label_data

            # for file_obj in files:
            #     print(file_obj)
            #     response = upload_file(file_obj, str(creator[0].id))
            #     mapdata['save_path'] = response['url']
            #     mapdata['save_name'] = response['original']
            #     # if len(mapdata['name']) == '':
            #     if 'name' not in mapdata:
            #         mapdata['name'] = os.path.splitext(mapdata['save_name'])[0]  # 分割，不带后缀名
            #     serializer = MapDataSerializer(data=mapdata)
            #     if serializer.is_valid():
            #         serializer.save()
            #         returndata.append(serializer.data)
            # serializer = MapDataUserSerializer(returndata, many=True)
        # userLabelData['label_data_pbf'] = ''
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLabelDataDetailViewSet(APIView):
    """
    Retrieve, update or delete a code map data.
    """
    # authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    #
    # def get_object_username(self, pk, username):
    #     try:
    #         return Map.objects.get(pk=pk, author=username)
    #     except MapData.DoesNotExist:
    #         raise Http404
    #
    # def get_object_pk(self, pk):
    #     try:
    #         return Map.objects.get(pk=pk)
    #     except MapData.DoesNotExist:
    #         raise Http404

    def get(self, request, pk=None):
        # if request.user.is_staff:
        #     user_data = self.get_object_pk(pk)
        #     serializer = CstdMapSerializer(user_data)
        # else:
        #     user_data = self.get_object_username(pk, request.user)
        #     serializer = CstdMapSerializer(user_data)
        queryset = UserLabelData.objects.filter(pk=pk)
        serializer = UserLabelDataSerializer(queryset.first(), many=False)
        # response = Response({'data': {'items': serializer.data, 'total': queryset.count()}, 'code': 20000})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # print('pk:', pk)
        # userLabelData = UserLabelData.objects.filter(pk=pk)
        # print(userLabelData.first())
        # serializer = UserLabelDataSerializer(userLabelData)
        # return JsonResponse(serializer.data)

    def put(self, request, pk):
        # if request.user.is_staff:
        #     map_data = self.get_object_pk(pk)
        #     serializer = UserLabelDataSerializer(map_data, data=request.data)
        # else:
        #     map_data = self.get_object_username(pk, request.user)
        #     serializer = CstdMapSerializer(map_data, data=request.data)
        #
        queryset = UserLabelData.objects.filter(pk=pk)
        serializer = UserLabelDataSerializer(queryset.first(), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # delete 此处可能需要增加判断，目前这样别的登陆用户可能删除不是自己的数据
    def delete(self, request, pk):
        try:
            user_map = UserLabelData.objects.get(pk=pk)
        except user_map.DoesNotExist:
            return HttpResponse(status=404)
        user_map.delete()
        return HttpResponse(status=204)

