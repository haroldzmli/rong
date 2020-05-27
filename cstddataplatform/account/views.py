from django.http import Http404
from django.utils import timezone
from rest_framework import status, authentication, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import ObtainJSONWebToken

from account.models import CstdUser
from account.serializers import CstdUserSerializer


class UserDetailView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return CstdUser.objects.get(pk=pk)
        except CstdUser.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        user_data = self.get_object(pk)
        serializer = CstdUserSerializer(user_data)
        return Response(serializer.data)

    def put(self, request, pk):
        user_data = self.get_object(pk)
        serializer = CstdUserSerializer(user_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_data = self.get_object(pk)
        user_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [JSONWebTokenAuthentication]
    # authentication_classes = [BasicAuthentication, JSONWebTokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # token = request.data['token']
        # token = request.query_params.get('Token', None)
        # username = request.META
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if not auth:
            return None
        # user, token = authentication.TokenAuthentication.authenticate(self, request)
        # print(user + token)
        print('token:', request.user)
        print('auth:', request.token)

        user_data = CstdUser.objects.all()
        serializer = CstdUserSerializer(user_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CstdUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({'code': 20000, 'data': {'rong_token': token}, 'msg': ''},
                            status=status.HTTP_200_OK)
        else:
            return Response({'code': 0, 'data': "no rong_token User", 'msg': ''},
                            status=status.HTTP_200_OK)
        # else:
        #     return JsonResponse({'failed': 'reason'})


        # print('token:', CstdObtainJSONWebToken)
        # # if super(CstdObtainJSONWebToken, self).post(request, *args, **kwargs)
        #
        # return Response({'code': 0, 'data': super(CstdObtainJSONWebToken, self).post(request, *args, **kwargs).data, 'msg': ''},
        #                 status=status.HTTP_200_OK)





class TestJSONWebTokenAPIView(GenericAPIView):
    """Base JWT auth view used for all other JWT views (verify/refresh)."""

    permission_classes = ()
    authentication_classes = ()

    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        print('000000')
        # try:
        #     token = self.get_token_from_request(request)
        #     print('token000000:', token)
        # except MissingToken:
        #     return None
        serializer = self.get_serializer(data=request.data)
        print('111111')
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user') or request.user
        token = serializer.validated_data.get('token')
        print('token:', token)
        issued_at = serializer.validated_data.get('issued_at')
        response_data = JSONWebTokenAuthentication. \
            jwt_create_response_payload(token, user, request, issued_at)

        response = Response(response_data)

        # if api_settings.JWT_AUTH_COOKIE:
        #     set_cookie_with_token(response, api_settings.JWT_AUTH_COOKIE, token)

        return response
