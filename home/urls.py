from home import views
from django.urls import path

urlpatterns = [    
    path('', views.home, name='Home'),
    path('contact/', views.contact, name='Contact'),
    path('about/', views.about, name='About'),
    path('signup/', views.signuppage, name='Signuppage'),
    path('login/', views.loginpage, name='Loginpage'),
    path('logout/', views.logoutpage, name='Logoutpage')
]