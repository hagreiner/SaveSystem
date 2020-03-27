import os
import maya.cmds as cmds
import main


class LoadAssets:
    sessionPaths = {}

    def __init__(self):
        self.fileFilter = "OBJ Files (*.obj);;FBX Files (*.fbx);;Maya Files (*.ma *.mb);;"
        self.loadSessionPaths = cmds.fileDialog2(dialogStyle=1, fileMode=4, cap="RTB: Load Skeleton Registration",
                                                 ff=self.fileFilter)

    def add(self):
        if self.loadSessionPaths is None:
            return None
        for path in self.loadSessionPaths:
            tempName = os.path.basename(path)
            objName = tempName.split(".")[0]
            LoadAssets.sessionPaths[objName] = path


class SavePaths:
    splitKey = "#.#.#"

    def __init__(self):
        self.pathways = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pathways.txt")

    def saveData(self):
        file = open(self.pathways, "a")
        for name, path in LoadAssets.sessionPaths.items():
            file.write(name + SavePaths.splitKey + path)
            file.write("\n")
        file.close()

    def removeData(self, name, path):
        with open(self.pathways, "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                if i != (name + SavePaths.splitKey + path):
                    f.write(i)
            f.truncate()


def loadAsset(path):
    LockedObject().add()
    cmds.file(path, i=True, ra=True)
    # if LockedObject.item != "":
    #     MoveObject(cmds.ls(sl=True), LockedObject.item).move()


def removeAsset(name, path):
    try:
        del LoadAssets.sessionPaths[name]
    except:
        pass
    SavePaths().removeData(name, path)
    main.Library().create()


def saveAsset(name, path):
    type = path.split(".")[-1]
    cmds.file(rename=name + "." + type)
    cmds.file(path, type="mayaBinary", exportSelected=True)


class Callback(object):
    def __init__(self, func, *args, **kwargs):
        self.args = args
        self.func = func
        self.kwargs = kwargs
    def __call__(self, *args, **kwargs):
        return self.func(*self.args, **self.kwargs)


class LockedObject:
    item = ""
    def add(self):
        LockedObject.item = cmds.ls(sl=True)


class MoveObject:
    def __init__(self, object, location):
        cmds.select(location)
        loc_xmin, loc_ymin, loc_zmin, loc_xmax, loc_ymax, loc_zmax = cmds.xform(bb=True, query=True)
        self.object = object

        self.pos_loc = [(loc_xmin + loc_xmax)/2.0, (loc_ymin + loc_ymax)/2.0, (loc_zmin + loc_zmax)/2.0]

    def move(self):
        cmds.move(self.pos_loc[0], self.pos_loc[1], self.pos_loc[2], self.object)
