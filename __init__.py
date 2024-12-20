bl_info = {
    "name": "Utility Tools",
    "author": "Amogh Agrawal",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > Utility Tools",
    "description": "Adds various helpful tools to Blender to make your workflow easier.",
    "doc_url": "",
    "tracker_url": "",
    "warning": "",
    "category": "3D View",
}

import bpy
from . import main_script 

def register():
    main_script.register()

def unregister():
    main_script.unregister()

if __name__ == "__main__":
    register()