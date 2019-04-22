


from django.urls import path,include
from . import views

#lass-based views
#    1. Add an import:  from other_app.views import Home
 #   2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')


from ChatApp.views import home
from ChatApp.views import chat





urlpatterns = [
    path('introduction/',views.introduction),
    path('login/', views.log_in),
    path('logout/',views.log_out),
    path('register/',views.register),
    path('',views.homepage),
    path('registerchat/', home, name='index'),
    path('chat/', chat ,name = 'chat')


]