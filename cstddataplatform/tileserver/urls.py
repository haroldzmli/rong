from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
# from rest_framework_jwt import views
from tileserver.views import MapViewSet, UploadDataSet


urlpatterns = [
    path('maps/', MapViewSet.as_view(), name='map'),
    path('maps/upfile/', UploadDataSet.as_view()),
    path('tileserver', views.tile, name='tileserver'),
    path('vectorserver/<str:layer>/<str:filename>/', views.vectordata, name='vectorserver'),
    path('vectorserver/<str:layer>/<str:font>/<str:fontid>/', views.vectordatafont, name='vectorserverfont'),

    # path('tokentest/', views.tokentest, name='tokentest'),
    # path('<str:type>/<str:time>/<int:x>/<int:y>/<int:z>/', views.weather, name='weather'),

]

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
