from django.urls import path
from . import views

urlpatterns = [
    #homepage
    path('', views.home, name='home'),

    #managing users
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    #board CRUD
    path('board/<str:pk>', views.board, name='board'),
    path('create_board/', views.createBoard, name='create-board'),
    path('update_board/<str:pk>/', views.updateBoard, name='update-board'),
    path('delete_board/<str:pk>', views.deleteBoard, name='delete-board'),

    #card CRUD
    path('board/<str:pk>/create_card/', views.createCard, name='create-card'),
    path('update_card/<str:pk>', views.updateCard, name='update-card'),
    path('delete_card/<str:pk>', views.deleteCard, name='delete-card'),
]