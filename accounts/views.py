from django.shortcuts import render,redirect, get_object_or_404

from reviews.models import Review
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.


def index(request):

    users = User.objects.all()

    context = {
        'users' : users
    }

    return render(request,'accounts/index.html',context)


def signup(request):
    if request.method == 'POST':
        signup_form = CustomUserCreationForm(request.POST)

        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username')
            raw_password = signup_form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            auth_login(request,user)
            return redirect('reviews:main')

    else:
        signup_form = CustomUserCreationForm()

    context = {
        'signup_form' : signup_form
    }
        
    return render(request,'accounts/signup.html',context)


def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            login_form = AuthenticationForm(request,data=request.POST)

            if login_form.is_valid():
                auth_login(request,login_form.get_user()
                )
                return redirect(request.GET.get('next') or 'reviews:index' )
        else:
            login_form = AuthenticationForm()

        context = {
            'login_form':login_form
        }
        return render(request,'accounts/login.html',context)

    else:
        return redirect('accounts:index')

def logout(request):
    auth_logout(request)

    return redirect('reviews:main')

@login_required
def update(request):

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')

    else:
        form = CustomUserChangeForm(instance = request.user)
    context={
        'form':form
    }

    return render(request,'accounts/update.html',context)

@login_required
def profile(request,user_pk):

    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    context = {
        'person': person
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def follow(request,user_pk):
    
    User = get_user_model()
    me = request.user
    you = User.objects.get(pk=user_pk)

    if you == request.user:
        return redirect("accounts:profile", user_pk)

    if you.followers.filter(pk=me.pk).exists():
        you.followers.remove(me)
        is_followed = False

    else:
        you.followers.add(me)
        is_followed = True

    context = {
        'is_followed':is_followed,
        'followings_count':you.followings.count(),
        "followers_count":you.followers.count(),
    }
    return JsonResponse(context)