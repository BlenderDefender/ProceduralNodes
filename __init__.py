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

bl_info = {
    "name": "Procedural Nodes",
    "description": "Useful and cool node groups",
    "author": "Blender Defender",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Node Editors > Add > Procedural Nodes",
    "description": "Add pre-made node groups to the node editors",
    "warning": "Check Out Gumroad for extension packs and more",
    "doc_url": "",
    "category": "Node",
}


def menu_func(self, context):
    self.layout.menu(
        "PROCEDURALNODES_MT_main_menu",
        text="Procedural Nodes",
        icon='PRESET_NEW',
    )


def register():
    menus.register()
    prefs.register()
    bpy.types.NODE_MT_add.append(menu_func)


def unregister():
    menus.unregister()
    prefs.unregister()
    bpy.types.NODE_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
