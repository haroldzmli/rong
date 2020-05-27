from django.urls import path
from account import views

urlpatterns = [
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_search_modify_delete'),
    path('user/', views.UsersView.as_view(), name='user_search_modify_delete'),
    path('token/', views.CstdObtainJSONWebToken.as_view(), name='CstdObtainJSONWebToken'),
    # path('token/', views.TestJSONWebTokenAPIView.as_view(), name='TestJSONWebTokenAPIView'),
]

