from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from .models import Entry

# Create your views here.

#Logic to redirect user to login page or guestbook, depeding on whether the user is authenticated
def landing(request):
    context = {}
    #If user has signed in, direct to app
    if request.user.is_authenticated:
        return redirect("guestbookview")
    #If not signed in, direct to login page
    else:
        context["message"] = "Please log in first"
        return render(request, "guestbookapp/login.html", context)

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

def logoutview(request):
    context = {}
    #If user is logged in, log them out, and return to login page
    if request.user is not None and request.method == "POST":
        context["message"] = "Successfully logged out"
        logout(request)
        return render(request, "guestbookapp/login.html", context)
    return redirect("guestbookview")

def guestbookview(request):
    context = {}
    #Only allow authenticated users
    if request.user.is_authenticated:
        #Get all entries and add them to context
        entries = Entry.objects.order_by("-entry_date")
        context["entries"] = entries
        return render(request, "guestbookapp/guestbook.html", context=context)
    return redirect("loginview")

def create_entry(request):
    #POST New entry created, add to db
    context = {}
    if request.method == "POST" and request.user.is_authenticated:
        #Check that mandatory fields are filled
        if request.POST["entry_text"] != "" and request.POST["author"] != "":
            entry_text = request.POST["entry_text"]
            author = request.POST["author"]
            entry_image = request.FILES.get("entry_image", None)
            Entry.objects.create(entry_text=entry_text, author=author, entry_image=entry_image)
            return redirect("guestbookview")
        #If mandatory fields are not filled, send back to creation page with message
        context["message"] = "Please fill in mandatory fields: text and author"
        return render(request, "guestbookapp/create.html", context=context)
    #If user is not authenticated, and GET request, send to login page with message
    elif not request.user.is_authenticated:
        context["message"] = "Please log in first"
        return render(request, "guestbookapp/login.html", context=context)
    #GET request, open the create entry page
    return render(request, "guestbookapp/create.html")