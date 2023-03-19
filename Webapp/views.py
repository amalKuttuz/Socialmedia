from django.shortcuts import render,redirect
import logging
from django.http import HttpResponseServerError
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import F
from django.shortcuts import HttpResponseRedirect
from django.utils import timezone
import random
# Create your views here.
from django.views.generic import CreateView,FormView,TemplateView,ListView
from .forms import LoginForm,UserRegistrationForm,PostsForm,Posts,Commentform
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserForm, ProfileForm,Commentform,DeleteForm
from django.shortcuts import render, get_object_or_404

from api.models import *

# View for login .
@login_required
def login(self, request):
      #Accept and authenticate login form if request is post
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                messages.error("Try again")
                return redirect("signin")
    else:
        form=LoginForm() #Send login form if request is not post
        return render(request,'login.html',{"form":form})

# View for signin .

def signin(self, request):
    if request.method == 'POST':
    
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            # Update the user's profile with default values
            profile = user.profile
            profile.bio = 'no bio'
            profile.user= user
            messages.success("You can login now")
          
            return redirect("login")
        else:
            messages.error("Try again")
            return redirect("signin")
    else:
        form=UserRegistrationForm()  #Send Reg form if request is not post
        return render(request,'signin.html',{"form":form})

#View for index page

def index(request):
    
        return render(request,'index.html')
    
@login_required
def profile(request):
    posts_feed =Posts.objects.filter(user=request.user)[:10]
    for post in posts_feed:
    
      post.comments = Comments.objects.filter(post=post).order_by('-created_date')[:3]
      post.commentcount=Comments.objects.filter(post=post).count
      post.comment_form = Commentform()
      post.postdeleteform = DeleteForm(initial={'post_id': post.id}) 
      following = request.user.profile.following.all()
      following_count = following.count()
      posts_count =Posts.objects.filter(user=request.user).count
      if request.method == 'POST':
        # Get the forms from the request
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        # Save the forms if they are valid
        if user_form.is_valid() and profile_form.is_valid():
          user_form.save()
          profile_form.save()
          
          # Update the session authentication hash to prevent session hijacking
          update_session_auth_hash(request, user_form.instance)
          
          return redirect('profile')
      else:
        # Render the forms if the request method is not POST
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        users=User.objects.filter(username=request.user)
        profileobjects=Profile.objects.filter(user_id=request.user)
      context = {
        'user_form': user_form,
        'profile_form': profile_form,'profileobjects':profileobjects,'users':users,'following_count':following_count,'posts_count':posts_count,'posts_feed':posts_feed
      }
    return render(request, 'profile.html', context)



@login_required
def newsfeed(request):
  userlist = User.objects.exclude(pk=request.user.pk)
  # select a random set of users
  recommendations = random.sample(list(userlist), 5)
    # Get the latest posts
  posts = Posts.objects.order_by('-created_date')[:10]
        # Get the random users
  users = User.objects.order_by('?')[:5]

  # Get the comments for each post
  for post in posts:
    post.comments = Comments.objects.filter(post=post).order_by('-created_date')[:3]
    post.commentcount=Comments.objects.filter(post=post).count
    post.comment_form = Commentform()
    post.postdeleteform = DeleteForm(initial={'post_id': post.id})
  # Handle POST requests
  if request.method == 'POST':
    form_type = request.POST.get('form_type')
    if form_type == 'comment':
      form = Commentform(request.POST)
      if form.is_valid():
        post1 = Posts.objects.get(id=request.POST['post_id'])
        print(post1)
        # Create a new comment
        comment = Comments(
          comment=form.cleaned_data['comment'],
          post=post1,
          user=request.user,
        )
        comment.save()
      else:
        print(form.errors)
    elif form_type == 'post':
      form = PostsForm(request.POST, request.FILES)
      if form.is_valid():
        # Create a new post
        post = Posts(
          post=form.cleaned_data['post'],
          image=form.cleaned_data['image'],
          user=request.user,
        )
        post.save()
      else:
        print(form.errors)
    return redirect('newsfeed')

  addpostform=PostsForm()

  context = {
        'posts': posts,'addpostform':addpostform,'users': users,'recommendations':recommendations }
  return render(request, 'feed.html', context)



def post(request,pk):
    post = get_object_or_404(Posts, pk=pk)
    commentlist = Comments.objects.filter(post=post)
    post.commentfield=Comments.objects.filter(post=post).count
    form = Commentform()

    post.delete_form = DeleteForm(initial={'post_id': post.id})
     # Get the form for deleting the post
    
    # check if the form has been submitted
    if request.method == 'POST':
        # bind the form to the request data
        form = Commentform(request.POST)
        # check if the form is valid
        if form.is_valid():
            # save the comment to the database
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post', pk=post.pk)
  
    commentfield=Commentform()
    context = {
    'post': post, "commentlist":commentlist,'commentfield':commentfield,"form":form
    }
    return render(request, 'post.html', context)


def like_post(request, pk):
    # retrieve the post to be liked
    post = Posts.objects.get(pk=pk)
    # add the user to the likes many-to-many field
    post.likes.add(request.user)
    return redirect('newsfeed')

def unlike_post(request, pk):
    # retrieve the post to be unliked
    post = Posts.objects.get(pk=pk)
    # remove the user from the likes many-to-many field
    post.likes.remove(request.user)
    return redirect('newsfeed')

def like_comment(request, pk):
    # retrieve the comment to be liked
    comment = Comments.objects.get(pk=pk)
    # add the user to the like many-to-many field
    comment.like.add(request.user)
    return redirect('newsfeed')

def unlike_comment(request, pk):
    # retrieve the comment to be unliked
    comment = Comments.objects.get(pk=pk)
    # remove the user from the like many-to-many field
    comment.like.remove(request.user)
    return redirect('newsfeed')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')    
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
def view_profile(request,username):
   # Get the user's profile
    user = User.objects.get(username=username)
    profile = user.profile

    # Get the list of users that the current user is following
    following = request.user.profile.following.all()
    following_count = following.count()
    id=User.objects.get(username=username)
    posts_count =Posts.objects.filter(user=id).count
    posts_feed =Posts.objects.filter(user=id)

    # Check if the current user is following the user whose profile they are viewing
    is_following = False
    if user in following:
        is_following = True
    context={'profile': profile, 'is_following': is_following, 'user':user,'following_count':following_count,
    'posts_count':posts_count,'posts_feed':posts_feed
    
    }
    # Render the profile template
    return render(request, 'userprofile.html', context)

@login_required
def follow(request, username):
    # Get the user to follow/unfollow
    user_to_follow = User.objects.get(username=username)

    # Get the current user's profile
    profile = request.user.profile

    # Check if the current user is following the user they want to follow/unfollow
    if user_to_follow in profile.following.all():
        # If the user is already following the user, unfollow them
        profile.following.remove(user_to_follow)
    else:
        # If the user is not already following the user, follow them
        profile.following.add(user_to_follow)

    # Save the changes to the profile
    profile.save()

    # Redirect back to the user's profile
    return redirect('viewprofile', username=username)


@login_required
def deletepost(request):
  if request.method == 'POST':
    # Get the form for deleting the post
    deleteform = DeleteForm(request.POST)
    if deleteform.is_valid():
      # Get the post to delete
      post_id = deleteform.cleaned_data['post_id']
      post = Posts.objects.get(id=post_id)

      # Check if the current user is the owner of the post
      if post.user == request.user:
        # Delete the post
        post.delete()

  # Redirect back to the newsfeed
  return redirect('newsfeed')

@login_required
def delete_detail(request):
  if request.method == 'POST':
    # Get the form for deleting the post
    form = DeleteForm(request.POST)
    if form.is_valid():
      # Get the post to delete
      post = get_object_or_404(Posts, pk=form.cleaned_data['post_id'])

      # Check if the current user is the owner of the post
      if post.user == request.user:
        # Delete the post
        post.delete()

        # Redirect to the newsfeed
        return redirect('newsfeed')
  return redirect('newsfeed')



def search(request):
  # Get the search term from the query string
  query = request.GET.get('q')
  # users = User.objects.exclude(pk=request.user.pk)

  # Search for users with matching usernames
  users = User.objects.filter(username__icontains=query).exclude(username=request.user.username)

  # Build the search results as a list of dictionaries
  results = []
  for user in users:
    results.append({
      'username': user.username,
      # 'bio':user.profile.bio,
      'profile_url': '/viewprofile/' + user.username
    })

  # Return the search results as JSON
  return JsonResponse({'results': results})



def delete_comment(request, pk):
    # get the comment to be deleted
    comment = get_object_or_404(Comments, pk=pk)
    # check if the user who created the post is the same as the logged-in user
        # delete the comment
    comment.delete()
    return redirect('newsfeed')
 
    # postsexceptme = Posts.objects.exclude(user_id=request.user)


def recommend_follow(request):
    # get all users except the logged-in user
    users = User.objects.exclude(pk=request.user.pk)
    # select a random set of users
    recommendations = random.sample(list(users), 5)
    # render the template with the recommendations
    return render(request, 'feed.html', {'recommendations': recommendations})