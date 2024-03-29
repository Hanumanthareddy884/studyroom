from django.shortcuts import render,redirect
from django.db.models import Q #use to query of multiple
from django.contrib.auth.models import User # inbuilt user access
from django.contrib.auth.decorators import login_required #add perticular user
from django.http import HttpResponse
from django.contrib import messages # uses for flass message
from django.contrib.auth import authenticate,login,logout # inbult login,logout and authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message
from .forms import RoomForm, UserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated: # If is already login is redirect to Home page
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password is Invalid")

    context = {'page':page}
    return render(request,"base/login_register.html",context)

def logoutUser(request):
    logout(request)
    return redirect("login")

def registerPage(request):
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # commit false is data is not inserted DB
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Error is occure during registration")

    return render(request,'base/login_register.html',{"form":form})

def home(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains = q)|
        Q(description__icontains=q)
        )
    topics = Topic.objects.all().order_by('room')[0:5]
    room_messages= Message.objects.filter(Q(room__topic__name__icontains=q))

    print(room_messages)
    context = {'rooms':rooms,'topics':topics,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk=None):
    room = Room.objects.get(id=pk)
    messages_model = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user= request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)


    context = {'room':room,'messages_model':messages_model,'participants':participants  }
    return render(request,'base/room.html', context)

def user_profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages= user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}

    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def room_form(request):

    form = RoomForm() # model form
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name =request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host =request.user,
            topic =topic,
            name =request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')

    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form =RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("Your not access")

    if request.method == 'POST':
        topic_name =request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        room.name =request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method =='POST':
        room.delete()
        return redirect('home')
    return render(request,"base/delete.html",{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.method =='POST':
        message.delete()
        return redirect('home')
    return render(request,"base/delete.html",{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form  = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)
    context = {'form':form}
    return render(request,'base/update_user.html',context)

def topicsPage(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    p = Paginator(topics,5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    rooms = Room.objects.all()
    context = {'topics':page_obj,'rooms':rooms,'page_obj':page_obj}
    return render(request,'base/topics.html',context)

def activityPage(request):
    room_message =Message.objects.all()
    print(room_message)
    p = Paginator(room_message,2)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'room_message':page_obj,'page_obj':page_obj}
    return render(request,'base/activity.html',context)