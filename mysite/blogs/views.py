from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from . models import Blogpost, Comment, CustomUser
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'blogs/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = CustomUser.objects.create_user(username=f'{username}')
            user.password = password
            #the line above does not hash the password, instead it should be like this: user.password = user.set_password(password)
            #hashing the password is important in case of a data breach or leak
            user.save()
            #printing to see the password as plain text
            print('created-user data:')
            print(user.username, user.password)
            login(request, user)
            return HttpResponseRedirect(reverse('blogs:blogs_page'))
    form = RegisterForm()
    return render(request, 'blogs/register.html', {"form":form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            print(username, password)
            try:
                #login should be modified as well to use django secure authentication 
                #user = authenticate(request, username=username, password=password)
                user = CustomUser.objects.get(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('blogs:blogs_page'))
            except:
                print('Invalid user trying to login')
 
    form = LoginForm()
    return render(request, 'blogs/login.html', {"form":form})


#non authenticated users should not be able to see content that is for authenticated users
#fix is to add a @login_required decorator that redirects non logged in users to login page
#@login_required
def blogs_page(request):
    return render(request, 'blogs/blogs_page.html')


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('blogs:home'))