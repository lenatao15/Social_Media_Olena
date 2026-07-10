# FeedApp User Scenarios

This document details all the user scenarios (use cases) supported by the **FeedApp** application.

---

## Table of Contents
1. [User Registration & Authentication](#1-user-registration--authentication)
   * [1.1 User Registration](#11-user-registration)
   * [1.2 User Login](#12-user-login)
   * [1.3 User Logout](#13-user-logout)
   * [1.4 View & Update User Profile](#14-view--update-user-profile)
2. [Post Management](#2-post-management)
   * [2.1 View My Feed](#21-view-my-feed)
   * [2.2 Create a New Post](#22-create-a-new-post)
3. [Social Feed & Interactions](#3-social-feed--interactions)
   * [3.1 View Friends Feed](#31-view-friends-feed)
   * [3.2 Like a Friend's Post](#32-like-a-friends-post)
   * [3.3 View Comments on a Post](#33-view-comments-on-a-post)
   * [3.4 Add Comment to a Post](#34-add-comment-to-a-post)
4. [Friends & Network Management](#4-friends--network-management)
   * [4.1 View Friends Dashboard](#41-view-friends-dashboard)
   * [4.2 Send Friend Requests](#42-send-friend-requests)
   * [4.3 Accept/Approve Friend Requests](#43-acceptapprove-friend-requests)
5. [Administrative Operations](#5-administrative-operations)
   * [5.1 Admin Panel Access](#51-admin-panel-access)

---

## 1. User Registration & Authentication

### 1.1 User Registration
*   **Actor**: Anonymous Visitor
*   **Goal**: Create a new account to access the social network's features.
*   **Preconditions**: The visitor must not be currently authenticated.
*   **Main Success Flow (Happy Path)**:
    1.  The visitor navigates to the Registration page (`/users/register/`).
    2.  The visitor is presented with the registration form (Username, Password, and Password Confirmation).
    3.  The visitor fills in a unique username and matching passwords, then clicks **Register**.
    4.  The system validates the inputs, creates a new `User` record in the database, and automatically logs the user in.
    5.  The system redirects the user to the Home page (`/`).
*   **Alternative / Exception Flows**:
    *   **Username already exists**: The form validation fails; the system displays an error: *"A user with that username already exists."* The visitor remains on the registration page.
    *   **Passwords do not match**: Validation fails; the system displays: *"The two password fields didn't match."* The visitor remains on the registration page.
    *   **Weak Password**: Validation fails due to password policy issues (e.g., too common, too short, entirely numeric); the system displays specific warning messages and the visitor is prompted to enter a stronger password.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `users:register` &rarr; `users/register/` (defined in [users/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/users/urls.py))
    *   **Django View**: `register` in [users/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/users/views.py)
    *   **Form Class**: `django.contrib.auth.forms.UserCreationForm`
    *   **Template**: `users/templates/registration/register.html`
    *   **Affected Models**: `django.contrib.auth.models.User`

### 1.2 User Login
*   **Actor**: Registered Visitor
*   **Goal**: Authenticate credentials and establish a secure, authenticated session.
*   **Preconditions**: The visitor must have a registered account and must not be currently authenticated.
*   **Main Success Flow (Happy Path)**:
    1.  The visitor navigates to the Login page (`/users/login/`) or clicks **Log In** in the navigation bar.
    2.  The visitor enters their Username and Password, then clicks **Log In**.
    3.  The system verifies the credentials against the database and creates an active session.
    4.  The system redirects the visitor to the Home page (`/`).
*   **Alternative / Exception Flows**:
    *   **Invalid Credentials**: Validation fails; the system displays an alert: *"Your username and password didn't match. Please try again."* The visitor remains on the login page.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `users:login` &rarr; `users/login/` (included from `django.contrib.auth.urls` in [users/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/users/urls.py))
    *   **Django View**: Built-in `django.contrib.auth.views.LoginView`
    *   **Template**: `users/templates/registration/login.html`
    *   **Affected Models**: `django.contrib.auth.models.User`

### 1.3 User Logout
*   **Actor**: Authenticated User
*   **Goal**: End the current active session securely.
*   **Preconditions**: The user must be logged in.
*   **Main Success Flow (Happy Path)**:
    1.  The user clicks the **Log out** link in the navigation bar.
    2.  The system destroys the session data.
    3.  The user is redirected to the Logged Out page (`/users/logout/`), displaying a confirmation message.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `users:logout` &rarr; `users/logout/` (included from `django.contrib.auth.urls` in [users/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/users/urls.py))
    *   **Django View**: Built-in `django.contrib.auth.views.LogoutView`
    *   **Template**: `users/templates/registration/logged_out.html`

### 1.4 View & Update User Profile
*   **Actor**: Authenticated User
*   **Goal**: Manage personal details associated with the user account.
*   **Preconditions**: The user must be logged in.
*   **Main Success Flow (Happy Path)**:
    1.  The user clicks **Profile** in the navigation bar &rarr; routes to `/profile/`.
    2.  The system retrieves the user's `Profile` object (creates one dynamically if it does not already exist).
    3.  The user views their current profile details: First Name, Last Name, Email, Date of Birth, and Bio.
    4.  The user updates any of these fields and clicks **Update Profile**.
    5.  The system validates the form, saves the changes to the `Profile` model in the database, and redirects back to the profile page to display the updated info.
*   **Alternative / Exception Flows**:
    *   **Validation Errors**: If the email formatting is invalid or inputs violate constraints, the form validation fails. The page displays the form containing the user's input alongside warning messages.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:profile` &rarr; `/profile/` (defined in [FeedApp/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/urls.py))
    *   **Django View**: `profile` in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py) (protected by `@login_required`)
    *   **Form Class**: `ProfileForm` in [FeedApp/forms.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/forms.py)
    *   **Template**: `FeedApp/templates/FeedApp/profile.html`
    *   **Affected Models**: `FeedApp.models.Profile` (which maps one-to-one with `User`)

---

## 2. Post Management

### 2.1 View My Feed
*   **Actor**: Authenticated User
*   **Goal**: View a personal chronological timeline of all posts they have created, along with engagement metrics.
*   **Preconditions**: The user must be logged in.
*   **Main Success Flow (Happy Path)**:
    1.  The user clicks **My Feed** in the navigation bar &rarr; routes to `/myfeed`.
    2.  The system queries the database for all `Post` records created by the current user, ordered by `date_posted` in descending order (newest first).
    3.  For each post, the system queries the counts of related `Like` and `Comment` objects.
    4.  The user is shown a list of post cards, displaying the text description, uploaded image (if any), timestamp, total likes, and a link displaying the total comments count.
*   **Alternative / Exception Flows**:
    *   **No Posts**: If the user has not created any posts, the page renders an empty state card saying *"You haven't posted anything yet."* and provides a button to **Create Your First Post**.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:myfeed` &rarr; `/myfeed` (defined in [FeedApp/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/urls.py))
    *   **Django View**: `myfeed` in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py) (protected by `@login_required`)
    *   **Template**: `FeedApp/templates/FeedApp/my_feed.html`
    *   **Affected Models**: `FeedApp.models.Post`, `FeedApp.models.Comment`, `FeedApp.models.Like`

### 2.2 Create a New Post
*   **Actor**: Authenticated User
*   **Goal**: Publish a new post with a text description and an optional image upload.
*   **Preconditions**: The user must be logged in.
*   **Main Success Flow (Happy Path)**:
    1.  The user clicks the **New Post** button in the navigation header or on their feed page &rarr; routes to `/new_prost/`.
    2.  The user is shown a form containing:
        *   Description textarea (*"What would you like to say?"*)
        *   Image file upload input
    3.  The user enters a description, selects an image file from their device, and clicks **Post**.
    4.  The system processes the text and the uploaded image (verifying format safety using Pillow), creates a new `Post` record linked to the logged-in user, and saves the image to the `media/images` directory.
    5.  The user is redirected to the **My Feed** page (`/myfeed`), showing the new post at the top.
*   **Alternative / Exception Flows**:
    *   **Invalid File Upload**: If the user uploads a non-image file or a corrupted image, validation fails. The page displays an error message indicating a bad file format, and no post is created.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:new_post` &rarr; `/new_prost/` (defined in [FeedApp/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/urls.py))
    *   **Django View**: `new_post` in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py) (protected by `@login_required`)
    *   **Form Class**: `PostForm` in [FeedApp/forms.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/forms.py)
    *   **Template**: `FeedApp/templates/FeedApp/new_post.html`
    *   **Affected Models**: `FeedApp.models.Post`

---

## 3. Social Feed & Interactions

### 3.1 View Friends Feed
*   **Actor**: Authenticated User
*   **Goal**: View a unified feed of all posts published by the user's friends, ordered by the latest post first.
*   **Preconditions**: The user must be logged in and must have established friendships with other users.
*   **Main Success Flow (Happy Path)**:
    1.  The user clicks **Friends Feed** in the navigation bar &rarr; routes to `/friends_feed/`.
    2.  The system fetches the profiles of all users who are in the current user's `friends` list.
    3.  The system queries the database for all `Post` records where the author is in the friends list, ordered by `date_posted` in descending order.
    4.  The system counts likes and comments for each post.
    5.  The user is shown a feed of post cards displaying the friend's username avatar, timestamp, post description, image (if uploaded), a "Like" button with the like count, and a comment count link.
*   **Alternative / Exception Flows**:
    *   **No Friends or No Friend Posts**: If the user has no friends or their friends have not posted anything, the page renders an empty state card saying *"No posts to display from your friends."* and displays a button to **Find and Add Friends** which links to the Friends Manager.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:friends_feed` &rarr; `/friends_feed/` (defined in [FeedApp/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/urls.py))
    *   **Django View**: `friends_feed` in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py) (protected by `@login_required`)
    *   **Template**: `FeedApp/templates/FeedApp/friends_feed.html`
    *   **Affected Models**: `FeedApp.models.Post`, `FeedApp.models.Profile`, `FeedApp.models.Like`, `FeedApp.models.Comment`

### 3.2 Like a Friend's Post
*   **Actor**: Authenticated User
*   **Goal**: Express appreciation for a post published by a friend.
*   **Preconditions**: The user must be logged in and must be viewing the Friends Feed page.
*   **Main Success Flow (Happy Path)**:
    1.  On the Friends Feed page (`/friends_feed/`), the user locates a post they want to like and clicks the red heart **Like** button.
    2.  The browser sends a POST request containing the `like` parameter (value set to the `post_id`).
    3.  The system checks if a `Like` record already exists for the combination of this post and the current user.
    4.  If no duplicate exists, the system creates a new `Like` record.
    5.  The system redirects the user back to the Friends Feed page, updating the like count display for that post.
*   **Alternative / Exception Flows**:
    *   **Post Already Liked**: If the user has already liked the post, the view checks and ignores the request, avoiding duplicate database entries (and enforcing the `Like` model's `unique_together` constraint).
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:friends_feed` &rarr; `/friends_feed/` (POST request)
    *   **Django View**: `friends_feed` POST handling in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py)
    *   **Affected Models**: `FeedApp.models.Like`, `FeedApp.models.Post`

### 3.3 View Comments on a Post
*   **Actor**: Authenticated User
*   **Goal**: Read comments left by other users on a specific post.
*   **Preconditions**: The user must be logged in.
*   **Main Success Flow (Happy Path)**:
    1.  The user clicks on the comment count link/icon on any post card (from either My Feed or Friends Feed).
    2.  The browser navigates to `/comments/<post_id>/`.
    3.  The system retrieves the target `Post` object and all associated `Comment` records, ordered by `date_added` descending.
    4.  The user is shown a page with the full original post card at the top, and a list of comments below, displaying the author username, comment text, and timestamp.
*   **Alternative / Exception Flows**:
    *   **No Comments Yet**: If no comments have been posted yet, the page displays a placeholder message: *"No comments yet. Be the first to share your thoughts!"*.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:comments` &rarr; `/comments/<int:post_id>/` (defined in [FeedApp/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/urls.py))
    *   **Django View**: `comments` in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py) (protected by `@login_required`)
    *   **Template**: `FeedApp/templates/FeedApp/comments.html`
    *   **Affected Models**: `FeedApp.models.Post`, `FeedApp.models.Comment`

### 3.4 Add Comment to a Post
*   **Actor**: Authenticated User
*   **Goal**: Post a comment/reply on a specific post.
*   **Preconditions**: The user must be logged in and viewing the comments page of that post.
*   **Main Success Flow (Happy Path)**:
    1.  On the comments page (`/comments/<post_id>/`), the user scrolls to the **Add Comment** form.
    2.  The user enters text in the comment input field and clicks **Submit**.
    3.  The form sends a POST request with the comment payload.
    4.  The system creates a new `Comment` record associated with the post and the current user.
    5.  The system refreshes the comments page, showing the newly created comment at the top of the comments list.
*   **Alternative / Exception Flows**:
    *   **Empty Comment**: The input field uses the HTML5 `required` attribute. If a user tries to submit an empty input, the browser blocks the request and prompts the user to enter text.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:comments` &rarr; `/comments/<int:post_id>/` (POST request with `btn1` parameter)
    *   **Django View**: `comments` in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py)
    *   **Template**: `FeedApp/templates/FeedApp/comments.html`
    *   **Affected Models**: `FeedApp.models.Comment`, `FeedApp.models.Post`

---

## 4. Friends & Network Management

### 4.1 View Friends Dashboard
*   **Actor**: Authenticated User
*   **Goal**: Monitor current friendships, inspect pending requests sent/received, and find other users to connect with.
*   **Preconditions**: The user must be logged in.
*   **Main Success Flow (Happy Path)**:
    1.  The user clicks **Friends** in the navigation bar &rarr; routes to `/friends/`.
    2.  The system gathers all relevant user relationship data:
        *   **My Friends**: Users currently linked as mutual friends in the user's `Profile` object.
        *   **Friend Requests Sent**: List of users the current user sent requests to (relationship records where the current user is the `sender`).
        *   **Send a Request (Recommendations)**: Users who are *not* currently friends and have *no* pending requests sent by the current user.
        *   **Friend Requests Received**: Incoming relationships where the current user is the `receiver` and status is still `'sent'`.
    3.  The user is presented with a dashboard organized into four panels mapping these categories.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:friends` &rarr; `/friends/` (defined in [FeedApp/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/urls.py))
    *   **Django View**: `friends` in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py) (protected by `@login_required`)
    *   **Template**: `FeedApp/templates/FeedApp/friends.html`
    *   **Affected Models**: `FeedApp.models.Profile`, `FeedApp.models.Relationship`

### 4.2 Send Friend Requests
*   **Actor**: Authenticated User
*   **Goal**: Invite other users to establish a friendship.
*   **Preconditions**: The user must be logged in and viewing the Friends Dashboard page.
*   **Main Success Flow (Happy Path)**:
    1.  On the Friends Dashboard, under the **Send a Request** section, the user identifies one or more users to invite.
    2.  The user selects the checkboxes next to the target users' names.
    3.  The user clicks the **Send Requests** button.
    4.  The browser submits a POST request containing the `send_requests` array of profile IDs.
    5.  For each checked profile, the system creates a new `Relationship` record:
        *   `sender`: current user's profile
        *   `receiver`: target user's profile
        *   `status`: `'sent'`
    6.  The system redirects back to the `/friends/` page. The target users now display in the **Friend Requests Sent** section with a status of `'sent'`.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:friends` &rarr; `/friends/` (POST request with `send_requests` parameter)
    *   **Django View**: `friends` handling in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py)
    *   **Affected Models**: `FeedApp.models.Relationship`, `FeedApp.models.Profile`

### 4.3 Accept/Approve Friend Requests
*   **Actor**: Authenticated User
*   **Goal**: Confirm pending incoming friend requests to establish a mutual friendship.
*   **Preconditions**: The user must be logged in and have pending incoming requests visible in the **Friend Requests Received** card.
*   **Main Success Flow (Happy Path)**:
    1.  Under the **Friend Requests Received** card, the user selects the checkboxes of the requests they want to accept.
    2.  The user clicks **Approve Requests**.
    3.  The browser sends a POST request with the `receive_requests` array containing the selected Relationship IDs.
    4.  For each checked relationship, the system:
        *   Updates the `Relationship` status field from `'sent'` to `'accepted'`.
        *   Adds the sender's `User` object to the receiver's `Profile.friends` list.
        *   Adds the receiver's `User` object to the sender's `Profile.friends` list.
    5.  The system redirects back to the `/friends/` page. The accepted users are now displayed in the **My Friends** table.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `FeedApp:friends` &rarr; `/friends/` (POST request with `receive_requests` parameter)
    *   **Django View**: `friends` handling in [FeedApp/views.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/views.py)
    *   **Affected Models**: `FeedApp.models.Relationship`, `FeedApp.models.Profile`

---

## 5. Administrative Operations

### 5.1 Admin Panel Access
*   **Actor**: Administrator / Superuser
*   **Goal**: Maintain system stability and administer records directly in the backend.
*   **Preconditions**: The user must be registered as a Django Superuser.
*   **Main Success Flow (Happy Path)**:
    1.  The administrator navigates to `/admin/` and logs in using superuser credentials.
    2.  The admin is presented with the Django Administration dashboard.
    3.  The admin can click into any model category (Profiles, Relationships, Posts, Comments, Likes, Users, Groups) to search, add, update, or delete records.
*   **Technical Implementation Details**:
    *   **URL Pattern**: `/admin/` (configured in [FeedProject/urls.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedProject/urls.py))
    *   **Django App**: Built-in `django.contrib.admin`
    *   **Configuration**: Models registered in [FeedApp/admin.py](file:///C:/Documents/Documents/AdvPython/social_media_project/FeedApp/admin.py)
