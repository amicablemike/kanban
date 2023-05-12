from django.urls import path
from . import views

urlpatterns = [
    #homepage
    path('', views.home, name='home'),

    #users
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    #boards
    path('board/<str:pk>', views.board, name='board'),
    path('create_board/', views.createBoard, name='create-board'),
    path('update_board/<str:pk>/', views.updateBoard, name='update-board'),
    path('delete_board/<str:pk>', views.deleteBoard, name='delete-board'),
    path('leave_board/<str:pk>', views.leaveBoard, name='leave-board'),

    #cards
    path('board/<str:pk>/create_card/', views.createCard, name='create-card'),
    path('update_card/<str:pk>', views.updateCard, name='update-card'),
    path('delete_card/<str:pk>', views.deleteCard, name='delete-card'),
]