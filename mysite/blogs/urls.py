from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login_page', views.login_page, name='login_page'),
    path('blogs_page', views.blogs_page, name='blogs_page'),
    path('logout_page', views.logout_page, name='logout_page')

]