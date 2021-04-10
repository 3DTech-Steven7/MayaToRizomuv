import maya.OpenMayaMPx as ompx
import sys

PyVersion = sys.version_info[0]
if(PyVersion == 3):
    from importlib import reload
    try:
        from ..mtor3 import mainwindow as mtor
    except:
        from mtor3 import mainwindow as mtor
else:
    try:
        from ..mtor2 import mainwindow as mtor
    except:
        from mtor2 import mainwindow as mtor

reload(mtor)


def initializePlugin(mobject):
    """
    Entry point for a plugin. It is called once -- immediately after the plugin is loaded.
    This function registers all of the commands, nodes, contexts, etc... associated with the plugin.

    It is required by all plugins.

    :param plugin: MObject used to register the plugin using an MFnPlugin function set
    """
    vendor = "Steven Qiu"
    version = "2021.4.10.02"
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