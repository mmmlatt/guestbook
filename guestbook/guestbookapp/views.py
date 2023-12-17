from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate

# Create your views here.

#Logic to redirect user to login page or guestbook, depeding on whether the user is authenticated
def landing(request):
    #If user has signed in, direct to app
    if request.user.is_authenticated:
        return redirect("guestbookview")
    #If not signed in, direct to login page
    else:
        return redirect("loginview")

def loginview(request):
    return render(request, "guestbookapp/login.html")

def guestbookview(request):
    return render(request, "guestbookapp/guestbook.html")