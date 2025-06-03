from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from .models import User, UserDetails
from django.contrib.auth.models import User as Auth_User
from django.contrib.auth import  authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
# Create your views here.


def firstFunction(request):
    template = loader.get_template("first.html")
    return HttpResponse(template.render())
    return HttpResponse("first response")
@login_required
def users(request):
    users = User.objects.order_by('-id').filter(details__isnull=False)
    return render(request, 'users/list.html',{'users':users})
@login_required
def create(request):
    if(request.method == "POST"):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        tele_phone = request.POST.get('telephone')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        profile_picture = request.FILES.get('profile_picture')

        user = User.objects.create(
            firstname=first_name,
            lastname=last_name,
            telephone=tele_phone
        )

                # Step 2: Create user details
        UserDetails.objects.create(
            user=user,
            country=country,
            state=state,
            city=city,
            profile_picture=profile_picture
        )

    #     return HttpResponse(request.POST)
    return render(request, 'users/create.html')
@login_required
def deleteUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect("users.index")
@login_required
def updateUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Ensure the user has a related UserDetails object
    details = getattr(user, 'details', None)
    if not details:
        details = UserDetails(user=user)

    if request.method == "POST":
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        telephone = request.POST.get('telephone')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        profile_picture = request.FILES.get('profile_picture')

        user.firstname = firstname
        user.lastname = lastname
        user.telephone = telephone
        user.save()

        details.country = country
        details.state = state
        details.city = city
        if profile_picture:
            details.profile_picture = profile_picture
        details.save()

    return render(request, 'users/update.html', {'user': user})


def login(request):
    if request.method == "POST":
        identifier = request.POST.get('username')  # could be username or email
        password = request.POST.get('password')

        user = Auth_User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()

        if user is None:
            messages.error(request, "User does not exist with that username or email.")
            return redirect("users.login")

        if not user.check_password(password):
            messages.error(request, "Incorrect password.")
            return redirect("users.login")

        if not user.is_active:
            messages.error(request, "This account is inactive.")
            return redirect("users.login")

        # Authenticate and login
        user = authenticate(request, username=user.username, password=password)
        if user:
            auth_login(request, user)
            return redirect("users.index")
        else:
            messages.error(request, "Authentication failed. Please try again.")
            return redirect("users.login")

    return render(request, 'auth/login.html')
    
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('password_confirm')
        
        if password != c_password:
            messages.error(request, 'Enter same confirm password.')
            return redirect('users.signup')
        user = Auth_User.objects.create_user( username = user_name, email = email, password = password, first_name = first_name, last_name = last_name)
        if(authenticate(request,username = user_name, password = password)):
            auth_login(request,user)
            return redirect('users.index')
    return render(request, "auth/signup.html")