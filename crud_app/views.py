from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User as Auth_User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from .models import User, UserDetails
from functools import wraps


# decorator for redirect logged user to index 
def redirect_authenticated_user(view_func):
    @wraps(view_func) #the name, docstring, and metadata of the original view function (like login) are preserved.
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:index')
        return view_func(request, *args, **kwargs)
    return wrapper
# Function to handle form data creation
def handle_user_form(request, user=None):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    telephone = request.POST.get('telephone')
    country = request.POST.get('country')
    state = request.POST.get('state')
    city = request.POST.get('city')
    profile_picture = request.FILES.get('profile_picture')

    if user:
        user.firstname = first_name
        user.lastname = last_name
        user.telephone = telephone
        user.save()

        details = user.details if user.details else UserDetails(user=user)
        details.country = country
        details.state = state
        details.city = city
        if profile_picture:
            details.profile_picture = profile_picture
        details.save()
    else:
        # Create new user and details
        user = User.objects.create(firstname=first_name, lastname=last_name, telephone=telephone)
        UserDetails.objects.create(user=user, country=country, state=state, city=city, profile_picture=profile_picture)

    return user


def firstFunction(request):
    return render(request, "first.html")


@login_required
def users(request):
    users = User.objects.order_by('-id').filter(details__isnull=False)
    return render(request, 'users/list.html', {'users': users})


@login_required
def create(request):
    if request.method == "POST":
        handle_user_form(request)  # Call function to handle form data creation
        messages.success(request, "User created successfully.")
        return redirect("users:index")

    return render(request, 'users/create.html')


@login_required
def deleteUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()  # Correct way to delete a specific user
    messages.success(request, "User deleted successfully.")
    return redirect("users:index")


@login_required
def updateUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        handle_user_form(request, user)  # Update existing user and details
        messages.success(request, "User updated successfully.")
        return redirect("users:index")

    return render(request, 'users/update.html', {'user': user})

@redirect_authenticated_user
def login(request):
    if request.method == "POST":
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        user = Auth_User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()
        if user and user.check_password(password) and user.is_active:
            user = authenticate(request, username=user.username, password=password)
            if user:
                auth_login(request, user)
                if request.POST.get('next'):
                    return redirect(request.POST.get('next'))
                return redirect("users:index")
            else:
                messages.error(request, "Authentication failed. Please try again.")
        else:
            messages.error(request, "Invalid username or password.")
            
        return redirect("users:login")
    return render(request, 'auth/login.html')

@redirect_authenticated_user
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('password_confirm')

        if password != c_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('users:signup')

        user = Auth_User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        auth_login(request, user)
        return redirect('users:index')

    return render(request, "auth/signup.html")

def auth_logout(request):
    logout(request)
    return redirect('users:login')
