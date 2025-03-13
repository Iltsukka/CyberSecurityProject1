from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, NewPostForm, NewCommentForm
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from . models import Blogpost, Comment, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db import connection

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
    if request.method=='POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            post = Blogpost.objects.create(blog_title=title, blog_content=content, pub_date=timezone.now())
            return redirect('blogs:blogs_page')

        
    form = NewPostForm()
    blogs = Blogpost.objects.all()
    if len(blogs) < 4:
        return render(request, 'blogs/blogs_page.html', {"form":form, "blogs":blogs})
    blogs = blogs[(len(blogs) - 3):]
    return render(request, 'blogs/blogs_page.html', {"form":form, "blogs":blogs})


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('blogs:home'))
    
@login_required   
def blog_detail(request, id):
    blog = Blogpost.objects.get(id=id)
    form = NewCommentForm()
    return render(request, 'blogs/blog_detail.html', {'blog':blog, 'form':form})

def add_comment(request, id):
    print('id is ', id)
    if request.method=='POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            print('form is valid')
            comment = form.cleaned_data["comment"]
            # the line below is vulnerable to SQL injection as user can input executable sql code in and cause trouble
            connection.cursor().execute(f"INSERT INTO blogs_comment (blogpost_id, comment) VALUES ({id}, '{comment}')")
            # best practice is to use parameterized quaries where input data is not executable and safe to add to quary
            # FIX: connection.cursor().execute("INSERT INTO blogs_comment (blogpost_id, comment, likes) VALUES (%s, %s, %s)", [id, comment, 0])
            # Alternatively Django ORM can be used for safe quarying
            return redirect('blogs:blog_detail', id=id)
    return redirect('blogs:blog_detail', id=id)
    