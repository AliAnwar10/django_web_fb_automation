# 📢 Facebook Group Automation Web App

> A full-featured Django-based automation tool to schedule and publish posts (with images) to multiple Facebook groups using **Playwright**, with a sleek Bootstrap UI for managing credentials, group links, and post templates.

---

## 🚀 Features

- ✅ **Add & Manage Facebook Credentials** (email & password)
- ✅ **Create Facebook Group Entries** with name + URL
- ✅ **Design Custom Post Templates** with title, description, hashtags, and image
- ✅ **Visual Dashboard** with tabs, modals, and responsive layout
- ✅ **Post Selection Logic** to map posts to groups per credential
- ✅ **Full Automation Runner** via Playwright (headless or visible browser)
- ✅ **Async/Await-based Playwright Automation** using Chromium
- ✅ **AJAX Form Submission** with success/error feedback
- ✅ **Image Upload Support** with `media/posts/` storage
- ✅ **Responsive UI with Bootstrap 5** + jQuery interactivity

---

## 🖥️ Tech Stack

| Layer           | Tech                                      |
|----------------|-------------------------------------------|
| **Backend**     | Python 3.x, Django 4.x                    |
| **Automation**  | Playwright (Async Mode)                   |
| **Frontend**    | HTML, CSS, Bootstrap 5, JavaScript, jQuery |
| **Database**    | SQLite3                                   |
| **Storage**     | Django Media for Image Uploads           |

---

## 📂 Project Structure

fb_automation_web/
├── autoapp/ # Main Django app
│ ├── models.py # Models: Credential, GroupLink, Post, PostSelection
│ ├── views.py # Handles add/delete/view actions and AJAX
│ ├── forms.py # Django Forms
│ ├── automation_runner.py # Async Playwright automation script
│ └── templates/autoapp/ # HTML Templates
│
├── media/ # Uploaded post images
├── static/ # Bootstrap and custom JS/CSS
├── fb_automation_web/ # Project settings and URLs
├── manage.py
├── requirements.txt
└── .gitignore



## ⚙️ Setup & Installation

### 1. Clone the Repository

git clone https://github.com/your-username/fb_automation_web.git
cd fb_automation_web
### 2. Create Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt

### 3. Run Migrations & Start Server

python manage.py migrate
python manage.py runserver
Visit: http://127.0.0.1:8000/

### 🛠️ Usage Workflow
Add Facebook Credential via modal

Add Facebook Group (name + URL)

Create Post Template (title, description, hashtags, image)

Select Group + Post Mappings from load tab

Run Automation (select credential and run)

### 🤖 Automation Logic
Uses Playwright (async) to launch Chromium browser

Loads credentials from DB and logs into Facebook

For each selected post-group pair:

Navigates to group

Clicks "Write something"

Fills in title + description + hashtags

Attaches uploaded image (if available)

Clicks "Post"

Logs all events and errors live to browser via AJAX

### 📦 Dependencies
Install dependencies with:
playwright install

### 🧩 Troubleshooting

| Issue                         | Solution                              |
| ----------------------------- | ------------------------------------- |
| Facebook CAPTCHA / Login Fail | Use real browser session or slow down |
| Image not uploading           | Check image path & selector logic     |
| Timeout Errors                | Increase Playwright timeout values    |



### 📸 Screenshots




### 💬 Author
Ali Anwar
Software Engineer| Python Developer| Django


