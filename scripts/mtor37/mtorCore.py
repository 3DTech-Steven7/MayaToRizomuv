# -*- coding: utf-8 -*-
import base64
import os
import shutil
import subprocess
from binascii import b2a_hex, a2b_hex
import time
import maya.OpenMaya as om
import pymel.core as pm
import sys

PyVersion = sys.version_info[0]
if PyVersion == 3:
    import winreg
else:
    import _winreg as winreg


class ApplicationLic(object):

    def __init__(self):
        self.__userName = "mtor#@*tester"  # Key
        self.__passWord = ""  # 自定IV向量
        self.filterNum = self.getCVolumeSerialNumber()
        os.chdir(os.path.dirname(__file__))
        self.licPath = os.path.abspath("..\\..\\config\\mtor.lic")

    def getCVolumeSerialNumber(self):
        CVolumeSerialNumber = os.popen("wmic BaseBoard get SerialNumber").read()
        if(CVolumeSerialNumber):
            CVolumeSerialNumber = CVolumeSerialNumber.split('\r\n')[1]
        else:
            try:
                import win32api
                CVolumeSerialNumber = win32api.GetVolumeInformation("C:\\")[1]
            except:
                CVolumeSerialNumber = None
        if (CVolumeSerialNumber):
            return str(CVolumeSerialNumber)  # number is long type，has to be changed to str for comparing to content after.
        else:
            return 0

    def __set_lic(self):
        EncryptStr = "{0}>>>{1}>>>{2}>>>{3}>>>{4}".format(hex(int(self.filterNum))[2:-1], self.__userName,
                                                          oct(int(self.filterNum))[-1:1:-1],
                                                          bin(int(self.filterNum, 10))[2:-2], self.__passWord)
        print(EncryptStr)
        lic = base64.b64encode(EncryptStr)
        # hqx_lic = b2a_hqx(lic)
        hex_hex = b2a_hex(lic)
        finally_lic = "#".join([str(ord(aci)) for aci in list(hex_hex)])
        finally_lic_bin = "3".join([str(bin(int(aci))) if (aci != "#") else ("#") for aci in list(finally_lic)])
        finally_lic_bin = finally_lic_bin.replace("b", "2").replace("#", "4")
        return finally_lic_bin

    def get_lic(self, lic):
        try:
            finally_lic_bin_list = lic.replace("2", "b").replace("4", "#").split("3")
            finally_lic = "".join([str(int(aci, 2)) if (aci != "#") else ("#") for aci in finally_lic_bin_list])
            hex_hex = "".join([chr(int(aci)) for aci in finally_lic.split("#")])
            hqx_lic = a2b_hex(hex_hex)
            # orgin_lic = a2b_hqx(hqx_lic)
            # orgin_lic = orgin_lic[0] if (len(orgin_lic) > 1) else (orgin_lic)
            lic_id = base64.b64decode(hqx_lic)
            EncryptStr = "{0}>>>{1}>>>{2}>>>{3}>>>{4}".format(hex(int(self.filterNum))[2:-1], self.__userName,
                                                              oct(int(self.filterNum))[-1:1:-1],
                                                              bin(int(self.filterNum, 10))[2:-2], self.__passWord)
            self.__userName = lic_id.split(">>>")[1]
            self.__passWord = lic_id.split(">>>")[-1]
            licIDs = lic_id.split(">>>")[0] + lic_id.split(">>>")[2] + lic_id.split(">>>")[3]
            EncryptStrIDs = EncryptStr.split(">>>")[0] + EncryptStr.split(">>>")[2] + EncryptStr.split(">>>")[3]

            if (licIDs == EncryptStrIDs)or("mtor#@*TesterLove" == self.__userName):
                if ("\x33\x35\x81\xBC\x38\x5A\xE7" == self.__passWord):
                    if (self.__userName == "mtor#@*Steven"):
                        pm.confirmDialog(title='Registered Successfully',
                                         message='You are the administrator, welcome back!', button=['Ok'])

                    elif ("mtor#@*TesterLove" == self.__userName):
                        pm.confirmDialog(title='Registered Successfully',
                                         message='Love live!Thank you for participating in the plugin testing!', button=['Ok'])

                    elif ("mtor#@*" in self.__userName):
                        pm.confirmDialog(title='Registered Successfully',
                                         message='Thank you for participating in the plugin testing!', button=['Ok'])
                    return True
        except:
            return False

        return False

    def export_lic(self, lic):
        with open(self.licPath, "wb+") as f:
            f.writelines(lic)
        print("Successfuly Export!")

    def import_lic(self, path):
        if (os.path.isfile(path)):
            with open(path, "rb") as f:
                licContent = f.readline()
            if (self.get_lic(licContent)):
                print("Successfuly Import!")
                return True

        print("Fail Import!")
        return False


class MtorRef(object):
    def __init__(self):
        cache_file = "%s\\%s" % (os.getenv('TEMP'), "rezomuv.fbx")
        self.cache_file = cache_file.replace("\\", "/").replace("//", "/")
        self.prefix = "MTOR"
        self.ref_mtor = None

        # self.scence_init()
        # self.set_reference()

    def scence_init(self):
        # baseDir = os.path.abspath(os.path.dirname(__file__))
        # local_filePath = '%s\\resource\\test.fbx'%("\\".join(baseDir.split("\\")[:-2]))
        os.chdir(os.path.dirname(__file__))
        local_filePath = os.path.abspath("..\\..\\resource\\test.fbx")
        shutil.copy2(local_filePath, self.cache_file)
        print("init")
        cmd = 'file -r -type "FBX"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "{0}" "{1}";'.format(
            self.prefix, self.cache_file)
        # pm.mel.eval(cmd)
        om.MGlobal().executeCommand('optionVar -iv "FileDialogStyle" 2;')
        om.MGlobal().executeCommand(cmd)
        print(cmd)

    def set_reference(self):
        for ref_mtor in pm.ls(typ="reference"):
            if (ref_mtor.referenceFile()):
                if (ref_mtor.referenceFile().path == self.cache_file):
                    self.ref_mtor = ref_mtor
                    for obj in self.ref_mtor.referenceFile().nodes():
                        try:
                            obj.visibility.set(0)
                            obj.useOutlinerColor.set(1)
                            obj.outlinerColor.set([0.59, 0.59, 0.59])
                            obj.hiddenInOutliner.set(1)
                            obj.hideOnPlayback.set(1)
                        except:
                            pass

        if int(pm.mel.eval('exists AEdagNodeCommonRefreshOutliners')) == 1:
            # pm.mel.eval('AEdagNodeCommonRefreshOutliners()')
            # if int(om.MGlobal().executeCommand('exists AEdagNodeCommonRefreshOutliners')) == 1:
            om.MGlobal().executeCommand('AEdagNodeCommonRefreshOutliners()')
        else:
            pass

    def reload_reference(self):
        for ref_mtor in pm.ls(typ="reference"):
            if (ref_mtor.referenceFile()):
                if (ref_mtor.referenceFile().path == self.cache_file):
                    # print("load")
                    # self.ref_mtor.load()
                    ref_mtor.referenceFile().load()
                    for obj in ref_mtor.referenceFile().nodes():
                        try:
                            obj.visibility.set(0)
                            obj.useOutlinerColor.set(1)
                            obj.outlinerColor.set([0.59, 0.59, 0.59])
                            obj.hiddenInOutliner.set(1)
                            obj.hideOnPlayback.set(1)

                        except:
                            pass
        if int(pm.mel.eval('exists AEdagNodeCommonRefreshOutliners')) == 1:
            #     pm.mel.eval('AEdagNodeCommonRefreshOutliners()')
            # if int(om.MGlobal().executeCommand('exists AEdagNodeCommonRefreshOutliners')) == 1:
            om.MGlobal().executeCommand('AEdagNodeCommonRefreshOutliners()')
        else:
            pass

    def del_reference(self, all=True):
        for ref_mtor in pm.ls(typ="reference"):
            if ref_mtor and ref_mtor.referenceFile():
                if ref_mtor.referenceFile().path == self.cache_file:
                    if not all and ref_mtor.referenceFile() == self.ref_mtor.referenceFile():
                        continue
                    ref_mtor.referenceFile().remove()

class MtorLink(object):
    def __init__(self, RizomPath):
        # TEMP FILE
        cache_file = "%s\\%s" % (os.getenv('TEMP'), "rezomuv.fbx")
        lua_path = "%s\\%s" % (os.getenv('TEMP'), "rezomuv_lua_script.lua")
        self.cache_file = cache_file.replace("\\", "/").replace("//", "/")
        self.lua_path = lua_path.replace("\\", "/").replace("//", "/")
        self.mtor_lastselection = None
        self.prefix = "MTOR"
        self.ref_object = None

        # Rizom Exe
        self.RizomPath = RizomPath

    def set_ref(self, ref):
        self.ref_object = ref

    def init_lua(self):
        # pm.system.displayInfo(self.lua_path)
        with open(self.lua_path, "w+") as f:
            f.write("print(\"Successful To Link.\")")

    def get_selected_object(self):
        # * Get Object
        select_file = pm.ls(sl=True, tr=True)
        mesh_list = [f for f in select_file if (pm.ls(f, typ="mesh", dag=True))]
        return mesh_list

    def export_selected_object(self, mesh_list=None):
        # * Export Object
        if (mesh_list):
            pm.select(mesh_list)
        # print("Load")
        # pm.mel.eval('file - force - options "" - typ "FBX export" - pr - es"{0}";'.format(self.cache_file))
        om.MGlobal().executeCommand('optionVar -iv "FileDialogStyle" 2;')
        om.MGlobal().executeCommand(
            'file - force - options "" - typ "FBX export" - pr - es"{0}";'.format(self.cache_file))

        # pm.file({0}, f=True, typ="FBX export", pr=True, ea=True).format(self.cache_file)
        # try:
        #     pm.file({0}, f=True, typ="FBX export", pr=True, ea=True).format(self.cache_file)
        # except:
        #     pm.mel.eval('file - force - options "" - typ "FBX export" - pr - es"{0}";'.format(self.cache_file))
        # pm.exportSelected(self.cache_file, f=True)

    def set_link(self):
        # Popen exe
        cmd = "\"{0}\" /cfi \"{1}\"".format(self.RizomPath, self.lua_path)
        self.rizom_pipe = subprocess.Popen(cmd)

    def get_overfile(self, oldCmd=False):
        # Import file
        prefix = self.prefix

        if(oldCmd):
            pm.system.importFile(self.cache_file, defaultNamespace=False, renamingPrefix="mtor")
            pull_list = pm.ls("%s*:*" % prefix, tr=True)

            for obj in pull_list:
                orgin_obj = obj.longName().replace("MTOR1:", "").replace("MTOR:", "")
                orgin_obj_list = pm.ls(orgin_obj, dag=True, typ="mesh")
                for orgin in orgin_obj_list:
                    if (orgin_obj == orgin.getTransform()):
                        pm.polyTransfer(orgin_obj, ao=obj)
                        # pm.transferAttributes(obj, orgin_obj, transferPositions=0,
                        #                       transferNormals=0, transferUVs=2, sampleSpace=4)
                        pm.delete(orgin, ch=True)
            return 0

        if (self.mtor_lastselection):
            # print(self.last_selection)
            select_list = self.last_selection
        else:
            select_list = pm.ls(sl=True, tr=True)

        if (not self.ref_object.ref_mtor.objExists()):
            self.ref_object.scence_init()
            self.ref_object.set_reference()

        self.ref_object.reload_reference()
        # pm.system.importFile(self.cache_file, defaultNamespace=False, renamingPrefix="mtor")

        # pull_list = pm.ls("%s*:*" % prefix, tr=True)
        # print(self.ref_object)
        pull_list = [obj for obj in self.ref_object.ref_mtor.referenceFile().nodes() if obj.type() == "transform"]
        for obj in pull_list:
            #om.MGlobal.displayInfo("objjjjjj:%s" % obj)
            orgin_obj = obj.longName().replace("MTOR1:", "").replace("MTOR:", "")
            orgin_obj_list = pm.ls(orgin_obj, dag=True, typ="mesh")
            for orgin in orgin_obj_list:
                if (orgin_obj == orgin.getTransform()):
                    refConnectionInstance = RefConnection(orgin, obj)
                    refConnectionInstance.Proc(delNode=True)
                    # pm.delete(orgin, ch=True)
        pm.select(select_list)
        self.last_selection = None
        # pm.delte(obj)

    def save_script(self):
        lua_script = "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file
        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def load_script(self, post_save=False):
        lua_script = "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file
        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file
        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def quit_script(self):
        # lua_script = "ZomQuit()"
        # with open(self.lua_path, "w+") as f:
        #     f.write(lua_script)
        self.rizom_pipe.kill()

    def autoCut_script(self, selectMode=False, pre_load=False, post_save=False):
        lua_script = ''
        if (pre_load):
            lua_script += "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file
        selection = "&Selected" if (selectMode) else ("")
        lua_script += 'ZomSelect({\
        PrimType = "Edge", WorkingSet = "Visible%s", Select = true, ResetBefore = true, ProtectMapName = "Protect", FilterIslandVisible = true, Auto = {\
        QuasiDevelopable = { Developability = 0.5, IslandPolyNBMin = 1, FitCones = false, Straighten = true}, \
        HandleCutter = true, QuadLoopCutter = true, StoreCoordsUVW = true, FlatteningMode = 0, FlatteningUnfoldParams = {\
        BorderIntersections = true, TriangleFlips = true}}});'%(selection)
        lua_script+= 'ZomCut({PrimType = "Edge", WorkingSet = "Visible"});'

        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def autoUnfold_script(self, selectMode=False, pre_load=False, post_save=False):
        lua_script = ''
        if (pre_load):
            lua_script += "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file
        selection= "&Selected" if(selectMode) else("")
        lua_script += 'ZomPack({ RootGroup = "RootGroup", WorkingSet = "Visible%s", ProcessTileSelection = false, RecursionDepth = 1, Translate = true, LayoutScalingMode = 2, Scaling = { Mode = 2}})'%(selection)

        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def autoLayout_script(self, selectMode=False, pre_load=False, post_save=False):
        lua_script = ''
        if (pre_load):
            lua_script += "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file
        selection= "&Selected" if(selectMode) else("")
        lua_script += 'ZomPack({RootGroup="RootGroup", WorkingSet="Visible%s", ProcessTileSelection=false, RecursionDepth=1, Translate=true, LayoutScalingMode=2, Scaling={Mode=2}})'%(selection)

        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def autoOptimize_script(self, selectMode=False, pre_load=False, post_save=False):
        lua_script = ''
        if (pre_load):
            lua_script += "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file
        selection= "&Selected" if(selectMode) else("")
        lua_script += 'ZomOptimize({PrimType="Island", WorkingSet="Visible%s", Mix=1, AngleDistanceMix=1, RoomSpace=0, MinAngle=1e-05, ProcessSelection=true, PinMapName="Pin", Iterations=3})'%(selection)

        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def autoAlign_script(self, selectMode=False, pre_load=False, post_save=False):
        lua_script = ''
        if (pre_load):
            lua_script += "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file
        selection= "&Selected" if(selectMode) else("")
        lua_script += 'ZomDeform({WorkingSet="Visible%s", PrimType="Island", Geometrical="AlignLeft"})'%(selection)

        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def autoStack_script(self, selectMode=False, pre_load=False, post_save=False):
        lua_script = ''
        if (pre_load):
            lua_script += "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file
        selection= "&Selected" if(selectMode) else("")
        lua_script += 'ZomIslandCopy({WorkingSet="Visible%s", Mode="CopyCoordinates", Orientation="Straight", AreaThreshold=0.01, ReferenceIslandIDs={ 5}})'%(selection)

        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def autoStaighten_script(self, selectMode=False, pre_load=False, post_save=False):
        lua_script = ''
        if (pre_load):
            lua_script += "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file

        selection = "&Selected" if (selectMode) else ("")
        lua_script += 'ZomDeform({WorkingSet="Visible%s", PrimType="Island", Geometrical="Horizontalize"})'%(selection)

        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def autoLightmap_script(self, pre_load=False, post_save=False):
        lua_script = ''
        if (pre_load):
            lua_script += "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file

        lua_script += 'ZomUvset({Mode = "Create", Name = "lightmap"});\
        ZomUvset({Mode = "SetCurrent", Name = "lightmap"});\
        ZomSelect({PrimType="Edge", WorkingSet="Visible", Select=true, ResetBefore=true, ProtectMapName="Protect", FilterIslandVisible=true, Auto={Skeleton={Open=true}, HandleCutter=true, QuadLoopCutter=true, StoreCoordsUVW=true, FlatteningMode=0, FlatteningUnfoldParams={BorderIntersections=true, TriangleFlips=true}}});\
        ZomCut({PrimType="Edge", WorkingSet="Visible"});\
        ZomLoad({Data={CoordsUVWInternalPath="#Mesh.Tmp.AutoSelect.UVW "}});\
        ZomIslandGroups({Mode="DistributeInTilesByBBox", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE"});\
        ZomIslandGroups({Mode="DistributeInTilesEvenly", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", UseTileLocks=true, UseIslandLocks=true});\
        ZomPack({RootGroup="RootGroup", WorkingSet="Visible", ProcessTileSelection=false, RecursionDepth=1, Translate=true, LayoutScalingMode=2, Scaling={Mode=2}});'

        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        with open(self.lua_path, "w+") as f:
            f.write(lua_script)

    def fullAuto_script(self, pre_load=False, pre_save=False, post_save=False):
        lua_script = ''
        if (pre_load):
            lua_script += "ZomLoad({File={Path=\"%s\", ImportGroups=true, XYZUVW=true, UVWProps=true}, __Focus=true});" % self.cache_file
        if (pre_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        lua_script += '\
        ZomSet({Path="Prefs.UI.Display.PackLayout", Value=false});\
        ZomSelect({PrimType="Edge", WorkingSet="Visible", Select=true, ResetBefore=true, ProtectMapName="Protect", FilterIslandVisible=true, Auto={Skeleton={Open=true}, HandleCutter=true, QuadLoopCutter=true, StoreCoordsUVW=true, FlatteningMode=0, FlatteningUnfoldParams={BorderIntersections=true, TriangleFlips=true}}});\
        ZomCut({PrimType="Edge", WorkingSet="Visible"});\
        ZomLoad({Data={CoordsUVWInternalPath="#Mesh.Tmp.AutoSelect.UVW "}});\
        ZomIslandGroups({Mode="DistributeInTilesByBBox", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE"});\
        ZomIslandGroups({Mode="DistributeInTilesEvenly", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", UseTileLocks=true, UseIslandLocks=true});\
        ZomPack({RootGroup="RootGroup", WorkingSet="Visible", ProcessTileSelection=false, RecursionDepth=1, Translate=true, LayoutScalingMode=2, Scaling={Mode=2}});'

        if (post_save):
            lua_script += "ZomSave({File={Path=\"%s\", UVWProps=true}, __Focus=true});" % self.cache_file

        with open(self.lua_path, "w+") as f:
            f.write(lua_script)


class Selection_Similar(object):
    def __init__(self):
        self.selection_length = 0
        self.similar_list = []
        self.sel_mesh = None

    def get_selection_simliar_data(self):
        selection_list = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection_list)
        Mselection_list = om.MItSelectionList(selection_list)
        self.selection_length = selection_list.length()
        if (self.selection_length > 0):
            mfn_mesh = None
            while not Mselection_list.isDone():
                mfn_mesh = om.MDagPath()
                Mselection_list.getDagPath(mfn_mesh)
                Mselection_list.next()

            MItDag_iterator = om.MItDag()
            MItDag_iterator.reset(mfn_mesh, om.MItDag.kDepthFirst, om.MFn.kMesh)
            all_mesh_data = {}
            while not MItDag_iterator.isDone():
                self.sel_mesh = om.MFnMesh(MItDag_iterator.item())
                all_mesh_data[self.sel_mesh] = ",".join(
                    [str(self.sel_mesh.numFaceVertices()), str(self.sel_mesh.numVertices()),
                     str(self.sel_mesh.numPolygons())])

                MItDag_iterator.next()

            self.similar_list = []
            MItDependencyNodes_iterator = om.MItDependencyNodes(om.MFn.kMesh)
            while not MItDependencyNodes_iterator.isDone():

                fn_mesh = om.MFnMesh(MItDependencyNodes_iterator.item())
                all_mesh_data[fn_mesh] = ",".join(
                    [str(fn_mesh.numFaceVertices()), str(fn_mesh.numVertices()), str(fn_mesh.numPolygons())])
                if (all_mesh_data[self.sel_mesh] == all_mesh_data[fn_mesh]):
                    self.similar_list.append(fn_mesh)
                MItDependencyNodes_iterator.next()

    def set_selection_simliar_list(self):
        # selection simliar
        if ((self.similar_list) and (self.selection_length > 0)):
            selection_similar_list = om.MSelectionList()
            for obj in self.similar_list:
                mDagNode = om.MFnDagNode(obj.object())
                mDagNode_parent = om.MFnDagNode(mDagNode.parent(0))
                mdag = om.MDagPath()
                mDagNode_parent.getPath(mdag)
                selection_similar_list.add(mdag)
            om.MGlobal.setActiveSelectionList(selection_similar_list)

    def set_selection_simliar_uv(self, state):
        if (state):
            sel_obj = pm.PyNode(self.sel_mesh.fullPathName())
            for obj in self.similar_list:
                if (obj.fullPathName() != self.sel_mesh.fullPathName()):
                    similar_obj = pm.PyNode(obj.fullPathName())
                    pm.polyTransfer(similar_obj, ao=sel_obj)
                    pm.delete([sel_obj, similar_obj], ch=True)

        else:
            selection_list = pm.ls(sl=True, dag=True, typ="mesh")
            for obj in selection_list:
                if (obj != selection_list[0]):
                    pm.polyTransfer(obj, ao=selection_list[0])
                    pm.delete([selection_list[0], obj], ch=True)


class Selection_Edge(object):
    def __init__(self):
        pass

    def getAllSel(self):
        sel = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(sel)
        names = []
        sel.getSelectionStrings(names)
        ss = pm.ls(names, fl=1)
        return ss

    def getSandT(self, type="t"):
        outVal = ""
        try:
            "s for shape and t for Transform"
            selection = om.MSelectionList()
            om.MGlobal.getActiveSelectionList(selection)
            selection_iter = om.MItSelectionList(selection)
            obj = om.MObject()

            while not selection_iter.isDone():
                selection_iter.getDependNode(obj)
                dagPath = om.MDagPath.getAPathTo(obj)
                dagName = str(dagPath.fullPathName())
                if len(dagName.split("|")) > 2:
                    if type == "s":
                        outVal = dagName.split("|")[-1]
                    elif type == "t":
                        outVal = dagName.split("|")[-2]
                else:
                    outVal = dagName.split("|")[-1]
                selection_iter.next()
        except:
            pass
        return outVal

    def edgeMode(self):
        sel = self.getSandT("t")
        if sel == "": return
        om.MGlobal.executeCommand('resetPolySelectConstraint;')
        om.MGlobal.executeCommand('doMenuComponentSelection("' + sel + '", "edge");')

    def hardEdge(self):
        sel = self.getAllSel()
        if sel == []:
            om.MGlobal.displayWarning("Select something!")
            return 0
        sel = sel[0].split(".")[0]
        pm.select(sel + ".e[0]", r=1)
        self.edgeMode()
        om.MGlobal.executeCommand('polySelectConstraint -mode 3 -type 0x8000 -sm 1;resetPolySelectConstraint;')
        self.getAllSel()

    def uvEdge(self):
        sel = self.getAllSel()
        if sel == []:
            om.MGlobal.displayWarning("Select something!")
            return 0
        sel = sel[0].split(".")[0]
        pm.select(sel + ".e[0]", r=1)
        self.edgeMode()

        # Select the borders
        temp = pm.ls(sel + ".map[*]")

        pm.select(temp)
        om.MGlobal.executeCommand('polySelectBorderShell 1;')
        om.MGlobal.executeCommand('PolySelectConvert 20;')
        pEdge = self.getAllSel()

        edgeDeselect = []
        for edg in pEdge:
            uvs = pm.ls(pm.polyListComponentConversion(edg, tuv=1), fl=1)
            if len(uvs) <= 2:
                edgeDeselect.append(edg)

        pm.select(edgeDeselect, d=1)
        self.edgeMode()


class RefConnection(object):
    def __init__(self, origin, target):
        self.origin = origin
        self.target = target
        # om.MGlobal.displayInfo("origin: %s" % origin)
        # om.MGlobal.displayInfo("target: %s" % target)

    def Proc(self, delNode=False):
        originDagNode = self.origin.__apiobject__()
        originMesh_fn = om.MFnDagNode(originDagNode)
        # originTransform_fn = om.MFnDagNode(originDagNode)
        # if(not originTransform_fn.inModel()):return
        # if(originTransform_fn.childCount()==0):return

        # originShape = originTransform_fn.child(0)
        # originMesh_fn = om.MFnDagNode(originShape)

        targeDagNode = self.target.__apiobject__()
        targetTransform_fn = om.MFnDagNode(targeDagNode)
        if (not targetTransform_fn.inModel()): return
        if (targetTransform_fn.childCount() == 0): return

        targetShape = targetTransform_fn.child(0)
        targetMesh_fn = om.MFnDagNode(targetShape)

        # Find Mesh node's inMesh plug
        origin_plug = originMesh_fn.findPlug("inMesh", False)

        # Find Sphere node's output plug
        target_plug = targetMesh_fn.findPlug("outMesh", False)

        # om.MGlobal.displayInfo("origin_plug: %s" % origin_plug.name())
        # om.MGlobal.displayInfo("target_plug: %s" % target_plug.name())
        if (origin_plug.isConnected()):
            origin_plug_source = origin_plug.source()

            if (target_plug != origin_plug_source):
                dg_mod = om.MDGModifier()
                dg_mod.disconnect(origin_plug_source, origin_plug)
                dg_mod.doIt()
                if (delNode):
                    dg_mod.deleteNode(origin_plug_source.node())
            else:
                return

        # Connect PolySphere node's output to Mesh node's input
        dg_mod = om.MDGModifier()
        dg_mod.connect(target_plug, origin_plug)
        dg_mod.doIt()


class SwitchObjcet(object):
    def __init__(self):
        self.mtor = None
        self.run_state = False
        self.importThread = None
        self.importFuction = None
        self.last_selection = None
        # self.last_pm_selection = None

    def set_mtor(self, mtor_exe):
        self.mtor = mtor_exe

    def set_importThread(self, importThread):
        self.importThread = importThread

    def set_importFuction(self, importFuction):
        self.importFuction = importFuction

    def startTestCallBack(self, *args):
        if not self.mtor:
            return 

        selection_list = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection_list)
        Mselection_list = om.MItSelectionList(selection_list)
        # Mselection_list.setFilter(om.MFn.kTransform)
        mesh_group = self.list_selection(Mselection_list)
        self.state = False
        if mesh_group:
            if self.last_selection:
                if mesh_group != self.last_selection:
                    self.state = True
                    # for key in mesh_group[0].keys():
                    #     for last_key in self.last_selection[0].keys():
                    #         # if (key == last_key):
                    #         #     self.state = False
                    #         # else:
                    #         #     self.state = True
                    #         if (key != last_key):
                    #             self.state = True
                else:
                    return
            else:
                self.state = True

            self.last_selection = mesh_group
            # print(self.state, mesh_group, self.last_selection)
            if self.state:
                self.importThread.stop()
                self.mtor.export_selected_object()
                self.mtor.load_script()
                self.importThread.last_time = 0
                self.importFuction()
                self.state = False

            # self.last_pm_selection = pm.ls(sl=True, tr=True)
        # except Exception as e:
        #     print("Error %s" % e)

    def startCallBack(self):
        self.Call = om.MEventMessage.addEventCallback("SelectionChanged", self.startTestCallBack)

    def removeCallBack(self):
        om.MMessage.removeCallback(self.Call)

    def list_selection(self, Mselection_list):
        check_group = []
        while not Mselection_list.isDone():
            if (Mselection_list.itemType() == 0):
                dag_path = om.MDagPath()
                Mselection_list.getDagPath(dag_path)

                if (dag_path.childCount() > 0):
                    dag_path_name = self.obj_count(dag_path)
                    if dag_path_name:
                        check_group.append(dag_path_name)
                    # check_group.append(self.obj_count(dag_path))
                    # print "name:%s" % dag_path.partialPathName()
                    # print obj_count(dag_path)

                    # if dag_path.node().apiTypeStr() == 'kTransform':
                    #     newsel.add(dag_path)

                # print(check_group)
            Mselection_list.next()
        return check_group

    def obj_count(self, root):
        '''
        :param root: om.MDagpath
        :return: dict
        '''
        polyattr_list = None
        iterator = om.MItDag()
        iterator.reset(root, om.MItDag.kDepthFirst, om.MFn.kTransform)
        while not iterator.isDone():
            mdag_path = om.MDagPath()
            iterator.getPath(mdag_path)
            if (mdag_path.child(0).apiTypeStr() == 'kMesh'):
                return root.fullPathName()
                # item_name = root
                # child_item = om.MFnMesh(mdag_path.child(0))
                # item_list = [child_item.numFaceVertices(), child_item.numVertices()]
                # polyattr_list[item_name] = item_list
            iterator.next()

        return polyattr_list


class GetPathKey(object):
    @classmethod
    def subkeys(self, key):
        i = 0
        while True:
            try:
                subkey = winreg.EnumKey(key, i)
                yield subkey
                i += 1

            except WindowsError as e:
                break

    @classmethod
    def get_all_rizom_path(self):
        rizom_key = "SOFTWARE\\Rizom Lab"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rizom_key)

        for i in self.subkeys(key):
            rizomuv_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "{0}\\{1}\\rizomuv.exe".format(rizom_key, i))
            try:
                rizomuv_path, _ = winreg.QueryValueEx(rizomuv_key, "")
                return rizomuv_path
            except FileNotFoundError as e:
                continue
        return None


def open_link(rezomuv_path):
    mtor = MtorLink(rezomuv_path)
    mesh_list = mtor.get_selected_object()
    if (mesh_list == 0):
        raise EOFError
        om.MGlobal.displayError("list zero")
    mtor.export_selected_object(mesh_list)
    mtor.load_script()
    mtor.set_link()


if (__name__ == "__main__"):
    rezomuv_path = r"C:\Program Files\Rizom Lab\RizomUV 2020\rizomuv_virtual.exe"
    open_link(rezomuv_path)
    ##########
    import mtor.mtorCore as mtr

    reload(mtr)

    appLic = mtr.ApplicationLic()
    lic = appLic._ApplicationLic__set_lic()
    path = r"D:\GitHub\My_Git_Test.git\trunk\Code\MayaToRizomUV\config\mtor.lic"
    appLic.import_lic(path)

    appLic._ApplicationLic__userName = "mtor#@*TesterLove"
    appLic._ApplicationLic__passWord = "\x33\x35\x81\xBC\x38\x5A\xE7"

    lic = appLic._ApplicationLic__set_lic()
    appLic.export_lic(lic)
    appLic.import_lic(path)
    # appLic.get_lic(lic)
