from django.shortcuts import render,redirect
from django.db.models import Q #use to query of multiple
from django.contrib.auth.models import User# inbuilt user access
from django.contrib import messages # uses for flass message
from django.contrib.auth import authenticate,login,logout # inbult login,logout and authenticate
from .models import Room,Topic
from .forms import RoomForm

# Create your views here.
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
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

    context = {}
    return render(request,"base/login_register.html",context)

def logoutUser(request):
    logout(request)
    return redirect("login")

def home(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains = q)|
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    context = {'rooms':rooms,'topics':topics}
    return render(request,'base/home.html',context)

def room(request,pk=None):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request,'base/room.html', context)

def room_form(request):
    form = RoomForm() # model form
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form =RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method =='POST':
        room.delete()
        return redirect('home')
    return render(request,"base/delete.html",{'obj':room})