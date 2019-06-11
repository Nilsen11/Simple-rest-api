from django.urls import path

from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostList.as_view(), name='show-posts'),
    path('<int:pk>/', views.PostDetail.as_view(), name="post-detail"),
    path('like/<str:title>/', views.PostListLike.as_view(), name='post-like'),
    path('unlike/<str:title>/', views.PostListUnLike.as_view(), name='post-unlike'),
    path('create/', views.CreatePost.as_view(), name='create-post'),
    path('username/<str:username>/', views.UserPosts.as_view(), name='post-username'),
]
