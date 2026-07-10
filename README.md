# FeedApp — Django Social Media Project

**Live demo:** https://feedapp-oleg.onrender.com/

A simple social network built with Django: users, posts, comments, likes, and friends.

## Features

- User registration and login (`users` app)
- Create posts with images (My Feed)
- Comment on posts
- Like posts
- Send, accept, and view friend requests
- Friends feed (posts only from your friends)

## Stack

- Python 3 / Django 3.2
- SQLite (default `db.sqlite3`)
- Bootstrap 4 (via `django-bootstrap4`, `django-crispy-forms`)
- Pillow for image uploads

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

App runs at http://127.0.0.1:8000/.

## Project structure

- `FeedProject/` — Django project (settings, root URLs)
- `FeedApp/` — main app: posts, comments, likes, friends
- `users/` — auth: register, login, logout, profile
- `media/` — uploaded images (gitignored)
- `docs/` — project notes
