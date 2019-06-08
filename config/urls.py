from django.contrib import admin
from django.urls import include, path
from users.views import UserList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/users/', UserList.as_view()),
]
