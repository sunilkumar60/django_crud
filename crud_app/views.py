from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import User, UserDetails
from pprint import pprint
# Create your views here.


def firstFunction(request):
    template = loader.get_template("first.html")
    return HttpResponse(template.render())
    return HttpResponse("first response")

def users(request):
    users = User.objects.order_by('-id').filter(details__isnull=False)
    return render(request, 'users/list.html',{'users':users})

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

def deleteUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect("users.index")

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