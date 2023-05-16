from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import os

#Tkinter window
root = Tk()

#Giving the window a title
root.title("To-Do List")

#Window size
root.geometry("400x650")
root.resizable(False, False)

#Background
root.configure(bg = "black")

task_list =[]

#App Icon
Image_path1 = os.path.dirname(os.path.abspath(__file__))
Icon_path1 = os.path.join(Image_path1, "Icon1.png")

Image_icon = PhotoImage(file = Icon_path1)
root.iconphoto(False, Image_icon)

#Topbar
#Top backgrond design
Image_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topback.png")

#Resize the image
image1 = Image.open(Image_path2)

#Set size of the image
background_width = 1600
background_height = 70

resized_image = image1.resize((background_width, background_height), Image.LANCZOS)

New_topbar = ImageTk.PhotoImage(resized_image)

label_1 = Label(root, image = New_topbar)
label_1.pack()

#Menu bar icon
Image_path3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dock.png")
Topbar_Icon = PhotoImage(file = Image_path3)
Label(root, image = Topbar_Icon, bg ="#2E1A47").place(x=15,y=25)

#To-do list icon
Image_path4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "to-do-list.png")
image2 = Image.open(Image_path4)

Tdl_width = 20
Tdl_height = 20

resized_Tdl =image2.resize((Tdl_width,Tdl_height),Image.LANCZOS)

New_Tdl = ImageTk.PhotoImage(resized_Tdl)

label_2 = Label(root, image = New_Tdl, bg = "#2E1A47")
label_2.place(x = 360, y = 25)

#Top heading
Heading = Label(root, text="TASK",  font = "arial 20 bold", fg = "white", bg = "#2E1A47")
Heading.place(x = 165, y = 20)

#Function
#When input error

def Error_intput() :
    if task_entry.get() == "" :
        messagebox.showerror("Input Error")
        return 0
    return 1

def clear_taskField() :

    task_entry.delete(0, END)


def insertTask():
    value = Error_intput()
    if value == 0 :
        return

    content = task_entry.get() + "\n"

    task_list.append(content)

    listbox.insert(END,content)

    clear_taskField()

def delete_task():
    selected_task = listbox.curselection()
    if selected_task:
        index = int(selected_task[0])
        task_list.pop(index)
        listbox.delete(index)

def edit_task():
    selected_index = listbox.curselection()
    if selected_index:
        index = int(selected_index[0])
        old_task = listbox.get(index)
        new_task = simpledialog.askstring("Edit Task", "Modify the task:", initialvalue=old_task)
        if new_task:
            task_list[index] = new_task
            listbox.delete(index)
            listbox.insert(index, new_task)

#Main
Usr_frame = Frame(root, width = 400, height = 50, bg = "white")
Usr_frame.place(x = 0, y = 180)

task = StringVar()
task_entry = Entry(Usr_frame, width = 18, font = "arial 20", bd = 0)
task_entry.place(x = 10, y = 7)
task_entry.focus()

Add_button = Button(Usr_frame, text = "ADD", font = "arial 20 bold", width = 5, bg = "#8D50C7", fg = "white", bd=0, command = insertTask)
Add_button.place(x = 310, y = 0)

#Listbox
frame1 = Frame(root, bd = 3, width = 700, height = 280, bg ="#2E1A47" )
frame1.pack(pady = (160,0))

listbox = Listbox(frame1, font = ("arial", 12), width = 40, height = 16, bg = "#2E1A47", fg = "white", cursor = "hand2" , selectbackground = "black")
listbox.pack(side = LEFT, fill = BOTH, padx= 2)

scrollbar = Scrollbar(frame1)
scrollbar.pack(side = RIGHT , fill = BOTH)

listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listbox.yview)

#Delete buttton
Image_path5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "delete.png")
image3 = Image.open(Image_path5)

del_width = 50
del_height = 50

resized_del =image3.resize((del_width,del_height),Image.LANCZOS)

New_del = ImageTk.PhotoImage(resized_del)
Button(root, image = New_del , bg = "black", bd = 0, command = delete_task).place(x = 250, y = 575)

#Edit button
Image_path6 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "edit.png")
image4 = Image.open(Image_path6)

edit_width = 50
edit_height = 50

resized_edit = image4.resize((edit_width, edit_height), Image.LANCZOS)

New_edit = ImageTk.PhotoImage(resized_edit)
Button(root, image=New_edit, bg="black", bd = 0, command = edit_task).place(x = 100, y = 575)

root.mainloop()