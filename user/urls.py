from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import CreateUserView, ManageUserView
from user.views import UserList

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('token/', obtain_jwt_token, name='token'),
    path('token-refresh/', refresh_jwt_token, name='token-refresh'),
    path('users/', UserList.as_view(), name='users'),
]
