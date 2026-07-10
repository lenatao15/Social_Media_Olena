import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FeedProject.settings")

import django
django.setup()

from django.contrib.auth.models import User
from FeedApp.models import Profile, Relationship, Post

'''
to install from requirements.txt
pip install -r requirements.txt
'''

try:
    profile = Profile.objects.get(user__username='olena')
    print(f"Profile: {profile}")
    friends = profile.friends.all()
    print(f"Friends: {list(friends)}")
    friends_profiles = Profile.objects.filter(user__in=friends)
    print(f"Friends profiles: {list(friends_profiles)}")

    friends_values = Profile.objects.filter(user=profile.user).values('friends')
    posts = Post.objects.filter(user__in=friends_values).order_by('-date_posted')
    print(f"Posts: {[p.id for p in posts]}")
except Profile.DoesNotExist:
    print("Olena profile does not exist. Please run seed_db command first.")