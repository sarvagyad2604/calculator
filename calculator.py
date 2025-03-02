import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import sqlite3

def setup_database():
    conn = sqlite3.connect("calendar_events.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            event TEXT
        )
    """)
    conn.commit()
    conn.close()

def show_selected_date():
    selected_date = cal.get_date()
    conn = sqlite3.connect("calendar_events.db")
    cursor = conn.cursor()
    cursor.execute("SELECT event FROM events WHERE date = ?", (selected_date,))
    events = cursor.fetchall()
    conn.close()
    event_list = "\n".join([event[0] for event in events]) or "No events found."
    messagebox.showinfo("Events on " + selected_date, event_list)

def go_to_date():
    try:
        year = int(year_entry.get())
        month = int(month_entry.get())
        day = int(day_entry.get())
        cal.selection_set(f"{month}/{day}/{year}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid date (YYYY-MM-DD)")

def add_event():
    selected_date = cal.get_date()
    event_text = event_entry.get()
    if event_text.strip():
        conn = sqlite3.connect("calendar_events.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (date, event) VALUES (?, ?)", (selected_date, event_text))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Event added successfully!")
    else:
        messagebox.showerror("Error", "Please enter an event description.")

# Setup Database
setup_database()

# Create main application window
root = tk.Tk()
root.title("Calendar App")

# Create Calendar widget
cal = Calendar(root, selectmode='day', year=2025, month=2, day=20)
cal.pack(pady=20)

# Button to show selected date
display_button = tk.Button(root, text="Show Events", command=show_selected_date)
display_button.pack()

# Go to Date Feature
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Year:").grid(row=0, column=0)
year_entry = tk.Entry(frame)
year_entry.grid(row=0, column=1)

tk.Label(frame, text="Month:").grid(row=0, column=2)
month_entry = tk.Entry(frame)
month_entry.grid(row=0, column=3)

tk.Label(frame, text="Day:").grid(row=0, column=4)
day_entry = tk.Entry(frame)
day_entry.grid(row=0, column=5)

go_button = tk.Button(root, text="Go to Date", command=go_to_date)
go_button.pack()

# Add Event Feature
event_frame = tk.Frame(root)
event_frame.pack(pady=10)

tk.Label(event_frame, text="Event:").grid(row=0, column=0)
event_entry = tk.Entry(event_frame, width=30)
event_entry.grid(row=0, column=1)

add_event_button = tk.Button(root, text="Add Event", command=add_event)
add_event_button.pack()

# Run the Tkinter event loop
root.mainloop()
