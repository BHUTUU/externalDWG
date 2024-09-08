import os
def getLispTorepathAndRenameXref(targetXref, newXrefPath):
    baselispforinjection=f'''
    (if (tblsearch "block" "{targetXref}")
    (COMMAND "-xref" "P" "{targetXref}" "{newXrefPath}" "-RENAME" "b" "{targetXref}" "{os.path.basename(newXrefPath)}" )
    (princ "\\n{targetXref} not found. ")
    )'''
    return baselispforinjection
