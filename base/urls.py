from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('board/<str:pk>', views.board, name='board'),
    path('create_board/', views.createBoard, name='create-board'),
    path('update_board/<str:pk>/', views.updateBoard, name='update-board'),
    path('board/<str:pk>/create_card/', views.createCard, name='create-card'),
    path('update_card/<str:pk>', views.updateCard, name='update-card'),
]