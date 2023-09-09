# from http.client import HTTPResponse
# from types import NoneType
# from multiprocessing import context
# from email import message, message_from_binary_file
from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.contrib import messages   #for flashmessage which is error mesage when login details are not correct
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
# from django.contrib.auth.models import User
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyuserCreationForm




# from django.template import loader
# from django.http import HttpResponse 
# Create your views here.


def loginpage(request):
    #User login authentication
    page = 'login' #to check if the user could login ,so  that it will render the login form
    if request.user.is_authenticated:  #to prevent a user from typing log-out in the link in the google search to log-out
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower() #to make the user name in lower case
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist' )
        user = authenticate(request,email=email,password=password)

        if user is not None:  #if it is a user or none
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist' ) 
    context = {'page':page}
    return render (request,'base/login_register.html',context)


def logoutUser(request):
    #User logout authentication
    logout(request)
    return redirect('home')


def registerPage(request):
#User Register authentication
    page = 'register'  #to check if the user could login, so that it will render the login form
    form = MyuserCreationForm() # to create a register form for a user
    if request.method == 'POST':
        form = MyuserCreationForm(request.POST)
        if form.is_valid():# to check if the details the user used in registration is valid
            user = form.save(commit=False) #to accecess the new user that register objects like(username,password)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    
    return render(request,'base/login_register.html',{'form':form})


def home(request):
    # to search though a search result in a room 
    # rooms = Room.objects.all() 
    q = request.GET.get('q') if request.GET.get('q') != None  else  ' '        #To check if the request method in the filter has something
    

    # to filter through a search result thats a topic in the room
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5] #to allow only 5 topics to show in the home page

    room_count = rooms.count()   #to get the numbers of rooms available
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #to filter through to see all the latest  topics and activities of people in a group /room
    context = {'rooms':rooms,'topics':topics,
    'room_count': room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)



def room(request,pk):
    room = Room.objects.get(id=pk)
    # message_set.all()  is use to query child objects of a specific room
    room_messages = room.message_set.all() #to make the search filter by the newest message created and to display all the messages in the group
    participants = room.participants.all()  #to show all the users in a Group or a Room using many-to-many relationship
    if request.method == 'POST': #to enable a user to chat\create a message through the chatbox and it will show in the group/room
        message = Message.objects.create(
            user = request.user,
            room = room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user) #to add a user to a group when the user sends a message
        return redirect('room',pk=room.id) #to enable a page reload by it self when a user sends a message and make sure the user is till in the room/group without exist automatically when the page reload due to user message sent
    
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)



def userprofile(request,pk):
    #user profile creation
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() #to get all the user group and room 
    room_messages = user.message_set.all()  # to get all the  messages that a specific user have sent in a group or room for it to display in his profile 
    topics = Topic.objects.all()   # to get all the  topics that a specific user have sent in a group or room for it to display in his profile 
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


@login_required(login_url='login') #to restrict user from creating a room when they are not loged-in
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()  #to display all the topics in the room when the user wants to create a room
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created =Topic.objects.get_or_create(name=topic_name) #to make a user be able to create a topic in the room if the topic exist or does.nt exist ,that's why we use .get_or_create() method 
        
        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        ) # to enable a user to create a new topic when creating a new room
        # form = RoomForm(request.POST)
        # if form.is_valid():
             #to enable the backend get the instance the room when created by a user so as to process it and send it back ti the user to enable the user create the room /group
            # room = form.save(commit=False)
             #to allow only the log-in user to create a group/room when he is loged-in
            # room.host = request.user
            # room.save()
        return redirect('home')
        # request.POST.get('name')
        # print(request.POST)

    context = {'form':form,'topics':topics,}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login') #to restrict user from updating a room when they are not loged-in
def updateRoom(request,pk):
    # to update a Chat in the ChatRoom
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)   #instance is to check if the values match
    topics = Topic.objects.all()  #to display all the topics in the room when the user wants to update a topic in  a room
    if request.user != room.host : #To prevent a user from editing another user's messgae or topic
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created =Topic.objects.get_or_create(name=topic_name) #to make a user be able to update a topic in the room if the topic exist or does'nt exist ,that's why we use .get_or_create() method 
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST,instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')

    context = {'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login') #to restrict user from deleting a room when they are not loged-in
def deleteRoom(request,pk):
    #to delete a chat in the chatRoom
    room = Room.objects.get(id=pk)
    if request.user != room.host : #To prevent a user from deletting another user's messgae or topic
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


@login_required(login_url='login') #to restrict user from deleting a mesage in a group when they are not loged-in
def deleteMessage(request,pk):
    #to delete a chat in the chatRoom
    message = Message.objects.get(id=pk)
    if request.user != message.user : #To allow a user to delete the user's messgae or topic in a group when loged-in
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login') #to restrict user from updating  the user profile  when they are not loged-in
def updateuser(request):
    user = request.user #to get the user values when the user is updating the user profile
    form = UserForm(instance = user)
    #to accept the user input the user put for updating or editing the user profile
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user) #toaccess all the updated requirement , the FILES is for user updating their images or submitting file
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    
    return render(request,'base/update-user.html',{'form':form})


def topicspage(request): #browse topics on mobile version ,the topics page
    # rooms = Room.objects.all() 
    q = request.GET.get('q') if request.GET.get('q') != None  else  ' '        #To check if the request method in the filter has something
    topics = Topic.objects.filter(name__icontains=q)
    return render (request ,'base/topics.html',{'topics':topics})


#to get all the activities on the page ,recent activity and current activity
def activitypage(request):
    room_messages = Message.objects.all
    return render(request,'base/activity.html',{'room_messages':room_messages})