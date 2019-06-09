from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import CreateUserView, ManageUserView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('token-auth/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
]
