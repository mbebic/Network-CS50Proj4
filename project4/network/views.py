from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
import json

from .models import User, Post, Relationship
from .forms import NewPostForm


def index(request):
    posts = Post.objects.all()
    pagination = Paginator(posts, 10)

    pg_num = request.GET.get('page', 1)
    pg_obj = pagination.get_page(pg_num)

    if pg_obj.has_previous(): 
        pg_url = f'?page={pg_obj.previous_page_number()}'
    
    elif pg_obj.has_next():
        pg_url = f'?page={pg_obj.next_page_number()}'
    
    else:
        pg_url = ''

    return render(request, "network/index.html", {
        "form": NewPostForm(),
        "posts": pg_obj,
        "pg_obj": pg_obj,
        "pg_url": pg_url
    })

@login_required(login_url="login")
def newpost(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)

        # Checks if form is valid, saves new post to database and redirects user to "posts"
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))
    
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

@login_required(login_url="login")
def userprofile(request, user_id):
    user = User.objects.get(pk=user_id)
    # uname = User.objects.get(username=username)
    posts = Post.objects.filter(author=user_id)
    pagination = Paginator(posts, 10)

    pg_num = request.GET.get('page', 1)
    pg_obj = pagination.get_page(pg_num)

    if pg_obj.has_previous(): 
        pg_url = f'?page={pg_obj.previous_page_number()}'
    
    elif pg_obj.has_next():
        pg_url = f'?page={pg_obj.next_page_number()}'
    
    else:
        pg_url = ''
    
    if not request.user.is_authenticated:
        is_followed = False
    elif user.rel_to_user.filter(rel_fromuser=user, status='yes'):
        is_followed = True
    else:
        is_followed = False

    return render(request, "network/profile.html", {
        "username": user, 
        "posts": pg_obj,
        "pg_obj": pg_obj,
        "pg_url": pg_url,
        'following' : user.rel_from_user.count(),
        'followed_by' : user.rel_to_user.count(),
        "is_following": is_followed or None,
        "lastlogin": f'{user.last_login.strftime("%X")} on {user.last_login.strftime("%x")}'
    })

@csrf_exempt
@login_required(login_url="login")
def following(request, user_id):

    user = User.objects.get(pk=user_id)
    # user = request.GET.get("user") or None
    following = user.rel_from_user.filter(status='yes')
    flwingusers = User.objects.filter(id__in=following.values('rel_touser'))
    posts = Post.objects.filter(author__in=flwingusers)

    
    pagination = Paginator(posts, 10)

    pg_num = request.GET.get('page', 1)
    pg_obj = pagination.get_page(pg_num)

    if pg_obj.has_previous(): 
        pg_url = f'?page={pg_obj.previous_page_number()}'
    
    elif pg_obj.has_next():
        pg_url = f'?page={pg_obj.next_page_number()}'
    
    else:
        pg_url = ''

    return render(request, "network/following.html", {
        "posts": pg_obj,
        "pg_obj": pg_obj,
        "pg_url": pg_url
    })



@csrf_exempt
@login_required(login_url="login")
def updatelikecount(request, post_id):

    user = request.user

    try:
        post = Post.objects.get(pk = post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # If post is liked, unlike it
    if (user.likes.filter(pk=post_id).exists()):
        post.liked_by.remove(user)
        likes_post = False
    # If post is unliked, like it
    else: 
        post.liked_by.add(user)
        likes_post = True
    
    # Saves likes count on post
    likes = post.likes()
    
    return JsonResponse({"postLikes": likes_post, "numLikes": likes}, status=200)

@login_required(login_url="login")
@csrf_exempt
def followunfollow(request, user_id):
    user = User.objects.get(pk=user_id)
    # uname = User.objects.get(username=username)
    posts = Post.objects.filter(author=user_id)
    
    if request.user == user:
        return HttpResponse('You cannot follow yourself.', status=403)

    folunfol_check = user.rel_to_user.filter(rel_fromuser=request.user, status='yes')

    if folunfol_check:
        folunfol_check.delete()
        is_followed = False
        btnflag = 'Follow'

    else:
        folunfol_check = Relationship(rel_fromuser=request.user, rel_touser=user, status='yes')
        folunfol_check.save()
        is_followed = True
        btnflag = 'Following'
    
    response = {
        'username' : user.username,
        'post_count' : user.posts.count(),
        'following' : user.rel_from_user.count(),
        'followed_by' : user.rel_to_user.count(),
        'is_followed' : is_followed,
        'buttonflag': btnflag
    }
    return JsonResponse(response, status=200) 


@login_required(login_url="login")
@csrf_exempt
def editpost(request, post_id):

    if request.method != 'POST':
        return JsonResponse({'error': "POST request required"}, status=400)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': "Post not found"}, status=404)
   
    if request.user != post.author:
        return HttpResponse('You do not have permission to edit this post', status=400)

    postdata = request.body.decode('utf-8')
    postbody = json.loads(postdata)
    postcontent = postbody['content']
    Post.objects.filter(pk=post_id).update(content=f'{postcontent}')
    
    return JsonResponse({'content' : str(postcontent), "msg": "Success"}, status=200)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
