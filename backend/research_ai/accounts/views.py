from django.shortcuts import render, redirect
from django.contrib.auth import authenticate as auth_authenticate, login as auth_login, logout as auth_logout
from .forms import RegisterForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth_authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            error = "Invalid username or password."
    return render(request, "accounts/login.html", {"error": error})

def logout(request):
    auth_logout(request)
    return redirect("login")

