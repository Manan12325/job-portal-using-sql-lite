# 💼 Job Application Tracker

A desktop application built with **Python** and **Tkinter (ttkbootstrap)** that helps users track, manage, and analyze their job applications with ease. Featuring user authentication, reminder notifications, visual analytics, and a clean interface, this tool is ideal for job seekers looking to stay organized.


## 🔍 Features

* 🔐 **User Authentication** (Sign Up & Login)
* 📋 **Track Job Applications** with details like company, role, date, and status
* ⏰ **Reminder System** for follow-ups
* 📊 **Visual Analytics** of application status using bar charts
* 🎨 **Modern GUI** using `ttkbootstrap` themes
* 🗃️ **Persistent Data Storage** via SQLite

## 🛠️ Getting Started

### Prerequisites

* Python 3.x
* Required libraries:
  pip install matplotlib ttkbootstrap


### How to Run

1. Clone the repository:

   git clone https://github.com/yourusername/job-application-tracker.git
   cd job-application-tracker


2. Run the application:
   python job\ portal.py

Features Explained

| Module           | Description                                                                  |
| ---------------- | ---------------------------------------------------------------------------- |
| **Login/Signup** | Secure login system with SQLite-backed user management                       |
| **Job Entries**  | Add company name, title, application date, status, description, and reminder |
| **Analytics**    | Visual breakdown of application statuses                                     |
| **Reminders**    | Alert users of follow-up dates for applications                              |
| **Database**     | Automatically creates and manages user/job tables                            |


File Structure
job-application-tracker/
├── job portal.py        # Main application file
└── README.md            # Project documentation

Example Statuses

* Applied
* Interview
* Offered
* Rejected
* On Hold

Author
Manan Chawla
