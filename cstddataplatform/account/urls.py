from django.conf.urls import url, include
from django.urls import path
from account import views
from rest_framework_jwt import views as jwt_views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_search_modify_delete'),
    path('user/', views.UsersView.as_view(), name='user_search_modify_delete'),
    url(r"^token/$", jwt_views.obtain_jwt_token, name="auth"),


    path('mapdata/<int:pk>/', views.UsersMapDataDetailView.as_view(), name='map_data_search_modify_delete'),
    path('mapdata/', views.UsersMapDataView.as_view(), name='map_data_create_search')
    # path('token/', views.CstdObtainJSONWebToken.as_view(), name='CstdObtainJSONWebToken'),
    # path('token/', views.TestJSONWebTokenAPIView.as_view(), name='TestJSONWebTokenAPIView'),
    # path('accounts/', include('rest_registration.api.urls')),
    # url(r"^auth/verify/$", views.verify_jwt_token, name="auth-verify"),
    # url(r"^auth/refresh/$", views.refresh_jwt_token, name="auth-refresh"),
    # url(r"^impersonate/$", views.impersonate_jwt_token, name="impersonate"),
    # url(r"^test-view/$", test_view, name="test-view"),
    # url(r"^superuser-test-view/$", superuser_test_view, name="superuser-test-view"),
]

