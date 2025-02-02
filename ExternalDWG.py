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
        # self.root.maxsize(600,300)
        # self.root.resizable(False, False)
        self.leftMainFrame = Frame(self.root, width=200, bg='lightgrey')
        introductionButton = Button(self.leftMainFrame, text="Introduction", command=self.showIntroduction)
        introductionButton.pack(side="top", padx=10, pady=10, fill=X)
        load_Drawing_btn = Button(self.leftMainFrame, text="Load Drawings", command=self.onLoadDrawing) #command=self.setup_drawing_window
        load_Drawing_btn.pack(side="top", padx=10, pady=[0,10], fill=X)
        overlayXrefButton = Button(self.leftMainFrame, text="Overlay", command=self.overlayXrefs)
        overlayXrefButton.pack(side="top", padx=10, pady=[0,10], fill=X)
        tasklistButton = Button(self.leftMainFrame, text="Task List", command=self.showTasklist)
        tasklistButton.pack(side=TOP, padx=10, pady=[0,10], fill=X)
        self.leftMainFrame.pack(side='left', fill='y')
        self.rightFrame = Frame(self.root)
        self.rightFrame.pack(fill=BOTH, expand=True)
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
    def update_task(self, index):
        if self.tasks_check_vars[index].get() == 1:
            if self.taskList[index] not in self.toworkonTasklist:
                self.toworkonTasklist.add(self.taskList[index])
        else:
            if self.taskList[index] in self.toworkonTasklist:
                    self.toworkonTasklist.remove(self.taskList[index])
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
        for index, file in enumerate(self.selected_files):
            if file in self.toworkonfiles:
                var = IntVar(value=1)
            else:
                var = IntVar(value=0)
            self.add_drawing_check_vars.append(var)
            file_frame = Frame(scrollable_frame)
            file_frame.pack(fill=X, padx=10, pady=2)
            cb = Checkbutton(file_frame, variable=var, command=lambda i=index: self.update_files(i))
            cb.pack(side=LEFT)
            label = Label(file_frame, text=file, wraplength=300, anchor=W, justify=LEFT)
            label.pack(side=LEFT, fill=X, expand=True)
        removeDrawingButton = Button(self.rightFrame, text="Remove Selected", width=18, command=self.removeSelectedFiles).pack(side=BOTTOM, pady=3)
        addDrawingButton = Button(self.rightFrame, text="Browse", width=18, command=self.addFiles).pack(side=BOTTOM, pady=3)
        self.rightMainFrame = Frame(self.root,background="yellow")
        self.rightMainFrame.pack(side=RIGHT, fill=Y)
    def update_files(self, index):
        if self.add_drawing_check_vars[index].get() == 1:
            if self.selected_files[index] not in self.toworkonfiles:
                self.toworkonfiles.add(self.selected_files[index])
        else:
            if self.selected_files[index] in self.toworkonfiles:
                    self.toworkonfiles.remove(self.selected_files[index])
    def removeSelectedFiles(self):
        try:
            files_to_remove = list(self.toworkonfiles)
            for file in files_to_remove:
                if file in self.selected_files:
                    self.selected_files.remove(file)
            self.toworkonfiles.clear()
            self.onLoadDrawing()
        except Exception as e:
            messagebox.showinfo("No files selected", "Please select drawing file(s) to proceed.")

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
        def browseXrefOverLayfile(xrefPathEntry):
            xrefPath = filedialog.askopenfilename(title="Select Xref Overlay File", filetypes=[("DWG files", "*.dwg")])
            if xrefPath is not None:
                xrefPathEntry.delete(0, END)
                xrefPathEntry.insert(0, xrefPath)
        rightFirstFrame = Frame(self.rightFrame,bg="skyblue")
        rightSecondFrame = Frame(self.rightFrame,bg="skyblue")
        rightThirdFrame = Frame(self.rightFrame,bg="skyblue")
        self.rightFrame.config(bg="skyblue")
        # self.root.geometry("415x150")
        # self.root.maxsize(415,150)
        # self.root.resizable(False, False)
        # First frame elements:
        optionLabel = Label(rightFirstFrame, text="Option", bg="skyblue", borderwidth=1, relief=SOLID)
        optionLabel.pack(side="top", fill=X)
        xrefPathLabel = Label(rightFirstFrame, text="Xref Path", borderwidth=1, relief=SOLID)
        xrefPathLabel.pack(side="top", anchor="w", fill=X ,pady=2)
        xrefInsertionPointLabel = Label(rightFirstFrame, text="Insertion Point", borderwidth=1, relief=SOLID)
        xrefInsertionPointLabel.pack(side="top", anchor="w", fill=X ,pady=1)
        xrefRotationLabel = Label(rightFirstFrame, text="Rotation", borderwidth=1, relief=SOLID)
        xrefRotationLabel.pack(side="top", anchor="w", fill=X ,pady=1)
        xrefScaleLabel = Label(rightFirstFrame, text="Scale", borderwidth=1, relief=SOLID)
        xrefScaleLabel.pack(side="top", anchor="w", fill=X ,pady=1)
        xrefDraworderLabel = Label(rightFirstFrame, text="Draworder - Front/Back", borderwidth=1, relief=SOLID)
        xrefDraworderLabel.pack(side="top", anchor="w", fill=X ,pady=1)
        xrefLayerLabel = Label(rightFirstFrame, text="Destination Layer Name", borderwidth=1, relief=SOLID)
        xrefLayerLabel.pack(side="top", anchor="w", fill=X ,pady=1)

        # Second frame elements:
        xrefValueLabel = Label(rightSecondFrame, text="Value", bg="skyblue", borderwidth=1, relief=SOLID)
        xrefValueLabel.pack(side="top", fill=X)
        xrefPathEntry = Entry(rightSecondFrame)
        xrefPathEntry.pack(side="top", fill=X ,pady=2)
        xrefInsertionPointEntry = Entry(rightSecondFrame)
        xrefInsertionPointEntry.pack(side="top", fill=X ,pady=1)
        xrefInsertionPointEntry.insert(0, "0,0,0")
        xrefRotationEntry = Entry(rightSecondFrame)
        xrefRotationEntry.pack(side="top", fill=X ,pady=1)
        xrefRotationEntry.insert(0,"0")
        xrefScaleEntry = Entry(rightSecondFrame)
        xrefScaleEntry.pack(side="top", fill=X ,pady=1)
        xrefScaleEntry.insert(0,"1")
        xrefDraworderEntry = Entry(rightSecondFrame)
        xrefDraworderEntry.pack(side="top", fill=X ,pady=1)
        xrefDraworderEntry.insert(0,"back")
        xrefLayerEntry = Entry(rightSecondFrame)
        xrefLayerEntry.pack(side="top", fill=X ,pady=1)
        xrefLayerEntry.insert(0,"ZZ-Zz9030-M-ExtReferenceInfo")

        # Third frame elements:
        blankLabel = Label(rightThirdFrame, text="",bg="skyblue", borderwidth=1,relief=SOLID)
        blankLabel.pack(side="top", fill=X)
        xrefBrowseBtn = Button(rightThirdFrame, text="Browse", command=lambda x=xrefPathEntry:browseXrefOverLayfile(x))
        xrefBrowseBtn.pack(side="top", fill=X)
        def addThisOverlayToTaskList():
            xrefPath = xrefPathEntry.get()
            layerName = xrefLayerEntry.get()
            draworder = xrefDraworderEntry.get()
            insertionPoint = xrefInsertionPointEntry.get()
            rotation = xrefRotationEntry.get()
            scale = xrefScaleEntry.get()
            if not all([xrefPath, layerName, draworder, insertionPoint, rotation, scale]):
                messagebox.showerror("Invalid input", "All fields are required.")
                return
            listToInject = getLispToOverlayeXref(xrefPath, layerName, draworder)
            self.taskList.append(listToInject)
            print(listToInject)
        addTaskButton = Button(rightThirdFrame, text="Add", command=addThisOverlayToTaskList).pack(side=TOP, fill=BOTH,expand=True)
        # for i in range(5):
        #     Label(rightThirdFrame, text="", bg="skyblue").pack(side="top", fill=BOTH)
        
        
        # Packing the frames side by side
        rightFirstFrame.pack(side="left", anchor="nw", fill=Y)
        rightSecondFrame.pack(side="left", anchor="n", fill=Y)
        rightThirdFrame.pack(side="right", anchor="n",fill=Y)
        
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
