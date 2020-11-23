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


# -----------------------------------------------------------------------------
import os
from os.path import expanduser

import shutil
import platform

# -----------------------------------------------------------------------------
import bpy
from bpy.types import (
    Operator,
    Menu,
    AddonPreferences,
)
from bpy.props import (
    StringProperty,
    BoolProperty,
)

from bpy_extras.io_utils import ImportHelper
# -----------------------------------------------------------------------------
from . import (
    addon_updater_ops,
    menus,
    operators,
)

from .functions.main_functions import (
    node_center,
    node_path,
    node_template_add,
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


# -----------------------------------------------------------------------------
# Addon Preferences
class PROCEDURALNODES_APT_preferences(AddonPreferences):  # Procedural Nodes
    bl_idname = __package__

    # addon updater preferences

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
    )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        layout = self.layout
        mainrow = layout.row()
        col = mainrow.column()
        layout.operator("proceduralnodes.check_gumroad", icon='FUND')

        addon_updater_ops.update_settings_ui(self, context)

        layout.operator("proceduralnodes.install_file")


def menu_func(self, context):
    self.layout.menu(
        "PROCEDURALNODES_MT_main_menu",
        text="Procedural Nodes",
        icon='PRESET_NEW',
    )


classes = (
    PROCEDURALNODES_APT_preferences,
)


def register():
    addon_updater_ops.register(bl_info)
    menus.register()
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.NODE_MT_add.append(menu_func)


def unregister():
    addon_updater_ops.unregister()
    menus.unregister()
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.NODE_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
