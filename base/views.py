from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string

from .models import Post, PostComment
from .form import PostForm, CustomUserCraetionForm, ProfileForm, UserForm
from .filters import PostFilter
from .decorators import *
import logging

logger = logging.getLogger(__name__)

def home(request):
    try:
        posts = Post.objects.filter(active=True, featured=True)[:3]
        context = {'posts': posts}
        logger.info("Home view accessed successfully")
    except Exception as e:
        logger.error(f"Error occurred in home view: {e}")
        context = {'posts': []}  # Render with empty posts in case of error

    return render(request, 'base/index.html', context)

def posts(request):
    posts = Post.objects.filter(active=True)
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs
    page = request.GET.get('page')
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'myFilter': myFilter,
    }
    return render(request, 'base/posts.html', context)


def post(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        PostComment.objects.create(
            author=request.user.profile,
            post=post,
            body=request.POST['comment']
        )
        messages.success(request, "You're comment was successfuly posted!")

        return redirect('post', slug=post.slug)

    context = {'post': post}
    return render(request, 'base/post.html', context)


def profile(request):
    return render(request, 'base/profile.html')


#CRUD views

@admin_only
@login_required(login_url='home')
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('posts')
    context = {
        'form': form
    }
    return render(request, 'base/post_form.html', context)


@admin_only
@login_required(login_url='home')
def update_post(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts')
    context = {
        'form': form
    }
    return render(request, 'base/post_form.html', context)


@admin_only
@login_required(login_url='home')
def delete_post(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {
        'post': post
    }
    return render(request, 'base/delete.html', context)


def sendEmail(request):
    if request.method == 'POST':
        template = render_to_string('base/email_template.html', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['burgutlochin11@gmail.com']
        )

        email.fail_silently = False
        email.send()

    return render(request, 'base/email_sent.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Little Hack to work around re-building the usermodel
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except:
            messages.error(request, 'User with this email does not exists')
            return redirect('login')

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email OR password is incorrect')

    context = {}
    return render(request, 'base/login.html', context)


def registerPage(request):
    form = CustomUserCraetionForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCraetionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Account successfully created.')

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)

            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'An error has occured with registration')

    context = {
        'form': form
    }
    return render(request, 'base/register.html', context)


def logout1(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    context = {
        'profile': profile
    }
    return render(request, 'base/account.html', context)


@login_required(login_url="home")
def updateProfile(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'base/profile_form.html', context)
