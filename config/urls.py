from django.contrib import admin
from django.urls import include, path
from user.views import UserList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/post/', include('post.urls')),
    path('api/users/', UserList.as_view()),
]
