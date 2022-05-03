import maya.OpenMayaMPx as ompx
import sys


PyVersion = sys.version_info[0]
if(PyVersion == 3):
    PySubVersion = sys.version_info[1]
    from importlib import reload
    if PySubVersion == 7:
        try:
            from ..mtor37 import mainwindow as mtor
        except:
            from mtor37 import mainwindow as mtor
    elif PySubVersion == 9:
        try:
            from ..mtor39 import mainwindow as mtor
        except:
            from mtor39 import mainwindow as mtor
else:
    try:
        from ..mtor27 import mainwindow as mtor
    except:
        from mtor27 import mainwindow as mtor

reload(mtor)


def initializePlugin(mobject):
    """
    Entry point for a plugin. It is called once -- immediately after the plugin is loaded.
    This function registers all of the commands, nodes, contexts, etc... associated with the plugin.

    It is required by all plugins.

    :param plugin: MObject used to register the plugin using an MFnPlugin function set
    """
    vendor = "Steven Qiu"
    version = "2.2.3"
    mplugin = ompx.MFnPlugin(mobject, vendor, version)
    mtor.initialize()


def uninitializePlugin(mobject):
    """
    Exit point for a plugin. It is called once -- when the plugin is unloaded.
    This function de-registers everything that was registered in the initializePlugin function.

    It is required by all plugins.

    :param plugin: MObject used to de-register the plugin using an MFnPlugin function set
    """
    mtor.uninitialize()