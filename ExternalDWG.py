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
class ExternalDWG:
    def __init__(self, root):
        self.root = root
        self.selected_files=[]
        self.toworkonfiles=set()
        self.root.title("External DWG")
        self.root.geometry("600x300")
        # self.root.maxsize(600,300)
        # self.root.resizable(False, False)
        self.leftMainFrame = Frame(self.root, width=200, bg='lightgrey')
        load_Drawing_btn = Button(self.leftMainFrame, text="Load Drawings", command=self.onLoadDrawing) #command=self.setup_drawing_window
        load_Drawing_btn.pack(side="top", padx=10, pady=10)
        self.leftMainFrame.pack(side='left', fill='y')
        self.rightFrame = Frame(self.root)
        self.rightFrame.pack(fill=BOTH, expand=True)
    def onLoadDrawing(self):
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
        self.check_vars = []
        for index, file in enumerate(self.selected_files):
            if file in self.toworkonfiles:
                var = IntVar(value=1)
            else:
                var = IntVar(value=0)
            self.check_vars.append(var)
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
        if self.check_vars[index].get() == 1:
            if self.selected_files[index] not in self.toworkonfiles:
                self.toworkonfiles.add(self.selected_files[index])
        else:
            if self.selected_files[index] in self.toworkonfiles:
                self.toworkonfiles.remove(self.selected_files[index])
    def removeSelectedFiles(self):
        try:
            for files in self.toworkonfiles:
                self.selected_files.remove(str(files))
        except Exception as e:
            pass
        self.onLoadDrawing()
    def addFiles(self):
        getFilesVar = filedialog.askopenfilenames(title="Select Target Drawing Files", filetypes=[("DWG files", "*.dwg")])
        if getFilesVar is not None:
            for file in getFilesVar:
                self.selected_files.append(file)
                self.toworkonfiles.add(file)
            self.onLoadDrawing()
            return
        messagebox.showinfo("No files selected", "Please select drawing file(s) to proceed.")
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
        AcadVersions.add(versionNumber)
print(versions)
print(f"C3D versions: {C3DVersions}")
print(f"Acad versions: {AcadVersions}")
externalDWG = ExternalDWG(root)
root.mainloop()
