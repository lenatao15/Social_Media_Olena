from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from FeedApp.models import Profile, Post, Comment, Like, Relationship
from datetime import date, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with dummy users, profiles, posts, comments, and friendships.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing database data...')
        
        # Clear existing data in reverse order of dependencies
        Like.objects.all().delete()
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Relationship.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write('Database cleared. Seeding database...')

        # 1. Create Main User
        main_user = User.objects.create_user(
            username='olena',
            email='olena@example.com',
            password='password123',
            first_name='Olena',
            last_name='Shevchenko'
        )
        # Profile is created automatically in views if missing, but we create it here
        main_profile = Profile.objects.create(
            user=main_user,
            first_name='Olena',
            last_name='Shevchenko',
            email='olena@example.com',
            dob=date(2003, 5, 15),
            bio='CS Student | Explorer of new technologies | Coffee Lover ☕'
        )

        # 2. Create Dummy Users
        users_data = [
            {'username': 'john_doe', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'bio': 'Tech Enthusiast | Code & Design 💻'},
            {'username': 'jane_smith', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com', 'bio': 'Wanderlust 🌍 | Nature Photographer 📸'},
            {'username': 'sam_wilson', 'first_name': 'Sam', 'last_name': 'Wilson', 'email': 'sam@example.com', 'bio': 'Musician 🎸 | Sound Engineer | Retro vibe'},
            {'username': 'lisa_jones', 'first_name': 'Lisa', 'last_name': 'Jones', 'email': 'lisa@example.com', 'bio': 'Fitness Coach 🏃‍♀️ | Plant Parent 🌿'},
        ]

        users = {}
        profiles = {}
        for u_data in users_data:
            user = User.objects.create_user(
                username=u_data['username'],
                email=u_data['email'],
                password='password123',
                first_name=u_data['first_name'],
                last_name=u_data['last_name']
            )
            profile = Profile.objects.create(
                user=user,
                first_name=u_data['first_name'],
                last_name=u_data['last_name'],
                email=u_data['email'],
                bio=u_data['bio']
            )
            users[user.username] = user
            profiles[user.username] = profile

        # 3. Setup Friendships & Relationships
        # John and Jane are active friends of Olena
        main_profile.friends.add(users['john_doe'])
        profiles['john_doe'].friends.add(main_user)

        main_profile.friends.add(users['jane_smith'])
        profiles['jane_smith'].friends.add(main_user)

        # Sam sent a friend request to Olena (Incoming request for Olena)
        Relationship.objects.create(
            sender=profiles['sam_wilson'],
            receiver=main_profile,
            status='sent'
        )

        # Olena sent a friend request to Lisa (Outgoing request from Olena)
        Relationship.objects.create(
            sender=main_profile,
            receiver=profiles['lisa_jones'],
            status='sent'
        )

        # 4. Create Dummy Posts
        posts = []
        
        # John's posts
        p1 = Post.objects.create(
            user=users['john_doe'],
            description='Just deployed my first full-stack Django project! The layout is super clean and the database is running perfectly. #python #webdev'
        )
        posts.append(p1)
        
        p2 = Post.objects.create(
            user=users['john_doe'],
            description='Enjoying a late night coding session. Nothing beats the feeling when your code compiled on the first try!'
        )
        posts.append(p2)

        # Jane's posts
        p3 = Post.objects.create(
            user=users['jane_smith'],
            description='Caught a stunning sunrise over the mountains this morning. Nature never ceases to amaze me. 🌅🏔️'
        )
        posts.append(p3)

        # Olena's post
        p4 = Post.objects.create(
            user=main_user,
            description='Loving the new glassmorphic dark mode UI I just configured for my feed! It looks so alive and stylish. Let me know what you think!'
        )
        posts.append(p4)

        # 5. Create Comments
        Comment.objects.create(
            post=p1,
            user=main_user,
            text='Congrats John! The UI looks incredibly clean. Keep up the awesome work!'
        )
        Comment.objects.create(
            post=p1,
            user=users['jane_smith'],
            text='Wow, impressive! Would love to see the git repo!'
        )
        Comment.objects.create(
            post=p3,
            user=main_user,
            text='Beautiful shot, Jane! The colors are absolutely breathtaking.'
        )
        Comment.objects.create(
            post=p4,
            user=users['john_doe'],
            text='This is next level, Olena! The dark mode styling is really comfortable to look at.'
        )

        # 6. Create Likes
        Like.objects.create(user=main_user, post=p1)
        Like.objects.create(user=users['jane_smith'], post=p1)
        
        Like.objects.create(user=main_user, post=p3)
        Like.objects.create(user=users['john_doe'], post=p3)
        
        Like.objects.create(user=users['john_doe'], post=p4)
        Like.objects.create(user=users['jane_smith'], post=p4)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with dummy data!'))
        self.stdout.write(self.style.SUCCESS('Main User created: olena / password123'))
