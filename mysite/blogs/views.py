from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from . models import Blogpost, Comment, CustomUser

def index(request):
    return render(request, 'blogs/index.html')

#register contains a big flaw, password is not hashed
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = CustomUser.objects.create_user(username=f'{username}')
            user.password = password
            #the line above does not hash the password, instead it should be like this: user.password = user.set_password(password)
            user.save()
            #printing to see the password as plain text
            print('created-user data:')
            print(user.username, user.password)

            return HttpResponseRedirect(reverse('blogs:blogs_page'))
    form = RegisterForm()
    return render(request, 'blogs/register.html', {"form":form})

def login(request):
    return render(request, 'blogs/login.html')

def blogs_page(request):
    return render(request, 'blogs/blogs_page.html')
