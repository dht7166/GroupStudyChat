from django.urls import path,include
from . import views




urlpatterns = [
    path('create_room/',views.create_room),
    path('lobby/',views.lobby),
	# path('room/',views.room),
    path('<int:roomid>/',views.room),
    path('',views.lobby)
]