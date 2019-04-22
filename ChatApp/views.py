from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def home(request):
	title = "Group Chat"
	return render(request,'main.html',{"title":title})

def chat(request):
	title = "Chat Room"
	username = request.POST.get('username')
	return render(request,'chat.html',{"title":title,"username":request.user.username})