import maya.cmds as cmds
import os
import saveLinks

def start():
    MainUI().baseUI()


def end():
    if cmds.window("window", exists=True):
        cmds.deleteUI("window", window=True)
    if cmds.window("window_1", exists=True):
        cmds.deleteUI("window_1", window=True)


class MainUI:
    def __init__(self):
        self.width = 300
        self.window = "window"
        self.column = "col"

        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        if cmds.windowPref(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)

        self.typeWin = cmds.window(self.window, title="Object Library",
                                   minimizeButton=False, maximizeButton=False, sizeable=False)

        cmds.columnLayout(self.column, parent=self.typeWin)

    def baseUI(self):
        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)], parent=self.column)

        cmds.button(label="See Library", command=lambda args: Library().create())
        cmds.button(label="Load New Objects", command=lambda args: saveLinks.LoadAssets().add())
        cmds.button(label="Save Items Pathways", command=lambda args: saveLinks.SavePaths().saveData())
        cmds.showWindow(self.window)


class Library:
    def __init__(self):
        self.width = 300
        self.window = "window_1"
        self.column = "col_1"

        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        if cmds.windowPref(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)

        self.typeWin = cmds.window(self.window, title="Object Library",
                                   minimizeButton=False, maximizeButton=False, sizeable=False)

        cmds.columnLayout(self.column, parent=self.typeWin)

    def create(self):
        cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, self.width)],
                             parent=self.column)
        existingItemsName = []
        cmds.button(label="CLOSE", command=lambda args: cmds.deleteUI(self.window, window=True))

        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, self.width/2.0), (2, self.width/2.0)],
                             parent=self.column)
        pathways = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pathways.txt")
        self.file = open(pathways, "r")
        Lines = self.file.readlines()
        for line in Lines:
            lineList = line.split(saveLinks.SavePaths.splitKey)
            if lineList[0] not in existingItemsName:
                existingItemsName.append(lineList[0])
                cmds.button(label=lineList[0], command=saveLinks.Callback(saveLinks.loadAsset, lineList[1]))
                cmds.button(label="remove", command=saveLinks.Callback(saveLinks.removeAsset, lineList[0], lineList[1]))
        self.file.close()

        cmds.showWindow(self.window)
