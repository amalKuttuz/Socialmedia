from django.urls import path
from .import views
from Webapp import views as user_views

from django.contrib.auth import views as auth_views
from Webapp.views import *
urlpatterns = [
    path('feeds', views.newsfeed, name='newsfeed'),
    path('post/<int:pk>',views.post,name="post"),
    path('posts/<int:pk>/like/', views.like_post, name='like_post'),
    path('register/',views.register, name='register'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('viewprofile/<str:username>', views.view_profile, name='viewprofile'),
    path('delete/', views.deletepost, name='deletepost'),
    path('delete_detail/', views.delete_detail, name='deletedetail'),
    path('search', views.search, name='search'),


    # path('comment/<int:pk>/', views.comment, name='comment'),
    path('accounts/profile/', views.profile,name='profile'),
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('posts/<int:pk>/unlike/', views.unlike_post, name='unlike_post'),
    path('comments/<int:pk>/like/', views.like_comment, name='like_comment'),
    path('comments/<int:pk>/unlike/', views.unlike_comment, name='unlike_comment'),
]
