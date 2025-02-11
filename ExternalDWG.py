import os
from tkinter import *
from tkinter import messagebox, filedialog
autoDeskFolder = r"C:\Program Files\Autodesk"
def getLispTorepathAndRenameXref(targetXref, newXrefPath):
    baselispforinjection=f'''
    (if (tblsearch "block" "{targetXref}")
    (COMMAND "-xref" "P" "{targetXref}" "{newXrefPath}" "-RENAME" "b" "{targetXref}" "{os.path.basename(newXrefPath)}" )
    (princ "\\n{targetXref} not found. ")
    )'''
    return baselispforinjection
def getLispToOverlayeXref(targetXrefPath, xrefLayer="ZZ-Zz9030-M-ExtReferenceInfo", xrefDrawOrder="back"):
    baselispforinjection=f'''
    (COMMAND "TILEMODE" "1" "-layer" "m" "{xrefLayer}" "" "-xref" "O" "{targetXrefPath}" "r" "0" "s" "1" "0,0,0" "Draworder" "si" "l" "{xrefDrawOrder}" )
    '''
    return baselispforinjection
class ExternalDWG:
    def __init__(self, root):
        self.root = root
        self.selected_files=[]
        self.toworkonfiles=set()
        self.root.title("External DWG")
        self.root.geometry("600x300")
        self.taskList = []
        self.toworkonTasklist = set()
        self.leftMainFrame = Frame(self.root, width=200, bg='lightgrey')
        introductionButton = Button(self.leftMainFrame, text="Introduction", command=self.showIntroduction)
        introductionButton.pack(side="top", padx=10, pady=10, fill=X)
        load_Drawing_btn = Button(self.leftMainFrame, text="Load Drawings", command=self.onLoadDrawing)
        load_Drawing_btn.pack(side="top", padx=10, pady=[0,10], fill=X)
        overlayXrefButton = Button(self.leftMainFrame, text="Overlay", command=self.overlayXrefs)
        overlayXrefButton.pack(side="top", padx=10, pady=[0,10], fill=X)
        tasklistButton = Button(self.leftMainFrame, text="Task List", command=self.showTasklist)
        tasklistButton.pack(side=TOP, padx=10, pady=[0,10], fill=X)
        self.leftMainFrame.pack(side='left', fill='y')
        self.rightFrame = Frame(self.root)
        self.rightFrame.pack(fill=BOTH, expand=True)
#####################################################################################################################################################################
    def showTasklist(self):
        self.root.maxsize(600, 300)
        self.root.geometry("600x300")
        self.rightFrame.config(bg="#f0f0f0")
        for  wd in self.rightFrame.winfo_children():
            wd.destroy()
        titleLabel = Label(self.rightFrame, text="Task List", font=("Arial", 15, ["bold", "underline"]))
        titleLabel.pack(side=TOP)
        taskCanavas = Canvas(self.rightFrame)
        taskScroller = Scrollbar(self.rightFrame, orient=VERTICAL, command=taskCanavas.yview)
        taskScrollableFrame = Frame(taskCanavas)
        taskScrollableFrame.bind(
            "<Configure>",
            lambda e: taskCanavas.configure(scrollregion=taskCanavas.bbox("all"))
        )
        taskCanavas.create_window((0,0), window=taskScrollableFrame, anchor="nw")
        taskCanavas.configure(yscrollcommand=taskScroller.set)
        taskCanavas.pack(side=LEFT,fill=BOTH,expand=True)
        taskScroller.pack(side=RIGHT, fill=Y)
        taskCanavas.bind("<Enter>", lambda e: taskCanavas.bind_all("<MouseWheel>", lambda e: taskCanavas.yview_scroll(int(-1 * (e.delta / 120)), "units")))
        taskCanavas.bind("<Leave>", lambda e: taskCanavas.unbind_all("<MouseWheel>"))
        self.tasks_check_vars=[]
        for index, task in enumerate(self.taskList):
            if task in self.toworkonTasklist:
                var = IntVar(value=1)
            else:
                var = IntVar(value=0)
            self.tasks_check_vars.append(var)
            task_frame = Frame(taskScrollableFrame)
            task_frame.pack(fill=X, padx=10, pady=2)
            cb = Checkbutton(task_frame, variable=var, command=lambda i=index: self.update_task(i))
            cb.pack(side=LEFT)
            label = Label(task_frame, text=task, wraplength=300, anchor=W, justify=LEFT)
            label.pack(side=LEFT, fill=X, expand=True)
        removeTaskButton = Button(self.rightFrame, text="Remove Selected", width=18, command=self.removeSelectedTask).pack(side=BOTTOM, pady=3)
        moveSelectedUpButton = Button(self.rightFrame, text="Move Up", width=18, command=self.moveUp).pack(side=BOTTOM, pady=3)
        moveSelectedDownButton = Button(self.rightFrame, text="Move Down", width=18, command=self.moveDown).pack(side=BOTTOM, pady=3)
        self.selectAllTaskButton = Button(self.rightFrame, text="Select All", width=18, command=self.toggleTaskSelectButton)
        self.selectAllTaskButton.pack(side=BOTTOM, pady=3)
    def moveUp(self):
        try:
            pass
        except Exception as e:
            messagebox.showinfo("No task selected", "Please select a task to proceed.")
    def moveDown(self):
        try:
            # print(self.toworkonTasklist)
            pass
        except Exception as e:
            messagebox.showinfo("No task selected", "Please select a task to proceed.")
    def toggleTaskSelectButton(self):
        if all(var.get() == 1 for var in self.tasks_check_vars):
            self.unselectAllTasks()
        else:
            self.selectAllTasks()
    def selectAllTasks(self):
        for var in self.tasks_check_vars:
            var.set(1)
        self.toworkonTasklist.update(self.taskList)
        self.updateSelectAllTaskButtonText()
    def unselectAllTasks(self):
        for var in self.tasks_check_vars:
            var.set(0)    
        self.toworkonfiles.clear()
        self.updateSelectAllTaskButtonText()
    def updateSelectAllTaskButtonText(self):
        if not self.tasks_check_vars:
            self.selectAllTaskButton.config(state=DISABLED)
        else:
            self.selectAllTaskButton.config(state=NORMAL)
        if all(var.get() == 1 for var in self.tasks_check_vars):
            self.selectAllTaskButton.config(text="Unselect All")
        else:
            self.selectAllTaskButton.config(text="Select All")
    def update_task(self, index):
        if self.tasks_check_vars[index].get() == 1:
            if self.taskList[index] not in self.toworkonTasklist:
                self.toworkonTasklist.add(self.taskList[index])
        else:
            if self.taskList[index] in self.toworkonTasklist:
                    self.toworkonTasklist.remove(self.taskList[index])
        self.updateSelectAllTaskButtonText()
    def removeSelectedTask(self):
        try:
            task_to_remove = list(self.toworkonTasklist)
            for file in task_to_remove:
                if file in self.taskList:
                    self.taskList.remove(file)
            self.toworkonTasklist.clear()
            self.showTasklist()
        except Exception as e:
            messagebox.showinfo("No task selected", "Please select a task to proceed.")
####################################################################################################################################################
    def showIntroduction(self):
        # self.root.resizable(True, True)
        self.root.maxsize(600, 300)
        self.root.geometry("600x300")
        self.rightFrame.config(bg="#f0f0f0")
        for wd in self.rightFrame.winfo_children():
            wd.destroy()
        titleLabel = Label(self.rightFrame, text="INTRODUCTION", font=("Arial", 15, ["bold", "underline"]))
        titleLabel.pack(side="top")
        usageParagparh = Label(self.rightFrame, text="This is usage information area to be updated", font=("Arial", 10, ["bold"]))
        usageParagparh.pack(padx=10, pady=10)
        #here I will add usage and documentation in future....
    def onLoadDrawing(self):
        self.root.maxsize(600, 300)
        self.root.geometry("600x300")
        self.rightFrame.config(bg="#f0f0f0")
        for wd in self.rightFrame.winfo_children():
            wd.destroy()
        canvas = Canvas(self.rightFrame)
        scrollbar = Scrollbar(self.rightFrame, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.add_drawing_check_vars = []
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        for index, file in enumerate(self.selected_files):
            var = IntVar(value=1 if file in self.toworkonfiles else 0)
            self.add_drawing_check_vars.append(var)
            file_frame = Frame(scrollable_frame)
            file_frame.pack(fill=X, padx=10, pady=2)
            cb = Checkbutton(file_frame, variable=var, command=lambda i=index: self.update_files(i))
            cb.pack(side=LEFT)
            label = Label(file_frame, text=file, wraplength=300, anchor=W, justify=LEFT)
            label.pack(side=LEFT, fill=X, expand=True)
        removeDrawingButton = Button(self.rightFrame, text="Remove Selected", width=18, command=self.removeSelectedFiles)
        removeDrawingButton.pack(side=BOTTOM, pady=3)
        self.selectAllFileButton = Button(self.rightFrame, text="Select All", width=18, command=self.toggleSelectAll)
        self.selectAllFileButton.pack(side=BOTTOM, pady=3)
        addDrawingButton = Button(self.rightFrame, text="Browse", width=18, command=self.addFiles)
        addDrawingButton.pack(side=BOTTOM, pady=3)
        self.updateSelectAllFileButtonText()
    def toggleSelectAll(self):
        if all(var.get() == 1 for var in self.add_drawing_check_vars):
            self.unselectAllFiles()
        else:
            self.selectAllFiles()
    def selectAllFiles(self):
        for var in self.add_drawing_check_vars:
            var.set(1)
        self.toworkonfiles.update(self.selected_files)
        self.updateSelectAllFileButtonText()
    def unselectAllFiles(self):
        for var in self.add_drawing_check_vars:
            var.set(0)    
        self.toworkonfiles.clear()
        self.updateSelectAllFileButtonText()
    def update_files(self, index):
        if self.add_drawing_check_vars[index].get() == 1:
            if self.selected_files[index] not in self.toworkonfiles:
                self.toworkonfiles.add(self.selected_files[index])
        else:
            if self.selected_files[index] in self.toworkonfiles:
                    self.toworkonfiles.remove(self.selected_files[index])
        self.updateSelectAllFileButtonText()
    def removeSelectedFiles(self):
        files_to_remove = {file for file, var in zip(self.selected_files, self.add_drawing_check_vars) if var.get() == 1}
        if not files_to_remove:
            messagebox.showinfo("No files selected", "Please select drawing file(s) to proceed.")
            return
        self.selected_files = [file for file in self.selected_files if file not in files_to_remove]
        self.toworkonfiles.difference_update(files_to_remove)
        self.onLoadDrawing()
    def updateSelectAllFileButtonText(self):
        if not self.add_drawing_check_vars:
            self.selectAllFileButton.config(state=DISABLED)
        else:
            self.selectAllFileButton.config(state=NORMAL)
        if all(var.get() == 1 for var in self.add_drawing_check_vars):
            self.selectAllFileButton.config(text="Unselect All")
        else:
            self.selectAllFileButton.config(text="Select All")
    def addFiles(self):
        getFilesVar = filedialog.askopenfilenames(title="Select Target Drawing Files", filetypes=[("DWG files", "*.dwg")])
        if getFilesVar is not None:
            for file in getFilesVar:
                self.selected_files.append(file)
                self.toworkonfiles.add(file)
            self.onLoadDrawing()
            return
        messagebox.showinfo("No files selected", "Please select drawing file(s) to proceed.")
    def overlayXrefs(self):
        for wb in self.rightFrame.winfo_children():
            wb.destroy()
        self.rightFrame.config(bg="skyblue")
        def browseXrefOverLayfile(xrefPathEntry):
            xrefPath = filedialog.askopenfilename(title="Select Xref Overlay File", filetypes=[("DWG files", "*.dwg")])
            if xrefPath is not None:
                xrefPathEntry.delete(0, END)
                xrefPathEntry.insert(0, xrefPath)
        overlayHeading = Label(self.rightFrame, text="Overlay Xref", font=("Arial", 15, ["bold", "underline"]), bg="skyblue").pack(side=TOP)
        mainContainer = Frame(self.rightFrame, bg="skyblue")
        mainContainer.pack(fill=BOTH, expand=True, padx=10, pady=10)
        labels = [
            "Xref Path", "Insertion Point", "Rotation", "Scale", "Draworder - Front/Back", "Destination Layer Name"
        ]
        default_values = [
            "", "0,0,0", "0", "1", "back", "ZZ-Zz9030-M-ExtReferenceInfo"
        ]
        entries = []
        for i, (label_text, default_value) in enumerate(zip(labels, default_values)):
            # Label
            label = Label(mainContainer, text=label_text, bg="skyblue", font=("Arial", 10, "bold"), anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = Entry(mainContainer, font=("Arial", 10))
            entry.insert(0, default_value)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            entries.append(entry)
            if label_text == "Xref Path":
                browse_button = Button(mainContainer, text="Browse", command=lambda e=entry: browseXrefOverLayfile(e))
                browse_button.grid(row=i, column=2, padx=5, pady=5)
        def addThisOverlayToTaskList():
            xrefPath = entries[0].get()
            insertionPoint = entries[1].get()
            rotation = entries[2].get()
            scale = entries[3].get()
            draworder = entries[4].get()
            layerName = entries[5].get()
            if not all([xrefPath, layerName, draworder, insertionPoint, rotation, scale]):
                messagebox.showerror("Invalid input", "All fields are required.")
                return
            listToInject = getLispToOverlayeXref(xrefPath, layerName, draworder)
            if listToInject in self.taskList:
                messagebox.showerror("Duplicate Task", "Task already exists in the task list.")
                return
            self.taskList.append(listToInject)
            messagebox.showinfo("Success", "Task added to the task list.")
            entries[0].delete(0,END)
            # print(listToInject)
        add_button = Button(mainContainer, text="Add Task", command=addThisOverlayToTaskList, bg="lightgreen", font=("Arial", 10, "bold"))
        add_button.grid(row=len(labels), column=0, columnspan=3, pady=10, sticky="ew")
        mainContainer.grid_columnconfigure(1, weight=1)
        mainContainer.grid_rowconfigure(len(labels), weight=1)
root = Tk()
if not os.path.exists(autoDeskFolder):
    messagebox.showerror("AutoDesk not found", "Please install AutoCAD/CIVIL 3D installed before using it.")
    exit(0)
internalAutoDeskFolder = os.listdir(autoDeskFolder)
versions=set()
C3DVersions = set()
AcadVersions = set()
for fs in internalAutoDeskFolder:
    if fs.startswith("AutoCAD"):
        versionNumber = fs.split()[1]
        versions.add(versionNumber)
        intenalAutoCADFolder = os.listdir(os.path.join(autoDeskFolder, fs))
        if "C3D" in list(intenalAutoCADFolder):
            C3DVersions.add(versionNumber)
        if "acad.exe" in list(intenalAutoCADFolder):
            AcadVersions.add(versionNumber)
print(versions)
print(f"C3D versions: {C3DVersions}")
print(f"Acad versions: {AcadVersions}")
externalDWG = ExternalDWG(root)
externalDWG.showIntroduction()
root.mainloop()
