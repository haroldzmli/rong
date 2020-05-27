from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
# from rest_framework_jwt import views
from tileserver.views import MapViewSet, UserLayerViewSet

router = DefaultRouter()
# router.register('maps/layer/', UserLayerViewSet, 'layer')
urlpatterns = [
    path('maps/layer/user/<int:user_id>/', MapViewSet.as_view(), name='map_search_create'),
    path('maps/layer/user/detail/<int:pk>/', views.map_detail, name='map_detail_get_put_delete'),

    path('maps/data/user/<int:user_id>/', UserLayerViewSet.as_view({'get': 'list',
    'post': 'create'}), name='layerdata_detail_search_create'),
    path('maps/data/user/detail/<int:pk>/', views.map_data_detail, name='layerdata_detail_get_put_delete'),

    path('tileserver', views.tile, name='tileserver'),
    path('vectorserver/<str:layer>/<str:filename>/', views.vectordata, name='vectorserver'),
    path('vectorserver/<str:layer>/<str:font>/<str:fontid>/', views.vectordatafont, name='vectorserverfont'),


    # path('tokentest/', views.tokentest, name='tokentest'),
    # path('<str:type>/<str:time>/<int:x>/<int:y>/<int:z>/', views.weather, name='weather'),

]
urlpatterns += router.urls

# urlpatterns += router.urls


# from __future__ import unicode_literals
#
# from django.conf.urls import url
#
# from rest_framework_jwt import views
# from tests.views import test_view
#
# urlpatterns = [
#     url(r'^auth/$', views.obtain_jwt_token, name='auth'),
#     url(r'^auth/verify/$', views.verify_jwt_token, name='auth-verify'),
#     url(r'^auth/refresh/$', views.refresh_jwt_token, name='auth-refresh'),
#     url(r'^test-view/$', test_view, name='test-view'),
# ]
