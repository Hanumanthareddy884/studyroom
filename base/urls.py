from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('',views.home,name="home"),
    path('room/<int:pk>/',views.room,name="room"),

    path('create-room/',views.room_form,name="create_form"),
    path('update-room/<str:pk>',views.updateRoom,name='updated_room'),
    path('delete-room/<str:pk>',views.deleteRoom,name='delete_room'),
    path('delete-message/<str:pk>',views.deleteMessage,name='delete_message'),

]
