from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserDeleteView, UserDetailView, UserListView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("", UserListView.as_view(), name="users"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="update_user"),
    path("user/<int:pk>/delete/", UserDeleteView.as_view(), name="delete_user")
]
