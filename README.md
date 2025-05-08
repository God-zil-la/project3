# 📘 Event Planner Web Application

Live Demo: [https://event-plan.herokuapp.com](https://event-plan-10650f39d687.herokuapp.com/register/)

![amiresponsive](readme-img/amiresponsive.jpg)

---

## 📌 Important Note on "Shared Events"

The term **"shared events"** in this project refers to events that are **accessible to all users under a shared account**. It does **not** currently support sharing events **between separate user accounts**.

**This design choice means:**

* All events created within an account are visible and manageable by that account's user.
* There is no functionality for sending, syncing, or exposing events across multiple user accounts.
* This could be expanded in the future by introducing user-to-user permissions or event-sharing invitations.

---

## 🧭 Table of Contents
* 📌 Shared Event Explanation
* 📘 Overview
* 💡 Use Cases
* 👤 User Stories
* 🧑‍💻 Features
* 🔐 User Authentication
* 🗓️ Event Management
* 🔍 Validation
* 🛠️ Technologies Used
* 🧪 Testing
* 🧭 App Navigation
* 📁 Project Structure
* 📘 Entity Relationship Diagram
* 🌍 Deployment
* 💾 Saving to Home Screen
* 🧭 Additional Enhancements (Future Scope)
* ✍️ Attribution
* 📊 Final Validation Summary
* 🙏 Credits
* 👤 Author

---

## 🌟 Overview

Event Planner is a full-featured Django web application designed to help users manage personal or shared events. It supports user authentication, CRUD operations for events, syncing with Google Calendar, and responsive design down to 270px.

This project is ideal for:

* Individuals managing personal schedules
* Families organizing shared activities
* Couples planning events together
* Groups of friends coordinating outings
* Teenagers planning study or hangout sessions

Hosted live on Heroku and using PostgreSQL in production, the app delivers an end-to-end experience from user interaction to calendar integration.

---

## 💡 Use Cases

* Personal planning
* Couple schedule syncing
* Family accounts: kids & parents share logins
* Friends planning group trips or events
* Students coordinating study sessions
* Group of teenage friends planning weekend activities
* Classroom schedule coordination
* School clubs and after-school activities
* Church groups and volunteer team meetings
* Sports teams managing games and practices

---

### 👤 User Stories

| ID | As a...         | I want to...                            | So that I can...                   |
| -- | --------------- | --------------------------------------- | ---------------------------------- |
| 1  | Visitor         | Register for an account                 | Start using the app                |
| 2  | Registered User | Log in and log out securely             | Access my events safely            |
| 3  | Logged-in User  | Add events with date and description    | Plan my schedule                   |
| 4  | Logged-in User  | Edit or delete my events                | Keep my plans up to date           |
| 5  | Logged-in User  | Manually sync with Google Calendar      | Add events to my external calendar |
| 6  | Mobile User     | Use the app on a phone or tablet        | Access it anywhere                 |
| 7  | Group Member    | Share an account with my family or team | Coordinate shared schedules        |

---

## 🧑‍💻 Features

* Full user authentication
* CRUD for events
* Google Calendar sync
* Mobile-responsive design
* Secure and production-ready deployment
* Custom user background image support

## 🔐 User Authentication

* Register new users
* Secure login/logout
* Session-based authentication
* Logout via POST to prevent CSRF attacks

## 🗓️ Event Management

* Create, read, update, delete events
* Each event tied to the logged-in user (organizer)
* Event list ordered by date/time
* Full CRUD via Django views and templates
* Delete confirmation page to avoid accidental deletions
* Events stored relationally with foreign key to user

### ✨ Custom User Background Image
* Users can upload their own background image.
* Uploaded images are auto-resized to 1920x1080 using PIL.
* Background changes instantly for logged-in users.
* Stored in Google Cloud Storage in `user_backgrounds/user_<id>/`.
* Old background image is deleted when a new one is uploaded.

### ✨ Frontend File Validation
* Upload only allows `.jpg`, `.jpeg`, `.png`, `.webp`.
* Max size: 5MB.
* Live preview shown before upload.

### ✨ Django Feedback Messages
* Success: image uploaded
* Error: invalid file, size exceeded, or no file selected

---

## 🛠️ Technologies Used

**Backend**

* Django 4.x
* Python 3.10+
* PostgreSQL (Heroku)
* SQLite (local/dev)
* Pillow (📸 Auto-processing via Profile.save() in models.py)
* Media file storage using MEDIA_ROOT and MEDIA_URL

**Frontend**

* HTML5 with Django templating
↳ Validated via W3C
* CSS3 (custom, no frameworks)
↳ Flexbox layout, mobile-first, adaptive breakpoints
↳ Sticky footer, focus/hover states, accessible spacing
↳ Favicon and minimalist navbar
* JavaScript
↳ JSHint validated, responsive behavior

**Libraries/APIs**

* Google Calendar API
* google-auth-oauthlib
* google-api-python-client
* Heroku CLI for deployment
* Django Forms for validation
* Django Templates for rendering
* dotenv for secure local dev keys
* Pillow for image resizing
* Google Cloud Storage

### Migration Note

* Originally developed with `db.sqlite3`
* Deleted and added to `.gitignore` post-migration
* Test data was purged before switching to production

### Upgrade Details

* Now using **PostgreSQL** (Neon DB)
* All migrations applied
* Secure connection via `.env` and `dj-database-url`

---

## 🔍 Validation & Testing

* Python formatting via Flake8 & Black (PEP8-compliant)
* Lighthouse score: 100 in all categories
* 📷 Screenshots and validator results in `readme-img/validation-folder`


---

## 🧪 Testing

### ✅ Functional Testing Overview
	
* Feature	Test Case Description	Expected Result	Status
* Register Form	Valid input	Redirect to login	✅
* Register Form	Password mismatch or invalid email	Show error message	✅
* Login Form	Valid credentials	Redirect to events page	✅
* Login Form	Invalid credentials	Show "invalid login" error	✅
* Event Creation Form	All fields valid	Event is created	✅
* Event Creation Form	Missing required field (e.g., title)	Form shows field error	✅
* Event Editing	Access edit page while logged in	Edit form is shown	✅
* Event Editing	Attempt to edit another user's event (not applicable in shared account model)	N/A (shared model)	✅
* Google Calendar Sync	Logged in → trigger sync	Event syncs with Google Calendar	✅
* Google Calendar Sync	Not logged in → trigger sync	Redirect to login page	✅
* Navigation Links	Click "My Events", "Add Event", "Logout" etc.	Each link leads to correct destination	✅
* Unauthorized Access	Visit /events/ or /events/new/ while logged out	Redirect to login	✅
* Upload background image	Valid image upload (logged-in)	Image is saved and visible	✅
* Upload no file	Click submit without choosing file	Show error message or no action	✅
* Upload large file	File > 5MB	Show validation error / prevent upload	✅
* Upload wrong format	.exe or .txt file	Show file format error / prevent upload	✅
* View background on home page	Custom background applied after upload	Uploaded image is shown as background	✅
* Default background fallback	Shown when not logged in or no image exists	Default background is displayed	✅
* Delete old image on new upload	Upload second image and confirm first is deleted	Previous image removed, new one applied	✅

### 🌐 Browser Compatibility Testing

| Browser         | Tested Version | Status |
| --------------- | -------------- | ------ |
| Google Chrome   | 125+           | ✅      |
| Mozilla Firefox | 115+           | ✅      |
| Microsoft Edge  | 125+           | ✅      |
| Safari (iOS)    | iOS 16+        | ✅      |
| Safari (macOS)  | 16+            | ✅      |
| Android Chrome  | 125+           | ✅      |

## ✅ Manual Testing

* Login/logout tested on mobile & desktop
* Event CRUD verified for edge cases (e.g., blank fields)
* Google Calendar sync tested with real accounts
* Deletion sync tested
* Form validation via Django forms
* 404 and 500 error pages handled manually

## 🤖 Automated Testing (future scope)

![alt text](readme-img/automated-test.jpg)

* Coverage planned using Django’s test suite
* Can be extended with Selenium for UI tests
* Tests for Google Calendar mocks
* Form validation (valid file, max size, correct types)
* `upload_background` view test
* Background image saved and resized properly
* Google Cloud Storage handling (mocked)
* Upload page restricted to logged-in users only

---

## 🔍 Lighthouse Audit

* Performance score: 99
* Accessibility: 100
* Best Practices: 100
* SEO: 90

![alt text](readme-img/lighthouse-event-planner.jpg)

## ✅ Validators Used

**All other validations can you find in readme-img/validation-folder. All validations is based on the folder structure**

* HTML validator (no errors)

![alt text](readme-img/html-validator.jpg)

* CSS validated (no errors)

![alt text](readme-img/validation-folder-structure/planner/static/css-validator.jpg)

* JS linted via JSHint (ES6 warnings handled)

![alt text](readme-img/validation-folder-structure/planner/package-lock-validation.jpg)

*Python: PEP8 with Flake8 and Black for formatting

![alt text](readme-img/validation-folder-structure/event-planer/settings-validator.jpg)

---

## 🧭 App Navigation

```
/                      → Redirects to login  
/accounts/login/       → Login  
/register/             → Register  
/events/               → User's events  
/events/new/           → Create event  
/events/<id>/edit/     → Edit event  
/events/<id>/delete/   → Confirm deletion 
/accounts/profile/       → Upload Background 
/events/google-calendar/init/ → Start OAuth  
/oauth2callback/       → OAuth handler
```

---

## 📁 Project Structure

```
event-planner/
├── event_planner/
│   ├── settings.py
│   └── urls.py
├── planner/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── templates/accounts/
├── static/
│   └── css/styles.css
├── requirements.txt
├── Procfile
└── README.md

---


## 📘 Entity Relationship Diagram

### 🧱 Models in This Project

* Below is a list of all models used in the Event Planner project:

### 🔹 User (Django built-in)

* Standard authentication model
* Linked to Event and Profile

### 🔹 Profile

* One-to-one extension of User
* Stores background image uploads
* class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    background_image = models.ImageField(upload_to='user_backgrounds/')

### 🔹 Event

* Main model storing event details
* Linked to a user (organizer)
* Optionally synced with Google Calendar
*class Event(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    google_calendar_event_id = models.CharField(max_length=255, blank=True, null=True)

### 🔹 OAuthState

* Used internally to manage the Google Calendar OAuth2 state
* class OAuthState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

---

### 🔗 Relationships and Cardinality

* Relationship	Type	Description

User → Event	One-to-Many	A user can create many events
User → Profile	One-to-One	Each user has exactly one profile
User → OAuthState	One-to-Many	A user may have multiple OAuth sessions (for safety/logs)
Event → Google Calendar	Optional Link	Stores external calendar event ID (not a DB relation)

---

### 🧮 Cardinality Symbols in ERD

* Symbol	Meaning
0	Zero
0..*	Zero or many
1..*	One or many
`	
---

### 🖼 ERD Diagram Description

*** Your ERD would show: ***
* User entity connected with:
* Event (one-to-many)
* Profile (one-to-one)
* OAuthState (one-to-many)
* Event includes a google_calendar_event_id (a string, not a foreign key)

* User ───────────< Event
  │                └── google_calendar_event_id (optional)
  └─────────────── Profile
  └──────────< OAuthState**

*** A visual version of this Entity Relationship Diagram is available in the readme-img/ folder ***

---

## 🌍 Deployment

**Heroku Setup**

* `heroku create`
* Add-ons: Heroku PostgreSQL
* Set config vars: `DEBUG`, `ALLOWED_HOSTS`, `GOOGLE_CLIENT_ID`, `GOOGLE_SECRET`, `DATABASE_URL`
* `git push heroku main`
* Run migrations and test

**PostgreSQL Setup for Deployment**

1. **Create a PostgreSQL DB** (Neon, Heroku, etc.)
2. **Add your credentials to `.env`**:

```env
DATABASE_URL=postgresql://user:password@host/dbname
```

3. **Install dependencies**:

```bash
pip install dj-database-url psycopg2-binary
```

4. **Update `settings.py`**:

```python
import dj_database_url
DATABASES = {
  'default': dj_database_url.config(default=get_env_variable("DATABASE_URL"), conn_max_age=600)
}
```

5. **Apply Migrations**:

```bash
python manage.py migrate
```

---

## 💾 Saving to Home Screen

## 🧾 iPhone (Safari)

![alt text](readme-img/mobil-eventplaner.jpg)

1. Open the app in Safari (https://event-plan-10650f39d687.herokuapp.com/)
2. Tap the Share icon
3. Tap Add to Home Screen
4. Confirm by tapping Add

## 📱 Android (Chrome)

![alt text](readme-img/mobil-android-eventplaner.jpg)

1. Open the app in Chrome (https://event-plan-10650f39d687.herokuapp.com/)
2. Tap the three-dot menu in the upper-right corner
3. Tap Add to Home screen
4. Confirm by tapping Add again

## 🧾 iPad (Safari)

![alt text](readme-img/ipad-eventplanner.jpg)

1. Open the app in Safari (https://event-plan-10650f39d687.herokuapp.com/)
2. Tap the Share icon (square with an up arrow)
3. Scroll down and tap Add to Home Screen
4. Give it a name (e.g., Event Planner) and tap Add
5. The app will now appear like a native app on your iPad's home screen.

## 📱 Android Tablet (Chrome)

![alt text](readme-img/tablet-eventplaner.jpg)

1. Open the app in Chrome (https://event-plan-10650f39d687.herokuapp.com/)
2. Tap the three-dot menu in the upper-right corner
3. Tap Add to Home screen
4. Confirm by tapping Add again
5. It behaves just like an app with a fullscreen experience and quick access.

## 💻 MacBook (Safari)

![alt text](readme-img/mac-eventplanner.jpg)

1. Open the web app in Safari (https://event-plan-10650f39d687.herokuapp.com/)
2. In the top menu, click File → Add to Dock....
3. Give it a name like Event Planner and confirm.
4. The app icon will appear in the Dock — works like a standalone app!

**Using Chrome**

1. Open the web app in Google Chrome (https://event-plan-10650f39d687.herokuapp.com/)
2. Click the three-dot menu in the top-right corner.
3. Choose More Tools → Create Shortcut....
4. Check “Open as window” to make it feel like an app.
5. Click Create.
6. The shortcut will appear in Launchpad and Applications.

## 💻 Windows Laptop (Chrome or Edge)

![alt text](readme-img/desktop-eventplaner.jpg)

1. Open the site in your browser (https://event-plan-10650f39d687.herokuapp.com/)
2. Click the menu (three dots) at the top right.
3. Select Save and Share → Install app or More Tools → Create Shortcut (in Chrome).
4. Make sure to check “Open as window”.
5. Click Install or Create.
6. It adds an icon to your desktop or Start menu.

No installation needed — it's just a shortcut.


## 🧭 Additional Enhancements (Future Scope)

* Add recurring events
* Admin dashboard
* Notifications/reminders
* Export events as .ics files
* Public/private event sharing
* Invite friends via email
* Event attendance tracking
* Light/dark mode toggle
* Language support (i18n-ready)
* Delete uploaded background image

---

## ✍️ Attribution

* Django docs used for reference: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
* Google Calendar API Docs: [https://developers.google.com/calendar](https://developers.google.com/calendar)
* UI inspiration: Clean CSS patterns, no framework
* All code is original unless otherwise noted

---

## 📊 Final Validation Summary

| Requirement                        | Status       |
| ---------------------------------- | ------------ |
| Relational DB (PostgreSQL)         | ✅ Fulfilled |
| CRUD Functionality                 | ✅ Fulfilled |
| User Authentication                | ✅ Fulfilled |
| Navigation & Layout                | ✅ Fulfilled |
| Custom HTML/CSS                    | ✅ Fulfilled |
| README and Documentation           | ✅ Full      |
| Git & GitHub Used                  | ✅ Full      |
| Attribution Marked                 | ✅ Done      |
| Responsive down to 270px           | ✅ Done      |
| Sync + Deletion w/ Google Calendar | ✅ Working   |
| Validation & Linting               | ✅ Passed    |
| Image Upload, Resize, Validation	 | ✅ Working   |

> 🔒 Built with security in mind
> 💡 Designed for real-world usability
> 🧩 Easily expandable with more features
> 📱 Works beautifully across all screen sizes
> 🚀 Production-ready and developer-friendly

---

## 🙏 Credits

### 🧠 Concept & Development

*** Mr. Husse ***
* Planned, designed, and developed the entire Event Planner application — including user auth, event CRUD, background image uploads, and Google Calendar sync.

### 🎨 UI & Visual Design
* Custom UI and CSS layout created from scratch using Flexbox and mobile-first design.
* Background image functionality styled and previewed with responsive considerations.
* All visual styling, layout polish, and responsiveness by Mr. Husse.

### 🧪 Testing & Feedback
* Friends, family, and the Code Institute community
* Provided extensive feedback, tested features across devices, and helped improve form validation and UI consistency.

### 🌍 Community Contributions
* Open-source resources, articles, and forums
* Helped guide OAuth2 integration, Django deployment practices, and mobile UX improvements.

### 🙌 General Support
* Big thank you to Code Institute, my peers on Slack, and everyone who helped review, test, and support this project.
* Special thanks to my mentor Brian Macharia for code reviews, suggestions, and guidance throughout development.
* Also thanks to Kasia Bogucka for leading workshops and providing clear and encouraging support during stand-ups.
* Big thank you to my old teacher Khrystina for her early support and encouragement, and to my new teacher Kay at Code Institute for her patience, feedback, and belief in my ideas.
* Also, thanks to W3Schools for their always-reliable coding references.

---

👤 Author
Developed by Hussein Elali
GitHub: @god-zil-la

✔️ Final deployment working: [https://event-plan.herokuapp.com](https://event-plan-10650f39d687.herokuapp.com/register/)

# Commit 12 placeholder

# Commit 13 placeholder

# Commit 14 placeholder

# Commit 15 placeholder

# Commit 16 placeholder

# Commit 17 placeholder

# Commit 18 placeholder

# Commit 19 placeholder

# Commit 20 placeholder

# Commit 21 placeholder

# Commit 22 placeholder

# Commit 23 placeholder

# Commit 24 placeholder

# Commit 25 placeholder

# Commit 26 placeholder

# Commit 27 placeholder

# Commit 28 placeholder

# Commit 29 placeholder

# Commit 30 placeholder

# Commit 31 placeholder

# Commit 32 placeholder

# Commit 33 placeholder

# Commit 34 placeholder

# Commit 35 placeholder

# Commit 36 placeholder

# Commit 37 placeholder

# Commit 38 placeholder

# Commit 39 placeholder

# Commit 40 placeholder

# Commit 41 placeholder

# Commit 42 placeholder

# Commit 43 placeholder

# Commit 44 placeholder

# Commit 45 placeholder

# Commit 46 placeholder

# Commit 47 placeholder

# Commit 48 placeholder

# Commit 49 placeholder

# Commit 50 placeholder

# Commit 51 placeholder

# Commit 52 placeholder

# Commit 53 placeholder

# Commit 54 placeholder

# Commit 55 placeholder

# Commit 56 placeholder

# Commit 57 placeholder

# Commit 58 placeholder

# Commit 59 placeholder

# Commit 60 placeholder

# Commit 61 placeholder

# Commit 62 placeholder

# Commit 63 placeholder

# Commit 64 placeholder

# Commit 65 placeholder

# Commit 66 placeholder

# Commit 67 placeholder

# Commit 68 placeholder

# Commit 69 placeholder

# Commit 70 placeholder

# Commit 71 placeholder

# Commit 72 placeholder

# Commit 73 placeholder

# Commit 74 placeholder

# Commit 75 placeholder

# Commit 76 placeholder

# Commit 77 placeholder

# Commit 78 placeholder

# Commit 79 placeholder

# Commit 80 placeholder

# Commit 81 placeholder

# Commit 82 placeholder
