from tkinter import *
from PIL import ImageTk
from tkinter import messagebox, ttk

root  = Tk()
root.geometry("1000x600") #window size
root['bg'] = "#2e0947"
root.title("Student Manager")

root.iconphoto(False, ImageTk.PhotoImage(file="Exercise 3 - Student Manager/document.png"))

filename = "Exercise 3 - Student Manager/studentMarks.txt"
students = []

#loads students from text file
def studentIndex():
    global students
    students = [] #clear list
    with open(filename, "r") as file:
        lines = file.readlines()
        numStudents = int(lines[0].strip()) #first line is number of students
            
        for i in range(1, numStudents + 1):
            data = lines[i].strip().split(",")
            student = {
                'ID': data[0],
                'name': data[1],
                'grade1': int(data[2]),
                'grade2': int(data[3]),
                'grade3': int(data[4]),
                'exam': int(data[5])
                }
            students.append(student)

#saves students back to file
def saveStudents():
    with open(filename, "w") as file:
        file.write(f"{len(students)}\n")
        for student in students:
            file.write(f"{student['ID']},{student['name']},"
                      f"{student['grade1']},{student['grade2']},"
                      f"{student['grade3']},{student['exam']}\n")
    messagebox.showinfo("Data saved")

#calculates stats for a student
def Grader(student):
    totalgrade = (student['grade1'] + 
                      student['grade2'] + 
                      student['grade3'])
    totalMarks = totalgrade + student['exam']
    percent = (totalMarks / 160) * 100
    
    #work out grade
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

#clears grid
def clearOutput():
    for item in tree.get_children():
        tree.delete(item)
    summaryLabel.config(text="")

#adds student to grid
def addNew(student):
    stats = Grader(student)
    tree.insert("", END, values=(
        student['ID'], student['name'], student['grade1'], student['grade2'],
        student['grade3'], student['exam'], stats['totalgrade'], stats['totalMarks'],
        f"{stats['percent']}%",
        stats['grade']
    ))

#updates summary label
def updateSummary(text):
    summaryLabel.config(text=text)



#shows all students
def viewAll():
    clearOutput()
    if not students:
        updateSummary("No students found")
        return
    
    totalpercent = 0
    
    for student in students:
        addNew(student)
        stats = Grader(student)
        totalpercent += stats['percent']
    
    #summary at the end
    averagepercent = totalpercent / len(students)
    updateSummary(f"Total Students: {len(students)} | Average percent: {averagepercent}%")

#view one student
def viewSingle():
    if not students:
        messagebox.showwarning("No students found")
        return
    
    #create popup window
    selectWindow = Toplevel(root)
    selectWindow.title("Select Student")
    selectWindow.geometry("400x400")
    selectWindow['bg'] = "#ffffff"
    
    Label(selectWindow, text="Select a Student", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=20)
    
    #create listbox with scrollbar
    listFrame = Frame(selectWindow, bg="#ffffff")
    listFrame.pack(pady=10, padx=20, fill=BOTH, expand=True)
    
    listbox = Listbox(listFrame, font=("Arial", 12), selectmode=SINGLE, height=12)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)

    
    #add all students to listbox
    for s in students:
        listbox.insert(END, f"{s['ID']} - {s['name']}")
    
    #select first student by default
    listbox.select_set(0)
    
    def showSelected():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            clearOutput()
            addNew(students[index])
            updateSummary(f"Individual Record: {students[index]['name']}")
            selectWindow.destroy()
        else:
            messagebox.showwarning("Please select a student")
    
    Button(selectWindow, text="View Student", bg="#3498db", fg="white", 
           font=("Arial", 12), relief="flat", cursor="hand2",
           width=20, command=showSelected).pack(pady=20)
    
#shows student with highest score
def showHigest():
    if not students:
        messagebox.showwarning("No students found")
        return
    
    highestStudent = max(students, key=lambda s: Grader(s)['totalMarks'])
    
    clearOutput()
    addNew(highestStudent)
    stats = Grader(highestStudent)
    updateSummary(f"Highest Score: {highestStudent['name']} with {stats['totalMarks']}/160 ({stats['percent']}%)")

#shows student with lowest score
def showLowest():
    if not students:
        messagebox.showwarning("No students found")
        return
    
    lowestStudent = min(students, key=lambda s: Grader(s)['totalMarks'])
    
    clearOutput()
    addNew(lowestStudent)
    stats = Grader(lowestStudent)
    updateSummary(f"Lowest Score: {lowestStudent['name']} with {stats['totalMarks']}/160 ({stats['percent']}%)")

#sorts students by marks
def sorting():
    if not students:
        messagebox.showwarning("No students found")
        return
    
    #popup to choose order
    sortWindow = Toplevel(root)
    sortWindow.title("Sort Students")
    sortWindow.geometry("300x300")
    sortWindow['bg'] = "#ffffff"
    
    Label(sortWindow, text="Sort Order", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=20)
    
    def sortAscending():
        students.sort(key=lambda s: Grader(s)['totalMarks'])
        viewAll()
        sortWindow.destroy()
    
    def sortDescending():
        students.sort(key=lambda s: Grader(s)['totalMarks'], reverse=True)
        viewAll()
        sortWindow.destroy()
    
    Button(sortWindow, text="Ascending", width=15, bg="#0f58d6", fg="white", 
           font=("Arial", 11), relief="flat", cursor="hand2",
           command=sortAscending).pack(pady=5)
    
    Button(sortWindow, text="Descending", width=15, bg="#f0f361", fg="white", 
           font=("Arial", 11), relief="flat", cursor="hand2",
           command=sortDescending).pack(pady=5)

#adds new student
def addStudent():
    addWindow = Toplevel(root)
    addWindow.title("Add Student")
    addWindow.geometry("400x500")
    addWindow['bg'] = "#ffffff"
    
    Label(addWindow, text="Add New Student", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=20)
    
    #input boxes
    fieldsFrame = Frame(addWindow, bg="#ffffff")
    fieldsFrame.pack(pady=10, padx=20, fill=BOTH)
    
    Label(fieldsFrame, text="Student ID:", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, sticky=W, pady=5)
    IDEntry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    IDEntry.grid(row=0, column=1, pady=5)
    
    Label(fieldsFrame, text="Student Name:", bg="#ffffff", font=("Arial", 10)).grid(row=1, column=0, sticky=W, pady=5)
    nameEntry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    nameEntry.grid(row=1, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 1 ( /20):", bg="#ffffff", font=("Arial", 10)).grid(row=2, column=0, sticky=W, pady=5)
    gr1Entry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    gr1Entry.grid(row=2, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 2 (/20):", bg="#ffffff", font=("Arial", 10)).grid(row=3, column=0, sticky=W, pady=5)
    gr2Entry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    gr2Entry.grid(row=3, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 3 (/20):", bg="#ffffff", font=("Arial", 10)).grid(row=4, column=0, sticky=W, pady=5)
    gr3Entry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    gr3Entry.grid(row=4, column=1, pady=5)
    
    Label(fieldsFrame, text="Exam Mark (/100):", bg="#ffffff", font=("Arial", 10)).grid(row=5, column=0, sticky=W, pady=5)
    examEntry = Entry(fieldsFrame, font=("Arial", 10), width=25)
    examEntry.grid(row=5, column=1, pady=5)
    
    def saveNewStudent():
        try:
            ID = int(IDEntry.get())
            name = nameEntry.get()
            gr1 = int(gr1Entry.get())
            gr2 = int(gr2Entry.get())
            gr3 = int(gr3Entry.get())
            exam = int(examEntry.get())
            
            #check values are valid
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
            saveStudents()
            addWindow.destroy()
            
        except ValueError:
            messagebox.showerror("Please enter valid numbers")
    
    Button(addWindow, text="Add Student", bg="#1abc9c", fg="white", 
           font=("Arial", 12), relief="flat", cursor="hand2",
           command=saveNewStudent).pack(pady=20)

#removes a student
def removeEntry():
    if not students:
        messagebox.showwarning("No students found")
        return
    
    deleteWindow = Toplevel(root)
    deleteWindow.title("Delete Student")
    deleteWindow.geometry("400x400")
    deleteWindow['bg'] = "#ffffff"
    
    Label(deleteWindow, text="Select Student to Remove", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=20)
    
    #create listbox with scrollbar
    listFrame = Frame(deleteWindow, bg="#ffffff")
    listFrame.pack(pady=10, padx=20, fill=BOTH, expand=True)
    
    listbox = Listbox(listFrame, font=("Arial", 12), selectmode=SINGLE, height=12)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    
    #add all students to listbox
    for s in students:
        listbox.insert(END, f"{s['ID']} - {s['name']}")
    
    Button(deleteWindow, text="Delete Student", bg="#e74c3c", fg="white", 
           font=("Arial", 12), relief="flat", cursor="hand2").pack(pady=20)
    
#updates a students record
def updateEntry():
    if not students:
        messagebox.showwarning("No students found")
        return
    
    updateWindow = Toplevel(root)
    updateWindow.title("Update Student")
    updateWindow.geometry("450x550")
    updateWindow['bg'] = "#ffffff"
    
    Label(updateWindow, text="Update Student Record", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=15)
    
    Label(updateWindow, text="Select Student:", bg="#ffffff", font=("Arial", 11)).pack()
    
    #create listbox with scrollbar
    listFrame = Frame(updateWindow, bg="#ffffff")
    listFrame.pack(pady=5, padx=20)
    
    listbox = Listbox(listFrame, font=("Arial", 10), selectmode=SINGLE, height=5, width=35)
    listbox.pack(side=LEFT)
    
    #add all students to listbox
    for s in students:
        listbox.insert(END, f"{s['ID']} - {s['name']}")
    
    #fields to edit
    fieldsFrame = Frame(updateWindow, bg="#ffffff")
    fieldsFrame.pack(pady=10, padx=20)
    
    Label(fieldsFrame, text="Name:", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, sticky=W, pady=5)
    nameEntry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    nameEntry.grid(row=0, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 1:", bg="#ffffff", font=("Arial", 10)).grid(row=1, column=0, sticky=W, pady=5)
    gr1Entry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    gr1Entry.grid(row=1, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 2:", bg="#ffffff", font=("Arial", 10)).grid(row=2, column=0, sticky=W, pady=5)
    gr2Entry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    gr2Entry.grid(row=2, column=1, pady=5)
    
    Label(fieldsFrame, text="grade 3:", bg="#ffffff", font=("Arial", 10)).grid(row=3, column=0, sticky=W, pady=5)
    gr3Entry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    gr3Entry.grid(row=3, column=1, pady=5)
    
    Label(fieldsFrame, text="Exam Mark:", bg="#ffffff", font=("Arial", 10)).grid(row=4, column=0, sticky=W, pady=5)
    examEntry = Entry(fieldsFrame, font=("Arial", 10), width=20)
    examEntry.grid(row=4, column=1, pady=5)
    
    def loadStudent():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
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
            messagebox.showwarning("Please select a student", "Select a student")
    
    Button(updateWindow, text="Load Student Data", bg="#3498db", fg="white", 
           font=("Arial", 10), relief="flat", cursor="hand2",
           command=loadStudent).pack(pady=5)
    
    def saveUpdates():
        try:
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                
                students[index]['name'] = nameEntry.get()
                students[index]['grade1'] = int(gr1Entry.get())
                students[index]['grade2'] = int(gr2Entry.get())
                students[index]['grade3'] = int(gr3Entry.get())
                students[index]['exam'] = int(examEntry.get())
                
                saveStudents()
                updateWindow.destroy()
            else:
                messagebox.showwarning("Please select a student", "Select a student")
            
        except ValueError:
            messagebox.showerror("Invalid Number", "Please enter valid numbers")
    
    Button(updateWindow, text="Save Updates", bg="#2ecc71", fg="white", 
           font=("Arial", 11), relief="flat", cursor="hand2",
           command=saveUpdates).pack(pady=5)
    
#switch between screens
def showFrame(frame):
    frame.tkraise()

#create all screens
mainMenu = Frame(root, bg="#ffffff")
mainMenu.place(relwidth=1, relheight=1)

#title at top
titleFrame = Frame(mainMenu, bg="#2c3e50", height=100)
titleFrame.pack(fill=X)

Label(titleFrame, text="Student Manager", font=("Arial", 28, "bold"), 
      fg="white", bg="#2c3e50").pack(pady=30)

#buttons
buttonFrame = Frame(mainMenu, bg="#ffffff")
buttonFrame.pack(pady=20)

#row 1 - main features
row1 = Frame(buttonFrame, bg="#ffffff")
row1.pack(pady=5)

Button(row1, text="View All Students", width=20, height=2, bg="#3498db", fg="white", 
       font=("Arial", 11, "bold"), relief="flat", cursor="hand2",
       command=viewAll).pack(side=LEFT, padx=5)

Button(row1, text="View Individual Student", width=20, height=2, bg="#9b59b6", fg="white", 
       font=("Arial", 11, "bold"), relief="flat", cursor="hand2",
       command=viewSingle).pack(side=LEFT, padx=5)

Button(row1, text="Highest Score", width=20, height=2, bg="#2ecc71", fg="white", 
       font=("Arial", 11, "bold"), relief="flat", cursor="hand2",
       command=showHigest).pack(side=LEFT, padx=5)

Button(row1, text="Lowest Score", width=20, height=2, bg="#e74c3c", fg="white", 
       font=("Arial", 11, "bold"), relief="flat", cursor="hand2",
       command=showLowest).pack(side=LEFT, padx=5)

#row 2 - extra features
row2 = Frame(buttonFrame, bg="#ffffff")
row2.pack(pady=5)

Button(row2, text="Sort Students", width=20, height=2, bg="#f39c12", fg="white", 
       font=("Arial", 11, "bold"), relief="flat", cursor="hand2",
       command=sorting).pack(side=LEFT, padx=5)

Button(row2, text="Add New Student", width=20, height=2, bg="#1abc9c", fg="white", 
       font=("Arial", 11, "bold"), relief="flat", cursor="hand2",
       command=addStudent).pack(side=LEFT, padx=5)

Button(row2, text="Remove Student", width=20, height=2, bg="#e67e22", fg="white", 
       font=("Arial", 11, "bold"), relief="flat", cursor="hand2",
       command=removeEntry).pack(side=LEFT, padx=5)

Button(row2, text="Update Student", width=20, height=2, bg="#34495e", fg="white", 
       font=("Arial", 11, "bold"), relief="flat", cursor="hand2",
       command=updateEntry).pack(side=LEFT, padx=5)

#output display area
displayFrame = Frame(mainMenu, bg="#ffffff")
displayFrame.pack(fill=BOTH, expand=True, padx=20, pady=10)

Label(displayFrame, text="Student Records", font=("Arial", 14, "bold"), bg="#ffffff").pack(anchor=W, pady=5)

#create treeview (table/grid)
treeFrame = Frame(displayFrame)
treeFrame.pack(fill=BOTH, expand=True)

#treeview widget (excel-style grid)
tree = ttk.Treeview(treeFrame, 
                    columns=("ID", "Name", "gr1", "gr2", "gr3", "Exam", "Total gr", "Total", "percent", "Grade"),
                    show="headings", height=15)

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

#summary label below grid
summaryLabel = Label(displayFrame, text="", font=("Arial", 11, "bold"), bg="#ffffff", fg="#2c3e50", anchor=W)
summaryLabel.pack(fill=X, pady=10)

#load students when program starts
studentIndex()

root.mainloop()