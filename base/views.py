from django.shortcuts import render
from django.http import HttpResponse


rooms =[
    {'id':1, 'name':'Lets learn python'},
    {'id':2, 'name':'Laravel Developer'},
    {'id':3 , 'name':'Django Developer'},
]

# Create your views here.
def home(request):
    context = {'rooms':rooms}
    return render(request,'base/home.html',context)

def room(request,pk=None):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
            break
    context = {'room':room}

    return render(request,'base/room.html', context)
