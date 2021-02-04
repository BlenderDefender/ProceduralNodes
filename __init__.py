# ##### BEGIN GPL LICENSE BLOCK #####
#
#  Copyright (C) <2020>  <Blender Defender>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 3
#  of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

from . import (
    menus,
    prefs,
)

from .functions.blenderdefender_functions import setup_addons_data, decode
from .functions.dict.dict import decoding


bl_info = {
    "name": "Procedural Nodes",
    "description": "Useful and cool node groups",
    "author": "Blender Defender",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "Node Editors > Add > Procedural Nodes",
    "description": "Add pre-made node groups to the node editors",
    "warning": "Check Out Gumroad for extension packs and more",
    "tracker_url": "https://github.com/BlenderDefender/ProceduralNodes/issues",
    "category": "Node",
}


def menu_func(self, context):
    self.layout.menu(
        "PROCEDURALNODES_MT_main_menu",
        text="Procedural Nodes",
        icon='PRESET_NEW',
    )


def register():
    import os
    import shutil
    path = os.path.join(os.path.expanduser(
        "~"), "Blender Addons Data", "procedural-nodes")
    if not os.path.isdir(path):
        os.makedirs(path)
    shutil.copyfile(os.path.join(list(os.path.split(os.path.abspath(__file__)))[0],
                                 "functions",
                                 "data.blenderdefender"),
                    os.path.join(os.path.expanduser("~"),
                                 "Blender Addons Data",
                                 "procedural-nodes",
                                 "data.blenderdefender"))
    shutil.copyfile(os.path.join(os.path.join(
                                 os.path.dirname(os.path.abspath(__file__)),
                                 'functions',
                                 'data',
                                 'Procedural Nodes Basics.blend')),
                    os.path.join(os.path.expanduser("~"),
                                 "Blender Addons Data",
                                 "procedural-nodes",
                                 "Procedural Nodes Basics.blend"))

    data = decode(os.path.join(os.path.expanduser("~"),
                               "Blender Addons Data",
                               "procedural-nodes",
                               "data.blenderdefender"),
                  decoding)
    setup_addons_data(data[1])

    menus.register()
    prefs.register(bl_info)
    bpy.types.NODE_MT_add.append(menu_func)


def unregister():
    menus.unregister()
    prefs.unregister()
    bpy.types.NODE_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
