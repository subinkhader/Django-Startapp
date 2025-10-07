from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login, logout 
from django.contrib.auth.hashers import check_password
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username is already exist'})
            elif User.objects.filter(email=email).exists():
                return render(request, 'register,html', {'error': 'Email is already exist'})
            else:
                user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password1)
                user.save()
                print("Registration successful. Please log in.")
                return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:  # check if admin
                return redirect('/admin/')  # redirect admin to Django admin panel
            else:
                auth_login(request, user)
                return redirect(('/'))
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login.html')    
    else:
        return render(request, 'login.html')
    
def logout_user(request):
        logout(request)
        return redirect('/')
        
        