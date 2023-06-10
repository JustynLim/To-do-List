from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import Label, Toplevel
from PIL import Image, ImageTk
from plyer import notification
from tkcalendar import Calendar
import datetime
import os
import sqlite3

# Database
Connect = sqlite3.connect("account.db")
cursor = Connect.cursor()

######################################################################################################################################
###--- Window ---###
# Tkinter window
root = Tk()

# Window title
root.title("To-Do List")

# Window size
root.geometry("925x500")
root.resizable(False, False)

# Background
root.configure(bg = "white")

task_list =[]

######################################################################################################################################
###--- Background design ---###
# App Icon
Image_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Icon1.png") #Path to image

Image_icon = PhotoImage(file = Image_path1)
root.iconphoto(False, Image_icon)

# Topbar
Image_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "amethyst.jpg")
image1 = Image.open(Image_path2)    # Resize the image

background_width = 1600   # Set size of the image
background_height = 71

resized_image = image1.resize((background_width, background_height), Image.LANCZOS)

New_topbar = ImageTk.PhotoImage(resized_image)
label_1 = Label(root, image = New_topbar)
label_1.pack()

# Sidebar
newside_width = 100   # Set size of the image
newside_height = 500

resized_Side = image1.resize((newside_width, newside_height), Image.LANCZOS)

New_Sidebar = ImageTk.PhotoImage(resized_Side)
label_2 = Label(root, image = New_Sidebar, bg = "white")
label_2.place(x = 850, y = 72)

# Top heading
Heading = Label(root, text="TASK",  font = "arial 20 bold", fg = "white", bg = "#9960D1")
Heading.place(x = 400, y = 20)

# darkmode image path
Image_path3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topback.png")
image2 = Image.open(Image_path3)

resized_topbar = image2.resize((background_width, background_height), Image.LANCZOS)

dark_topbar = ImageTk.PhotoImage(resized_topbar)

resized_dsidebar = image2.resize((newside_width, newside_height), Image.LANCZOS)

dark_sidebar = ImageTk.PhotoImage(resized_dsidebar)

######################################################################################################################################
###--- Function ---###
# Input error
def error_intput() :
    if task_entry.get() == "" :
        messagebox.showerror("Input Error")
        return 0
    return 1

# Clear task
def clear_taskField() :
    task_entry.delete(0, END)

# Insert task
def add_task():
    value = error_intput()
    if value == 0:
        return

    content = task_entry.get()

    deadline = simpledialog.askstring("Set Deadline", "Enter the deadline (YYYY-MM-DD):")
    if deadline:
        current_date = datetime.datetime.now().date()
        deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()

        if deadline_date >= current_date:
            cursor.execute("""INSERT INTO TASK (USERNAME, TASK_NAME, TASK_DUEDATE, COMPLETED) 
            VALUES (?, ?, ?, 0)""", 
            ("user123", content, deadline))
            Connect.commit()

            task_list.append((content, deadline))
            listbox.insert(END, f"{content} (Deadline: {deadline}, Days Left: {get_days_left(deadline)})")
        else:
            messagebox.showerror("Invalid Deadline", "The deadline cannot be in the past.")

    clear_taskField()

def get_days_left(deadline):
    deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
    current_date = datetime.datetime.now().date()
    days_left = (deadline_date - current_date).days
    return days_left

# Load task
def load_tasks():
    cursor.execute("SELECT TASK_NAME, TASK_DUEDATE FROM TASK WHERE COMPLETED = 0")
    tasks = cursor.fetchall()
    current_date = datetime.datetime.now().date()

    for task in tasks:
        content, deadline = task
        deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
        days_left = (deadline_date - current_date).days

        if days_left < 0:
            notification_title = "Task Reminder"
            notification_message = f"The task '{content}' is overdue!"
            notification.notify(title=notification_title, message=notification_message, timeout= 5)
        elif days_left == 0:
            notification_title = "Task Reminder"
            notification_message = f"The task '{content}' is due today!"
            notification.notify(title=notification_title, message=notification_message, timeout= 5)
        elif days_left == 1:
            notification_title = "Task Reminder"
            notification_message = f"The task '{content}' is due tomorrow!"
            notification.notify(title=notification_title, message=notification_message, timeout= 5)  
        elif days_left > 1 and days_left < 7:
            notification_title = "Task Reminder"
            notification_message = f"The task '{content}' is due in {days_left} days!"
            notification.notify(title=notification_title, message=notification_message, timeout= 5)
        elif days_left == 7:
            notification_title = "Task Reminder"
            notification_message = f"The task '{content}' is due in a week!"
            notification.notify(title=notification_title, message=notification_message, timeout= 5)

        task_list.append((content, deadline))
        listbox.insert(END, f"{content} (Deadline: {deadline}, Days Left: {days_left})")

# Delete task
def delete_task():
    selected_task = listbox.curselection()
    if selected_task:
        index = int(selected_task[0])
        selected_item = listbox.get(index)
        task_name = selected_item.split(' (Deadline:')[0]  # Extract task name from selected item

        try:
            cursor.execute("DELETE FROM TASK WHERE TASK_NAME = ?", (task_name,))
            Connect.commit()
            task_list.pop(index)
            listbox.delete(index)
        except sqlite3.Error as error:
            print("Error deleting task:", error)

# Edit task
def edit_task():
    selected_index = listbox.curselection()
    if selected_index:
        index = int(selected_index[0])
        old_task, old_deadline = task_list[index]
        new_task = simpledialog.askstring("Edit Task", "Modify the task:", initialvalue=old_task)
        if new_task:
            new_deadline = simpledialog.askstring("Edit Task", "Modify the deadline (YYYY-MM-DD):", initialvalue=old_deadline)
            if new_deadline:
                current_date = datetime.datetime.now().date()
                deadline_date = datetime.datetime.strptime(new_deadline, "%Y-%m-%d").date()

                if deadline_date >= current_date:
                    task_list[index] = (new_task, new_deadline)
                    listbox.delete(index)
                    listbox.insert(index, f"{new_task} (Deadline: {new_deadline}, Days Left: {get_days_left(new_deadline)})")
                else:
                    messagebox.showerror("Invalid Deadline", "The deadline cannot be in the past.")

# Complete task
def complete_task():
    selected_index = listbox.curselection()
    if selected_index:
        index = int(selected_index[0])
        selected_item = listbox.get(index)
        task_name = selected_item.split(' (Deadline:')[0]  # Extract task name from selected item

        try:
            cursor.execute("UPDATE TASK SET COMPLETED = 1 WHERE TASK_NAME = ?", (task_name,))
            Connect.commit()
            task_list.pop(index)
            listbox.delete(index)

            notification_title = "Task Completed"
            notification_message = f"The task '{task_name}' has been completed!"
            notification.notify(title = notification_title, message = notification_message, timeout= 5,)  
        except sqlite3.Error as error:
            print("Error completing task:", error)

# Display calendar
def display_calendar():
    calendar_window = Toplevel(root)
    calendar_window.title("Calendar")
    calendar_window.geometry("400x400")
    calendar_window.configure(bg = "black")
    
    calendar = Calendar(calendar_window, selectmode="day", background="white", foreground="black", selectbackground="blue", font="arial 16")
    calendar.pack(pady=10)
    
    tasks = []
    for task in task_list:
        task_name = task[0]
        deadline = task[1]
        task_info = f"Task: {task_name}\nDeadline: {deadline}"
        tasks.append(task_info)
    
    tags = ["task{}".format(i) for i in range(len(tasks))]
    for tag in tags:
        calendar.tag_config(tag, background="#2E1A47")
    
    for i, task in enumerate(tasks):
        date = datetime.datetime.strptime(task_list[i][1], "%Y-%m-%d").date()
        calendar.calevent_create(date, "Task", tags=tags[i])
    
    def show_task_details(event):
        selected_date = calendar.selection_get()
        task_details_label.config(text="")
        tasks_on_selected_date = []

        for i, task in enumerate(task_list):
            task_date = datetime.datetime.strptime(task[1], "%Y-%m-%d").date()
            if selected_date == task_date:
                tasks_on_selected_date.append(tasks[i])

        if tasks_on_selected_date:
            task_details = "\n\n".join(tasks_on_selected_date)
            task_details_label.config(text=task_details)
    
    task_details_label = Label(calendar_window, text="", font="arial 12", bg="black", fg="white")
    task_details_label.pack(pady=10)
    
    calendar.bind("<<CalendarSelected>>", show_task_details)

# Change Theme
def system_theme():
    global button_mode

    if button_mode:
        #messagebox.showerror('Dark',"Dark Mode")
        toggle_mode.config(image = darkmode_button ,bg = '#26242f',activebackground = "#26242f")
        root.config(bg = "#26242f")
        Usr_frame.config(bg = "white")
        label_1.config(image = dark_topbar)
        label_2.config(image= dark_sidebar)
        Heading.config(bg = "#2E1A47")
        frame1.config(bg = "#2E1A47")
        listbox.config(bg = "#2E1A47")
        delete_button.config(bg = "#2E1A47")
        edit_button.config(bg = "#2E1A47")
        complete_button.config(bg = "#2E1A47")
        calendar_button.config(bg = "#2E1A47")
        toggle_mode.config(bg = "#2E1A47")

        button_mode = False

    else:
        #messagebox.showerror('Light',"Light Mode")
        toggle_mode.config(image = lightmode_button, bg = "white", activebackground = "white")
        root.config(bg = "white")
        Usr_frame.config(bg ="#9960D1")
        label_1.config(image = New_topbar)
        label_2.config(image= New_Sidebar)
        Heading.config(bg = "#9960D1")
        frame1.config(bg = "#9960D1")
        listbox.config(bg = "#9960D1")
        delete_button.config(bg = "#9960D1")
        edit_button.config(bg = "#9960D1")
        complete_button.config(bg = "#9960D1")
        calendar_button.config(bg = "#9960D1")
        toggle_mode.config(bg = "#9960D1")

        button_mode = True

######################################################################################################################################
###--- Main UI ---###
# Frame of user input box
Usr_frame = Frame(root, width = 410, height = 50, bg = "#9960D1")
Usr_frame.place(x = 260, y = 105)

# User input box
task = StringVar()
task_entry = Entry(Usr_frame, width = 20, font = "arial 20", bd = 0, bg= "white", fg = "black")
task_entry.place(x = 10, y = 7)
task_entry.focus()

# Task list frame
frame1 = Frame(root, bd = 3, width = 700, height = 280, bg ="#9960D1" )
frame1.pack(pady = (100,0))

# Task List box
listbox = Listbox(frame1, font = "arial 12 bold", width = 40, height = 16, bg = "#9960D1", fg = "white", cursor = "hand2" , selectbackground = "black")
listbox.pack(side = LEFT, fill = BOTH, padx= 2)

# Scroll bar
scrollbar = Scrollbar(frame1)
scrollbar.pack(side = RIGHT , fill = BOTH)

listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listbox.yview)

######################################################################################################################################
###--- Button ---###
# Add task button
Add_button = Button(Usr_frame, text = "ADD", font = "arial 20 bold", width = 5, bg = "#8D50C7", fg = "white", bd=0, command = add_task)
Add_button.place(x = 320, y = 0)

# Delete task buttton
Image_path4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "delete.png")
image3 = Image.open(Image_path4)

del_width = 50
del_height = 50

resized_del =image3.resize((del_width,del_height),Image.LANCZOS)

New_del = ImageTk.PhotoImage(resized_del)
delete_button = Button(root, image = New_del , bg = "#9960D1", bd = 0, command = delete_task)
delete_button.place(x = 865, y = 180)

# Edit task button
Image_path5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "edit.png")
image4 = Image.open(Image_path5)

edit_width = 50
edit_height = 50

resized_edit = image4.resize((edit_width, edit_height), Image.LANCZOS)

New_edit = ImageTk.PhotoImage(resized_edit)
edit_button = Button(root, image=New_edit, bg="#9960D1", bd = 0, command = edit_task)
edit_button.place(x = 865, y = 280)

# Complete task button
Image_path6 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "complete.png")
image5 = Image.open(Image_path6)

complete_width = 50
complete_height = 50

resized_complete = image5.resize((complete_width, complete_height), Image.LANCZOS)

New_complete = ImageTk.PhotoImage(resized_complete)
complete_button = Button(root, image=New_complete, bg="#9960D1", bd=0, command=complete_task)
complete_button.place(x=865, y=380)

# Calendar button
Image_path7 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar.png")
image6 = Image.open(Image_path7)

calendar_width = 50
calendar_height = 50

resized_calendar = image6.resize((calendar_width, calendar_height), Image.LANCZOS)

New_calendar = ImageTk.PhotoImage(resized_calendar)
calendar_button = Button(root, image=New_calendar, bg="#9960D1", bd=0, command= display_calendar)
calendar_button.place(x=15,y=15)

# Theme change buton
Image_path8 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "light_mode.png")
image7 = Image.open(Image_path8)

Image_path9 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dark_mode.png")
image8 = Image.open(Image_path9)

lightmode_button = ImageTk.PhotoImage(image7)
darkmode_button = ImageTk.PhotoImage(image8)

button_mode = True

toggle_mode = Button(root, width=173,height = 69, pady=7, image = lightmode_button, bd=0, bg = "#9960D1", command = system_theme)
toggle_mode.place(x = 750, y = 2)

######################################################################################################################################
###---Load task---###
# Call load task function
load_tasks()

root.mainloop()