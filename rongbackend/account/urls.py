from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt import views as jwt_views

from . import views
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
# from rest_framework_jwt import views
from account.views import AccountUserViewSet, CstdObtainJSONWebToken, CstdTokenVerifyUser, AccountUserDetailViewSet

router = DefaultRouter()
router.register('users', AccountUserViewSet, 'users')
router.register('users', AccountUserDetailViewSet, 'userdetail')

urlpatterns = [
    path('obtain_token/', CstdObtainJSONWebToken.as_view()),
    path('token2user/', CstdTokenVerifyUser.as_view()),
    # path('users/<int:pk>', AccountUserDetailViewSet.as_view({'get':'retrieve'},)),
]

urlpatterns += router.urls

