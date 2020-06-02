from django.urls import path
from rest_framework.routers import DefaultRouter
from tileserver import views as tileserverviews
from tileserver.views import MapViewSet, MapDataViewSet


router = DefaultRouter()
# router.register('maps/layer/', UserLayerViewSet, 'layer')
urlpatterns = [
    path('data/user/', MapDataViewSet.as_view({'get': 'list','post': 'create'}),
         name='layerdata_detail_search_create'),
    path('data/user/detail/<int:pk>/', tileserverviews.MapDataDetailViewSet.as_view(), name='mapdata_detail_get_put_delete'),
    path('map/user/', MapViewSet.as_view(), name='map_search_create'),
    path('map/user/detail/<int:pk>/', tileserverviews.MapDetailViewSet.as_view(), name='map_detail_get_put_delete'),

    path('map/user/<str:layer>/<str:filename>/<int:tileid>/', tileserverviews.TestViewSet.as_view(), name='TestViewSet'),

    path('tileserver/<int:userid>/<str:mapname>/', tileserverviews.TileViewSet.as_view(), name='tileserver'),


    path('vectorserver/<str:layer>/<str:filename>/', tileserverviews.vectordata, name='vectorserver'),
    path('vectorserver/<str:layer>/<str:font>/<str:fontid>/', tileserverviews.vectordatafont, name='vectorserverfont'),


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
