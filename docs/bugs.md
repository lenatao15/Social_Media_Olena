# Bugs and issues found in tutorial slides

Tracking discrepancies between the tutorial slides and a working implementation.
Status legend: 🔴 real bug · ⚠️ stylistic / minor · 📌 setup gap (not a slide bug)

---

## `Profile` model (FeedApp/models.py)

### 🔴 `created` / `updated` timestamps swapped

**Slide:**

```python
created = models.DateTimeField(auto_now=True)       # wrong — refreshes on every save
updated = models.DateTimeField(auto_now_add=True)   # wrong — set once on create
```

**Should be:**

```python
created = models.DateTimeField(auto_now_add=True)   # set once on create
updated = models.DateTimeField(auto_now=True)       # refreshes on every save
```

**Why it matters:** with the slide version, the field called `created` would change every time the row is saved (so it's not really a "created" timestamp), and `updated` would never change after creation.

---

## `Relationship` model (FeedApp/models.py)

### 🔴 `default="send"` — value not in `STATUS_CHOICES`

**Slide:**

```python
STATUS_CHOICES = (('sent', 'sent'), ('accepted', 'accepted'))
status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="send")  # ← typo
```

**Should be:** `default="sent"`.
**Why it matters:** the default `"send"` does not match any choice key. Saving a `Relationship` without explicitly setting `status` will fail `ModelForm`/admin validation with "Select a valid choice."

### 🔴 `created` / `updated` timestamps swapped

Same issue as in `Profile`.

### ⚠️ `max_length=8` is too tight

`'accepted'` is exactly 8 chars. No room to add longer statuses later (e.g. `'cancelled'` = 9). Not a bug, just brittle. Left as-is to match the slide.

### ⚠️ No `unique_together` on (sender, receiver)

Nothing in the model prevents the same user from sending the same friend request twice — two rows with identical `sender`/`receiver` are allowed. Tutorials commonly skip this; flag if duplicates become a problem.

Suggested fix (when relevant):

```python
class Meta:
    unique_together = ('sender', 'receiver')
```

### ⚠️ No DB-level constraint on `status` values

`choices=STATUS_CHOICES` is Django-level validation only. Raw SQL `INSERT` with `status='banana'` would succeed. Add a `CheckConstraint` if you need DB-level enforcement:

```python
class Meta:
    constraints = [
        models.CheckConstraint(
            check=Q(status__in=['sent', 'accepted']),
            name='relationship_status_valid',
        ),
    ]
```

---

## `Post` model (FeedApp/models.py)

### ⚠️ Field named `username` is actually a `User` FK

**Slide:**

```python
username = models.ForeignKey(User, on_delete=models.CASCADE)
```

Misleading name — `post.username` returns a `User` object, not a string. Conventional names: `user`, `author`, or `posted_by`. Left as-is to match slide.

### 📌 `ImageField` requires Pillow (setup gap, not a slide bug)

`makemigrations` will fail with:

> `ImageField requires the Pillow library.`

To fix:

```bash
pip install Pillow
```

And add `Pillow` to [requirements.txt](../requirements.txt).

### 📌 `upload_to='images'` requires MEDIA settings (setup gap)

[FeedProject/settings.py](../FeedProject/settings.py) currently has no `MEDIA_URL` / `MEDIA_ROOT`. Without them, uploaded files will not be saved/served correctly.

Add to settings.py:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'images'
```

And to [FeedProject/urls.py](../FeedProject/urls.py) (for dev only):

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...existing...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## `Comment` model (FeedApp/models.py)

### 🔴 `related_name='details'` — confusing reverse accessor

**Slide:**

```python
username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
```

**Why it matters:** `user.details.all()` would return the user's comments. The word "details" gives no hint that this is about comments — six months later this is unreadable.

**Suggested fix:** `related_name='comments'` → `user.comments.all()` is self-explanatory.

### ⚠️ Field named `username` is actually a `User` FK

Same issue as in `Post`. `comment.username` returns a `User` object, not a string. Conventional names: `user`, `author`. Left as-is to match slide.

### ⚠️ `blank=True` on an `auto_now_add` field is dead code

**Slide:**

```python
date_added = models.DateTimeField(auto_now_add=True, blank=True)
```

**Why it matters:** `auto_now_add=True` automatically sets `editable=False` (and Django itself already sets `blank=True` internally). A non-editable field is excluded from every `ModelForm` and from the admin — so an explicit `blank=True` flag has nothing to validate against. It's harmless but misleading: a reader might think "this field can be left empty in a form" when in reality the field never appears in any form.

Proof:

```python
from django.forms import modelform_factory
CommentForm = modelform_factory(Comment, fields='__all__')
print(CommentForm.base_fields.keys())  # date_added is NOT there
```

### ⚠️ `text = CharField(max_length=200)` — short and wrong type

- 200 chars is shorter than a tweet — comments are often longer.
- `CharField` is conventionally for short structured strings (names, statuses). For variable-length user content, `TextField` is the convention.

Suggested:

```python
text = models.TextField(max_length=2000)
```

Left as-is to match slide.

### ⚠️ No `related_name` on `post` FK

```python
post = models.ForeignKey(Post, on_delete=models.CASCADE)
```

Reverse accessor defaults to `post.comment_set.all()`. Adding `related_name='comments'` enables `post.comments.all()` — much cleaner, especially in templates: `{% for comment in post.comments.all %}`.

### ⚠️ `__str__` returns full text

For long comments (up to 200 chars) the admin list will be ugly. Consider:

```python
def __str__(self):
    return self.text[:50]
```

Cosmetic, not a bug.

---

## `Like` model (FeedApp/models.py)

### 🔴 No `unique_together` on (user, post)

**Slide:**

```python
class Like(models.Model):
    username = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
```

**Why it matters:** nothing prevents the same user from liking the same post multiple times. The DB would happily store 5 `Like` rows for the same `(user, post)` pair. For a "like" semantically this is a bug — a like must be idempotent.

**Suggested fix:**

```python
class Meta:
    unique_together = ('user', 'post')
```

### ⚠️ Field named `username` is actually a `User` FK

Same issue as in `Post` and `Comment`. Misleading name. Conventional: `user`.

### ⚠️ No timestamp

There's no `created` field — you can't tell when a like was placed. Useful for analytics, ordering ("most recent likes"), or rate-limiting. Suggested:

```python
created = models.DateTimeField(auto_now_add=True)
```

### ⚠️ No `__str__` method

Admin will show `Like object (1)` instead of something readable. Suggested:

```python
def __str__(self):
    return f'{self.user} likes {self.post}'
```

### 🟢 Same `related_name='likes'` on both FKs is fine

`user.likes.all()` and `post.likes.all()` — no conflict because they live on different target models. Both reverse accessors work correctly.

---

## Environment / dependencies

### 📌 `psycopg2` and `psycopg2-binary` won't build on Python 3.12

**Error when running `pip install -r requirements.txt`:**

```
psycopg/psycopgmodule.c:1085:28: error: expression is not assignable
    Py_TYPE(&typecastType) = &PyType_Type;
    ...
ERROR: Could not build wheels for psycopg2, psycopg2-binary
```

**Why it matters:** the pinned versions in [requirements.txt](../requirements.txt) (`psycopg2==2.7.7`, `psycopg2-binary==2.8.5`) predate Python 3.12. The CPython internals they rely on changed (`Py_TYPE` is no longer an lvalue). Compilation fails with clang.

**Why it's not blocking locally:** [FeedProject/settings.py](../FeedProject/settings.py) uses `django.db.backends.sqlite3` for local development. `psycopg2` is the PostgreSQL driver — only needed for the Heroku deployment. Locally it can be skipped.

**Workarounds (pick one):**

1. **Skip them locally** — install everything except psycopg2:
   ```bash
   grep -v -E "^psycopg2|^django-heroku" requirements.txt > req-no-pg.txt
   .venv/bin/pip install -r req-no-pg.txt
   ```
2. **Upgrade to versions that support Python 3.12:**
   ```
   psycopg2-binary>=2.9.9
   ```
   (drop the old pins; remove `psycopg2` source-distribution line entirely — `psycopg2-binary` covers the same need without compilation).
3. **Use Python 3.11** in the venv if you need to stay on the pinned versions.

### 📌 `django-heroku` is also unnecessary locally

In `requirements.txt`. Pulls in `psycopg2` as a dependency, so even if you install psycopg2-binary, this package will try to build psycopg2 again. Skip it locally if you're not deploying to Heroku from this venv.
