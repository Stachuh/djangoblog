from django.urls import path
from . import views
from django.contrib.auth import views as auth_views







urlpatterns = [
    path('',views.post_list,name='post_list'),
    path('post/<int:pk>',views.post_detail,name='post_detail'),
    path('post/new/',views.post_new,name='post_new'),
    path('post/<int:pk>/edit/',views.post_edit,name='post_edit'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/',views.logout_get,name='logout'),
    path('',views.base,name='base'),
    path('user/<int:pk>',views.user,name='user'),
]