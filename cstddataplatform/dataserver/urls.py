from django.urls import path
from rest_framework.routers import DefaultRouter
from dataserver import views as dataserverviews
from dataserver.views import UserLabelDataViewSet



router = DefaultRouter()
# router.register('maps/layer/', UserLayerViewSet, 'layer')
urlpatterns = [
    path('label/user/', UserLabelDataViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='label_data_detail_search_create'),
    path('label/user/detail/<int:pk>/', dataserverviews.UserLabelDataDetailViewSet.as_view(),
         name='label_data_detail_get_put_delete'),

]
urlpatterns += router.urls
