from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('like/<str:title>/', views.PostListLike.as_view()),
    path('unlike/<str:title>/', views.PostListUnLike.as_view()),
]
