from django.shortcuts import render,redirect, get_object_or_404

 
from reviews.models import Review, Comment
from .models import User,Isowner
from .forms import CustomUserCreationForm, CustomUserChangeForm, IsownerForm
 
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
        return redirect('reviews:index')

def logout(request):
    auth_logout(request)

    return redirect('reviews:main')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,request.FILES, instance = request.user)
        if form.is_valid():
            checker = form.save(commit=False)
            form.user = request.user
            checker.save()
            return redirect('accounts:profile', form.user.pk)
    else:
        form = CustomUserChangeForm(instance = request.user)
    context={
        'form':form
    }

    return render(request,'accounts/update.html',context)

@login_required
def profile(request,user_pk):

    person = get_user_model().objects.get(pk=user_pk)
    comment_list = person.comment_set.all()
    set_comment_list = []
    comment_id_list = []

    for i in comment_list:
        if i.review.id not in comment_id_list:
            comment_id_list.append(i.review.id)
            set_comment_list.append(i)

    context = {
        'person': person,
        'following': person.followings.order_by('followers')[:3],
        'follower': person.followers.order_by('followings')[:3],
        'comment_list':set_comment_list,
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
        'me':me.username,
        'is_followed':is_followed,
        'followings_count':you.followings.count(),
        "followers_count":you.followers.count(),
    }
    return JsonResponse(context)


def to_owner(request):
    if request.method == 'POST':
        form = IsownerForm(request.POST)
        if form.is_valid():
            owner=form.save(commit=False)
            owner.user = request.user
            owner.save()
            return redirect('reviews:index')
    else:
        form = IsownerForm()
    context ={
        'form':form
    }
    return render(request, 'accounts/to_owner.html',context)


def check(request):
    lists = Isowner.objects.all()   
    return render(request,'accounts/check.html',{'lists':lists,})


def approve(request,pk,user_pk):
    if request.user.is_superuser:
        lst = Isowner.objects.get(pk=pk)
        user = get_user_model().objects.get(pk=user_pk)
        user.is_owner = 1
        user.save()
        lst.delete()
        return redirect("accounts:check")