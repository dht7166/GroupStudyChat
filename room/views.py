from django.shortcuts import render,redirect
from .forms import RoomForm
from .models import Room, File
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os
import mimetypes
# Create your views here..


def create_room(request):
    if not request.user.is_authenticated:
        return redirect('/homepage/introduction/')
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            private = form.cleaned_data['private']
            new_room = Room(name = name,description = description,private = private)
            new_room.save()
            new_room.users.add(request.user) #adding creator
            # Adding via invitation
            invitation = form.cleaned_data['invitation'].strip().split(',')
            for username in invitation:
                try:
                    user = User.objects.get(username = username)
                    new_room.users.add(user)
                except User.DoesNotExist:
                    pass
            return redirect('/room/lobby/')
        else:
            render(request, 'room/Create_Room.html', {'user': request.user, 'form': form})
    else:
        form = RoomForm()
    return render(request, 'room/Create_Room.html', {'user':request.user,'form':form})


def lobby(request):
    if not request.user.is_authenticated:
        return redirect('/homepage/introduction/')
    current_room = Room.objects.filter(users = request.user)
    return render(request, 'room/Lobby.html', {'user':request.user,'current_room':current_room})


def room(request,roomid):
    class userFile():
        def __init__(self,name):
            self.name = os.path.split(name)[1]
            self.path = name
            self.MIME = mimetypes.MimeTypes().guess_type(name)[0]


    def upload_file(request,myroom):
        myfile = request.FILES['upload']
        fs = FileSystemStorage()
        filename = os.path.join(str(myroom.id),myfile.name)
        filename = fs.save(filename, myfile)
        uploaded_url = fs.url(filename)
        return userFile(uploaded_url)



    if not request.user.is_authenticated:
        return redirect('/homepage/introduction/')
    myroom = Room.objects.get(id = roomid)
    if len(myroom.users.filter(username = request.user.username)) == 0:
        # This user does not belong here
        return redirect('/room/lobby/')
    # Else, render this room for the user
    user_list = myroom.users.all()
    choice = [file.name for file in myroom.file_set.all()]
    # handle file upload request
    if request.method == 'POST' and request.FILES.get('upload',False):
        file = upload_file(request,myroom)
        record_of_file = File(name= file.name,file=file.path,room=myroom)
        record_of_file.save()
        print(file)
        return render(request, 'room/Room.html', {'room': myroom, 'user_list': user_list,'file':file,
                                                  'file_set':myroom.file_set.all() })
    if request.method == 'POST':
        file_to_open = request.POST.get('open_file',False)
        if file_to_open:
            file = userFile(file_to_open)
            return render(request, 'room/Room.html', {'room': myroom, 'user_list': user_list, 'file': file,
                                                      'file_set': myroom.file_set.all()})
    return render(request, 'room/Room.html', {'room':myroom,'user_list':user_list,
                                              'file_set':myroom.file_set.all()})


