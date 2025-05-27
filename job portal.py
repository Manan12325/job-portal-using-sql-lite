import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import datetime
import ttkbootstrap as ttk  # For modern UI themes

# Global variable for current user
current_user_id = None

# Setup database
def setup_database():
    conn = sqlite3.connect("job_tracker.db")
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    
    # Jobs table linked to users
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        company TEXT,
                        job_title TEXT,
                        application_date TEXT,
                        status TEXT,
                        description TEXT,
                        reminder_date TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

# Login window
def login_window():
    login = tk.Toplevel(root)
    login.title("Login")
    login.geometry("300x300")

    tk.Label(login, text="Username").pack(pady=10)
    username = tk.Entry(login)
    username.pack(pady=5)

    tk.Label(login, text="Password").pack(pady=10)
    password = tk.Entry(login, show="*")
    password.pack(pady=5)

    def login_user():
        user = username.get()
        pwd = password.get()
        conn = sqlite3.connect("job_tracker.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            global current_user_id
            current_user_id = user_data[0]
            login.destroy()
            load_jobs()
            messagebox.showinfo("Welcome", f"Logged in as {user}")
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(login, text="Login", command=login_user).pack(pady=20)
    tk.Button(login, text="Sign Up", command=signup_window).pack()

# Signup window
def signup_window():
    signup = tk.Toplevel(root)
    signup.title("Sign Up")
    signup.geometry("300x300")

    tk.Label(signup, text="Username").pack(pady=10)
    username = tk.Entry(signup)
    username.pack(pady=5)

    tk.Label(signup, text="Password").pack(pady=10)
    password = tk.Entry(signup, show="*")
    password.pack(pady=5)

    def register_user():
        user = username.get()
        pwd = password.get()
        conn = sqlite3.connect("job_tracker.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            signup.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        finally:
            conn.close()

    tk.Button(signup, text="Register", command=register_user).pack(pady=20)

# Load jobs for the current user
def load_jobs():
    for row in job_table.get_children():
        job_table.delete(row)
    
    conn = sqlite3.connect("job_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, company, job_title, application_date, status FROM jobs WHERE user_id=?", (current_user_id,))
    jobs = cursor.fetchall()
    conn.close()

    for job in jobs:
        job_table.insert("", "end", values=job)

# Add a new job
def add_job():
    def save_job():
        company = company_entry.get()
        job_title = title_entry.get()
        application_date = date_entry.get()
        status = status_combo.get()
        description = description_text.get("1.0", tk.END).strip()
        reminder_date = reminder_entry.get()

        conn = sqlite3.connect("job_tracker.db")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO jobs (user_id, company, job_title, application_date, status, description, reminder_date)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                       (current_user_id, company, job_title, application_date, status, description, reminder_date))
        conn.commit()
        conn.close()

        add_window.destroy()
        load_jobs()
        messagebox.showinfo("Success", "Job added successfully!")

    add_window = tk.Toplevel(root)
    add_window.title("Add Job")
    add_window.geometry("400x400")

    tk.Label(add_window, text="Company:").pack(pady=5)
    company_entry = tk.Entry(add_window)
    company_entry.pack()

    tk.Label(add_window, text="Job Title:").pack(pady=5)
    title_entry = tk.Entry(add_window)
    title_entry.pack()

    tk.Label(add_window, text="Application Date:").pack(pady=5)
    date_entry = tk.Entry(add_window)
    date_entry.pack()

    tk.Label(add_window, text="Status:").pack(pady=5)
    status_combo = ttk.Combobox(add_window, values=["Applied", "Interview", "Offered", "Rejected", "On Hold"])
    status_combo.pack()

    tk.Label(add_window, text="Description:").pack(pady=5)
    description_text = tk.Text(add_window, height=5, width=30)
    description_text.pack()

    tk.Label(add_window, text="Reminder Date (YYYY-MM-DD):").pack(pady=5)
    reminder_entry = tk.Entry(add_window)
    reminder_entry.pack()

    tk.Button(add_window, text="Save Job", command=save_job).pack(pady=20)

# Show job analytics
def show_analytics():
    conn = sqlite3.connect("job_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM jobs WHERE user_id=? GROUP BY status", (current_user_id,))
    data = cursor.fetchall()
    conn.close()

    statuses = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure(figsize=(8, 6))
    plt.bar(statuses, counts, color=["blue", "green", "orange", "red"])
    plt.xlabel("Status")
    plt.ylabel("Number of Applications")
    plt.title("Job Application Status Breakdown")
    plt.show()

# Check reminders
def check_reminders():
    today = datetime.date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect("job_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT company, job_title, reminder_date FROM jobs WHERE user_id=? AND reminder_date=?", 
                   (current_user_id, today))
    reminders = cursor.fetchall()
    conn.close()

    if reminders:
        reminder_msg = "\n".join([f"{r[0]} - {r[1]} (Reminder Date: {r[2]})" for r in reminders])
        messagebox.showinfo("Reminders", f"You have the following reminders today:\n\n{reminder_msg}")
    else:
        messagebox.showinfo("Reminders", "No reminders for today.")

# Main window
root = ttk.Window(themename="solar")
root.title("Job Application Tracker")
root.geometry("800x600")

# Toolbar
toolbar = tk.Frame(root)
toolbar.pack(side="top", fill="x")

tk.Button(toolbar, text="Add Job", command=add_job).pack(side="left", padx=5, pady=5)
tk.Button(toolbar, text="Analytics", command=show_analytics).pack(side="left", padx=5, pady=5)
tk.Button(toolbar, text="Check Reminders", command=check_reminders).pack(side="left", padx=5, pady=5)

# Job Table
columns = ("ID", "Company", "Job Title", "Application Date", "Status")
job_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    job_table.heading(col, text=col)
    job_table.column(col, width=100)

job_table.pack(fill="both", expand=True)

# Start login window
login_window()

# Run setup and main loop
setup_database()
root.mainloop()
