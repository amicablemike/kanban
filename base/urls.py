from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('board/<str:pk>', views.board, name='board'),
    path('create-board/', views.createBoard, name='create-board'),
]