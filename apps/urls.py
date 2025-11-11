from apps import views
from django.urls import path

urlpatterns = [
    path('', views.bloghome, name='BlogHome'),
    path('addpost/', views.addpost, name='AddPost'),
    path('postComment/', views.postcomment, name='PostComment'),
    path('search/', views.search, name='Search'),
    path('<str:slug>/',views.blogpost, name='BlogPost'), 
]