from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


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
