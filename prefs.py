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
from bpy.types import AddonPreferences

# -----------------------------------------------------------------------------
from . import addon_updater_ops

from .functions.blenderdefender_functions import check_free_donation_version, url

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


# -----------------------------------------------------------------------------
# Addon Preferences
class PROCEDURALNODES_APT_preferences(AddonPreferences):
    bl_idname = __package__

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
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

        if check_free_donation_version() == "free":
            layout.operator("wm.url_open", text="Checkout Gumroad for other addons and more...",
                            icon='FUND').url = "https://gumroad.com/blenderdefender"
            layout.label(
                text="Procedural Nodes - You are using the free version.")
            layout.label(
                text="If you want to support me and get cool discount codes, please upgrade to donation version. :)")
            layout.operator("proceduralnodes.upgrade")
            layout.label(text="")
        elif check_free_donation_version() == "donation":
            layout.label(
                text="Procedural Nodes - You are using the donation version. Thank you :)", icon='FUND')
            layout.operator(
                "wm.url_open", text="Get discount code for cool Blender Products").url = url()
        elif check_free_donation_version() == "database_file_corrupted":
            layout.operator("wm.url_open", text="Checkout Gumroad for other addons and more...",
                            icon='FUND').url = "https://gumroad.com/blenderdefender"
            layout.label(
                text="Procedural Nodes - Databasefile corrupted! Please delete it.")
            layout.label(
                text="And please, stop messing around with .db files. Thanks :)")
            layout.operator("proceduralnodes.upgrade",
                            text="Upgrade to donation version.")
            layout.label(text="")

        layout.operator("proceduralnodes.install_file", icon="IMPORT")

        addon_updater_ops.update_settings_ui(self, context)


classes = (
    PROCEDURALNODES_APT_preferences,
)


def register():
    addon_updater_ops.register(bl_info)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    addon_updater_ops.unregister()
    for cls in classes:
        bpy.utils.unregister_class(cls)
