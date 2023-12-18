from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from .models import Entry

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
    context = {}
    #User signs in, authenticate
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["pwd"]
        user = authenticate(username=username, password=password)
        #Login user, if account exists, and open guestbook
        if user is not None:
            login(request, user)
            return redirect("guestbookview")
        #Back to login site, with invalid credentials error
        else:
            context["message"] = "Invalid username or password"
            return render(request, "guestbookapp/login.html", context)
    #Open login site, if GET request    
    return render(request, "guestbookapp/login.html")

def guestbookview(request):
    context = {}
    #Only allow authenticated users
    if request.user.is_authenticated:
        #Get all entries and add them to context
        entries = Entry.objects.order_by("-entry_date")
        context["entries"] = entries
        return render(request, "guestbookapp/guestbook.html", context=context)
    return redirect("loginview")