from tkinter import *
from PIL import ImageTk
from tkinter import messagebox, ttk

root  = Tk()
root.geometry("1000x600")
root['bg'] = "#2e0947"
root.title("Student Manager")

root.iconphoto(False, ImageTk.PhotoImage(file="Exercise 3 - Student Manager/document.png"))

filename = "Exercise 3 - Student Manager/studentMarks.txt"
students = []

#loading student info
def studentIndex():
    global students
    students = [] 
    with open(filename, "r") as file:
        lines = file.readlines()
        numStudents = int(lines[0].strip()) #first line is number of students
        
        for i in range(1, numStudents + 1):
            data = lines[i].strip().split(",")
            student = {'ID': data[0], 'name': data[1], 'grade1': int(data[2]),
                        'grade2': int(data[3]), 'grade3': int(data[4]), 'exam': int(data[5])}
            students.append(student)

#calculates stats for a student
def Grader(student):
    totalgrade = (student['grade1'] + student['grade2'] + student['grade3'])
    totalMarks = totalgrade + student['exam']
    percent = (totalMarks / 160) * 100

    if percent >= 90:
        grade = 'A'
    elif percent >= 70:
        grade = 'B'
    elif percent >= 50:
        grade = 'C'
    elif percent >= 40:
        grade = 'D'
    else:
        grade = 'F'
    
    return {
        'totalgrade': totalgrade,
        'totalMarks': totalMarks,
        'percent': percent,
        'grade': grade
    }

def clearOutput():
    for item in tree.get_children():
        tree.delete(item)

def display(student):
    stats = Grader(student)
    tree.insert("", END, values=(student['ID'], student['name'], student['grade1'], student['grade2'], student['grade3'],
                                student['exam'], stats['totalgrade'], stats['totalMarks'],
                                f"{stats['percent']}%", stats['grade']))

#shows all students
def viewAll():
    clearOutput()
    for student in students:
        display(student)

#view one student
def viewSingle():
    openWin = Toplevel(root)
    openWin.title("Select Student")
    openWin.geometry("400x400")
    openWin['bg'] = "#0c005b"
    
    Label(openWin, text="Select a Student", font=("Arial", 16, "bold"), bg="#0c005b", fg="#ffffff").pack(pady=20)
    
    listFrame = Frame(openWin, bg="#ffffff")
    listFrame.pack(pady=10, padx=20, fill=BOTH, expand=True)
    listbox = Listbox(listFrame, font=("Arial", 12), selectmode=SINGLE, height=12)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    
    #add all students to list
    for s in students:
        listbox.insert(END, f"{s['ID']} - {s['name']}")

    def showSelected():
        select = listbox.curselection()
        if select:
            index = select[0]
            clearOutput()
            display(students[index])
            openWin.destroy()
        else:
            messagebox.showwarning("Error","Please select a student")
    
    Button(openWin, text="View Student", bg="#3498db", fg="#ffffff", font=("Arial", 12), relief="flat", cursor="hand2", width=20, command=showSelected).pack(pady=20)
    
#student with highest score
def showHighest():
    highestStudent = max(students, key=lambda s: Grader(s)['totalMarks'])
    clearOutput()
    display(highestStudent)

#student with lowest score
def showLowest():
    lowestStudent = min(students, key=lambda s: Grader(s)['totalMarks'])
    clearOutput()
    display(lowestStudent)

#sorts students by marks
def sorting():
    sortWin = Toplevel(root)
    sortWin.title("Sort Students")
    sortWin.geometry("300x300")
    sortWin['bg'] = "#0c005b"
    Label(sortWin, text="Sort Order", font=("Arial", 14, "bold"), bg="#0c005b", fg="#ffffff").pack(pady=20)
    
    def sortAsc():
        students.sort(key=lambda s: Grader(s)['totalMarks'])
        viewAll()
        sortWin.destroy()
    
    def sortDes():
        students.sort(key=lambda s: Grader(s)['totalMarks'], reverse=True)
        viewAll()
        sortWin.destroy()
    
    Button(sortWin, text="Ascending", width=15, bg="#068659", fg="#ffffff", font=("Arial", 11), relief="flat", cursor="hand2", command=sortAsc).pack(pady=5)
    Button(sortWin, text="Descending", width=15, bg="#901100", fg="#ffffff", font=("Arial", 11), relief="flat", cursor="hand2", command=sortDes).pack(pady=5)

#adds new student
def addStudent():
    addWin = Toplevel(root)
    addWin.title("Add Student")
    addWin.geometry("400x500")
    addWin['bg'] = "#0c005b"
    Label(addWin, text="Add New Student", font=("Arial", 16, "bold"), bg="#0c005b", fg="#ffffff").pack(pady=20)
    
    #input boxes
    fieldsFrame = Frame(addWin, bg="#0c005b")
    fieldsFrame.pack(pady=10, padx=20, fill=BOTH)
    
    Label(fieldsFrame, text="Student ID:", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, sticky=W, pady=5)
    IDEntry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    IDEntry.grid(row=0, column=1, pady=5)
    
    Label(fieldsFrame, text="Student Name:", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=1, column=0, sticky=W, pady=5)
    nameEntry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    nameEntry.grid(row=1, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 1 ( /20):", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=2, column=0, sticky=W, pady=5)
    gr1Entry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    gr1Entry.grid(row=2, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 2 (/20):", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=3, column=0, sticky=W, pady=5)
    gr2Entry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    gr2Entry.grid(row=3, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 3 (/20):", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=4, column=0, sticky=W, pady=5)
    gr3Entry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    gr3Entry.grid(row=4, column=1, pady=5)
    
    Label(fieldsFrame, text="Exam Mark (/100):", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=5, column=0, sticky=W, pady=5)
    examEntry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    examEntry.grid(row=5, column=1, pady=5)
    
    def saveNew():
        try:
            ID = int(IDEntry.get())
            name = nameEntry.get()
            gr1 = int(gr1Entry.get())
            gr2 = int(gr2Entry.get())
            gr3 = int(gr3Entry.get())
            exam = int(examEntry.get())
            
            if not (1000 <= ID <= 9999):
                messagebox.showerror("Student ID must be 1000-9999")
                return
            if not (0 <= gr1 <= 20 and 0 <= gr2 <= 20 and 0 <= gr3 <= 20):
                messagebox.showerror("Marks must be 0-20")
                return
            if not (0 <= exam <= 100):
                messagebox.showerror("Marks must be 0-100")
                return
            
            newStudent = {
                'ID': ID,
                'name': name,
                'grade1': gr1,
                'grade2': gr2,
                'grade3': gr3,
                'exam': exam
            }
            students.append(newStudent)
            addWin.destroy()
            
        except ValueError:
            messagebox.showerror("Error","Invalid Entry")
    
    Button(addWin, text="Add Student", bg="#3498db", fg="#ffffff", font=("Arial", 12), relief="flat", cursor="hand2", command=saveNew).pack(pady=20)

#removes a student
def removeEntry(): 
    deleteWin = Toplevel(root)
    deleteWin.title("Delete Student")
    deleteWin.geometry("400x400")
    deleteWin['bg'] = "#0c005b"
    
    Label(deleteWin, text="Select Student to Remove", font=("Arial", 16, "bold"), bg="#0c005b", fg="#ffffff").pack(pady=20)
    
    listFrame = Frame(deleteWin, bg="#ffffff")
    listFrame.pack(pady=10, padx=20, fill=BOTH, expand=True)

    listbox = Listbox(listFrame, font=("Arial", 12), selectmode=SINGLE, height=12)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    
    for s in students:
        listbox.insert(END, f"{s['ID']} - {s['name']}")

    def remove():
        if listbox.curselection():
            i = listbox.curselection()[0]
            name = students[i]["name"]
            
            if messagebox.askyesno("Confirm", f"Delete {name}?"):
                students.pop(i)
                deleteWin.destroy()
                viewAll()
        else:
            messagebox.showwarning("Error", "Please select a student")
    
    Button(deleteWin, text="REMOVE", bg="#b0291a", fg="#ffffff", font=("Arial", 11), relief="flat", command=remove).pack(pady=10)
   
#updates student record
def updateEntry():
    updateWin = Toplevel(root)
    updateWin.title("Update Student")
    updateWin.geometry("400x500")
    updateWin['bg'] = "#0c005b"
    
    Label(updateWin, text="Update Student Record", font=("Arial", 16, "bold"), bg="#0c005b", fg="#ffffff").pack(pady=15)
    Label(updateWin, text="Select Student:", bg="#0c005b", fg="#ffffff", font=("Arial", 11)).pack()
    
    listFrame = Frame(updateWin, bg="#3498db")
    listFrame.pack(pady=5, padx=20)
    
    listbox = Listbox(listFrame, font=("Arial", 10), selectmode=SINGLE, height=5, width=35)
    listbox.pack(side=LEFT)

    for s in students:
        listbox.insert(END, f"{s['ID']} - {s['name']}")
    
    #fields to edit
    fieldsFrame = Frame(updateWin, bg="#0c005b")
    fieldsFrame.pack(pady=10, padx=20)
    
    Label(fieldsFrame, text="Name:", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, sticky=W, pady=5)
    nameEntry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    nameEntry.grid(row=0, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 1:", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=1, column=0, sticky=W, pady=5)
    gr1Entry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    gr1Entry.grid(row=1, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 2:", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=2, column=0, sticky=W, pady=5)
    gr2Entry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    gr2Entry.grid(row=2, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 3:", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=3, column=0, sticky=W, pady=5)
    gr3Entry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    gr3Entry.grid(row=3, column=1, pady=5)
    
    Label(fieldsFrame, text="Exam Mark:", bg="#0c005b", fg="#ffffff", font=("Arial", 10)).grid(row=4, column=0, sticky=W, pady=5)
    examEntry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    examEntry.grid(row=4, column=1, pady=5)
    
    def loadStudent():
        select = listbox.curselection()
        if select:
            index = select[0]
            student = students[index]
            
            nameEntry.delete(0, END)
            nameEntry.insert(0, student['name'])
            gr1Entry.delete(0, END)
            gr1Entry.insert(0, student['grade1'])
            gr2Entry.delete(0, END)
            gr2Entry.insert(0, student['grade2'])
            gr3Entry.delete(0, END)
            gr3Entry.insert(0, student['grade3'])
            examEntry.delete(0, END)
            examEntry.insert(0, student['exam'])
        else:
            messagebox.showwarning("Not selected", "Select a student")
    
    Button(updateWin, text="Load Student Data", bg="#3498db", fg="#ffffff", font=("Arial", 10), relief="flat", cursor="hand2", command=loadStudent).pack(pady=5)
    
    def saveUpdates():
        try:
            select = listbox.curselection()
            if select:
                index = select[0]
                
                students[index]['name'] = nameEntry.get()
                students[index]['grade1'] = int(gr1Entry.get())
                students[index]['grade2'] = int(gr2Entry.get())
                students[index]['grade3'] = int(gr3Entry.get())
                students[index]['exam'] = int(examEntry.get())
                updateWin.destroy()
            else:
                messagebox.showwarning("Error", "Select a student")
        except ValueError:
            messagebox.showerror("Invalid Number", "Please enter valid numbers")
    
    Button(updateWin, text="Save Updates", bg="#0f9d4a", fg="#ffffff", font=("Arial", 11), relief="flat", cursor="hand2", command=saveUpdates).pack(pady=5)
    
def showFrame(frame):
    frame.tkraise()

mainMenu = Frame(root, bg="#ffffff")
mainMenu.place(relwidth=1, relheight=1)

titleFrame = Frame(mainMenu, bg="#0c005b", height=100)
titleFrame.pack(fill=X)
Label(titleFrame, text="Student Manager", font=("Arial", 28, "bold"), fg="#ffffff", bg="#0c005b").pack(pady=30)

buttonFrame = Frame(mainMenu, bg="#ffffff")
buttonFrame.pack(pady=20)

row1 = Frame(buttonFrame, bg="#ffffff")
row1.pack(pady=5)
Button(row1, text="View All Students", width=20, height=2, bg="#0c005b", fg="#ffffff", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=viewAll).pack(side=LEFT, padx=5)
Button(row1, text="View Individual Student", width=20, height=2, bg="#0c005b", fg="#ffffff", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=viewSingle).pack(side=LEFT, padx=5)
Button(row1, text="Highest Score", width=20, height=2, bg="#0c005b", fg="#ffffff", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=showHighest).pack(side=LEFT, padx=5)
Button(row1, text="Lowest Score", width=20, height=2, bg="#0c005b", fg="#ffffff", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=showLowest).pack(side=LEFT, padx=5)

row2 = Frame(buttonFrame, bg="#ffffff")
row2.pack(pady=5)
Button(row2, text="Sort Students", width=20, height=2, bg="#0c005b", fg="#ffffff", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=sorting).pack(side=LEFT, padx=5)
Button(row2, text="Add New Student", width=20, height=2, bg="#0c005b", fg="#ffffff", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=addStudent).pack(side=LEFT, padx=5)
Button(row2, text="Remove Student", width=20, height=2, bg="#0c005b", fg="#ffffff", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=removeEntry).pack(side=LEFT, padx=5)
Button(row2, text="Update Student", width=20, height=2, bg="#0c005b", fg="#ffffff", font=("Arial", 11, "bold"), relief="flat", cursor="hand2", command=updateEntry).pack(side=LEFT, padx=5)

displayFrame = Frame(mainMenu, bg="#0c005b")
displayFrame.pack(fill=BOTH, expand=True, padx=20, pady=10)
Label(displayFrame, text="Student Records", font=("Arial", 14, "bold"), bg="#0c005b", fg="#ffffff").pack(anchor=W, pady=5)

treeFrame = Frame(displayFrame)
treeFrame.pack(fill=BOTH, expand=True)

#treeview widget
tree = ttk.Treeview(treeFrame, columns=("ID", "Name", "gr1", "gr2", "gr3", "Exam", "Total gr", "Total", "percent", "Grade"), show="headings", height=15)

#define columns
tree.heading("ID", text="Student ID")
tree.heading("Name", text="Student Name")
tree.heading("gr1", text="gr 1")
tree.heading("gr2", text="gr 2")
tree.heading("gr3", text="gr 3")
tree.heading("Exam", text="Exam")
tree.heading("Total gr", text="Total gr")
tree.heading("Total", text="Total Marks")
tree.heading("percent", text="percent")
tree.heading("Grade", text="Grade")

#set column widths
tree.column("ID", width=100, anchor=CENTER)
tree.column("Name", width=150, anchor=W)
tree.column("gr1", width=60, anchor=CENTER)
tree.column("gr2", width=60, anchor=CENTER)
tree.column("gr3", width=60, anchor=CENTER)
tree.column("Exam", width=60, anchor=CENTER)
tree.column("Total gr", width=80, anchor=CENTER)
tree.column("Total", width=90, anchor=CENTER)
tree.column("percent", width=90, anchor=CENTER)
tree.column("Grade", width=60, anchor=CENTER)

tree.pack(fill=BOTH, expand=True)

#load students when program starts
studentIndex()
root.mainloop()