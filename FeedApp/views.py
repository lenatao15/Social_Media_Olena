from django.shortcuts import render, redirect
from .forms import PostForm, ProfileForm, RelationshipForm
from .models import Post, Comment, Like, Profile, Relationship
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

# When a URL request matches the pattern we just defined, 
# Django looks for a function called index() in the views.py file. 

def index(request):
    """The home page for Learning Log."""
    return render(request, 'FeedApp/index.html')



@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user)
    if not profile.exists():
        profile = Profile.objects.create(user=request.user)
    profile = Profile.objects.get(user=request.user)
    if request.method != 'POST':
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('FeedApp:profile')
    
    context = {'form': form}
    return render(request, 'FeedApp/profile.html', context)

@login_required
def myfeed(request):
    comments_count_list = []
    likes_count_list = []
    posts = Post.objects.filter(user=request.user).order_by('-date_posted')

    for post in posts:
        c_count = Comment.objects.filter(post=post).count()
        l_count = Like.objects.filter(post=post).count()
        comments_count_list.append(c_count)
        likes_count_list.append(l_count)
    zipped_list = zip(posts, comments_count_list, likes_count_list)
    context = {'posts': posts, 'zipped_list': zipped_list}
    return render(request, 'FeedApp/my_feed.html', context)

@login_required
def new_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('FeedApp:myfeed')

    context = {'form': form}
    return render(request, 'FeedApp/new_post.html', context)

@login_required
def friends_feed(request):
    comment_count_list = []
    like_count_list = []
    friends = Profile.objects.filter(user=request.user).values('friends')
    posts = Post.objects.filter(user__in=friends).order_by('-date_posted')
    for p in posts:
        c_count = Comment.objects.filter(post=p).count()
        l_count = Like.objects.filter(post=p).count()
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
    zipped_list = zip(posts, comment_count_list, like_count_list)

    if request.method == 'POST' and request.POST.get("like"):
        post_to_like = request.POST.get("like")
        like_already_exists = Like.objects.filter(post_id=post_to_like, user=request.user)
        if not like_already_exists.exists():
            Like.objects.create(post_id=post_to_like, user=request.user)
            return redirect("FeedApp:friends_feed")

    context = {'posts': posts, 'zipped_list': zipped_list}
    return render(request, 'FeedApp/friends_feed.html', context)

@login_required
def comments(request, post_id):
    if request.method == 'POST' and request.POST.get('btn1'):
        comment = request.POST.get('comment')
        Comment.objects.create(post_id=post_id, user=request.user, text=comment)
    comments = Comment.objects.filter(post_id=post_id).order_by('-date_added')
    post = Post.objects.get(id=post_id)
    context = {'comments': comments, 'post': post}
    return render(request, 'FeedApp/comments.html', context)

@login_required
def friends(request):
    user_profile = Profile.objects.get(user=request.user)

    # Get the profiles of my current friends
    user_friends = user_profile.friends.all()
    user_friends_profiles = Profile.objects.filter(user__in=user_friends)
    
    # Get all relationships (pending and accepted) initiated by me
    user_relationships = Relationship.objects.filter(sender=user_profile)
    request_sent_from_profiles = user_relationships.values('receiver')
    
    # Get eligible profiles to add - exclude myself, current friends, and profiles I have already sent requests to
    profiles_to_add = Profile.objects.exclude(user=request.user).exclude(id__in=user_friends_profiles).exclude(id__in=request_sent_from_profiles)
    
    # Get pending friend requests sent to me
    request_received_profiles = Relationship.objects.filter(receiver=user_profile, status='sent')

    if request.method == 'POST' and request.POST.get('send_requests'):
        receiver_profile_ids = request.POST.getlist('send_requests')
        for receiver_profile_id in receiver_profile_ids:
            receiver_profile = Profile.objects.get(id=receiver_profile_id)
            Relationship.objects.create(sender=user_profile, receiver=receiver_profile, status='sent')
        return redirect('FeedApp:friends')

    if request.method == 'POST' and request.POST.get('receive_requests'):
        incoming_relationship_ids = request.POST.getlist('receive_requests')
        for incoming_relationship_id in incoming_relationship_ids:
            relationship = Relationship.objects.get(id=incoming_relationship_id)
            relationship.status = 'accepted'
            relationship.save()
            user_profile.friends.add(relationship.sender.user)
            relationship.sender.friends.add(user_profile.user)
        return redirect('FeedApp:friends')

    context = {
        'user_friends_profiles': user_friends_profiles,
        'profiles_to_add': profiles_to_add,
        'request_received_profiles': request_received_profiles,
        'user_relationships': user_relationships,
    }
    return render(request, 'FeedApp/friends.html', context)