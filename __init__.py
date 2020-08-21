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
from . import addon_updater_ops

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


# Node Adding Operator
def node_center(context):
    from mathutils import Vector
    loc = Vector((0.0, 0.0))
    node_selected = context.selected_nodes
    if node_selected:
        for node in node_selected:
            loc += node.location
        loc /= len(node_selected)
    return loc


def node_template_add(context, filepath, node_group, ungroup, report):
    """ Main function
    """

    space = context.space_data
    node_tree = space.node_tree
    node_active = context.active_node
    node_selected = context.selected_nodes

    if node_tree is None:
        report({'ERROR'}, "No node tree available")
        return

    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        assert(node_group in data_from.node_groups)
        data_to.node_groups = [node_group]
    node_group = data_to.node_groups[0]

    # add node!
    center = node_center(context)

    for node in node_tree.nodes:
        node.select = False

    node_type_string = {
        "ShaderNodeTree": "ShaderNodeGroup",
        "CompositorNodeTree": "CompositorNodeGroup",
        "TextureNodeTree": "TextureNodeGroup",
    }[type(node_tree).__name__]

    node = node_tree.nodes.new(type=node_type_string)
    node.node_tree = node_group

    is_fail = (node.node_tree is None)
    if is_fail:
        report({'WARNING'}, "Incompatible node type")

    node.select = True
    node_tree.nodes.active = node
    node.location = center

    if is_fail:
        node_tree.nodes.remove(node)
    else:
        if ungroup:
            bpy.ops.node.group_ungroup()

    # node_group.user_clear()
    # bpy.data.node_groups.remove(node_group)


# -----------------------------------------------------------------------------
# Node Template Prefs

def node_path(context):
    bl_vs_full = bpy.app.version_string
    bl_vs_folder = ""
    user_name = expanduser("~")
    operating_system = platform.system()

    # Modify bl_vs_full to Output a shortened path:
    for i in range(0, len(bl_vs_full)):
        if i < 4:
            bl_vs_folder = bl_vs_folder + bl_vs_full[i]

    # Join the path to be the Addons-Directory path:
    dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    return dirpath


class PROCEDURALNODES_OT_add_group(Operator):
    """Add a pre-made Node Group"""
    bl_idname = "proceduralnodes.add_group"
    bl_label = "Add pre-made Node Group"
    bl_description = "Add pre-made Node Group"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(
        subtype='FILE_PATH',
    )
    group_name: StringProperty()

    def execute(self, context):
        node_template_add(context, self.filepath,
                          self.group_name, True, self.report)

        return {'FINISHED'}

    def invoke(self, context, event):
        node_template_add(context, self.filepath,
                          self.group_name, event.shift, self.report)

        return {'FINISHED'}


# -----------------------------------------------------------------------------
# Node menu list

def node_template_cache(context, *, reload=False):
    dirpath = node_path(context)

    if node_template_cache._node_cache_path != dirpath:
        reload = True

    node_cache = node_template_cache._node_cache
    if reload:
        node_cache = []
    if node_cache:
        return node_cache

    for fn in os.listdir(dirpath):
        if fn.endswith(".blend"):
            filepath = os.path.join(dirpath, fn)
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                for group_name in data_from.node_groups:
                    if not group_name.startswith("_"):
                        node_cache.append((filepath, group_name))

    node_template_cache._node_cache = node_cache
    node_template_cache._node_cache_path = dirpath

    return node_cache


node_template_cache._node_cache = []
node_template_cache._node_cache_path = ""


class PROCEDURALNODES_MT_main_menu(Menu):
    bl_label = "Node Groups"

    def draw(self, context):
        layout = self.layout

        dirpath = node_path(context)
        if dirpath == "":
            layout.label(
                text="Your Operating system is not supported yet. Please open a OS-Request on GitHub.")
            return

        try:
            node_items = node_template_cache(context)
        except Exception as ex:
            node_items = ()
            layout.label(text=repr(ex), icon='ERROR')

        for filepath, group_name in node_items:
            props = layout.operator(
                PROCEDURALNODES_OT_add_group.bl_idname,
                text=group_name,
            )
            props.filepath = filepath
            props.group_name = group_name


# -----------------------------------------------------------------------------
# Install licensed file
class PROCEDURALNODES_OT_InstallFile(Operator, ImportHelper):
    """Install a licensed .blend file for Procedural Nodes."""
    bl_idname = "proceduralnodes.install_file"
    bl_label = "Install Procedural Nodes file"

    def execute(self, context):
        """Install selected file(s)."""

        filename = os.path.basename(self.filepath)
        extension = os.path.splitext(filename)[1]
        source = self.filepath
        bl_vs_full = bpy.app.version_string
        bl_vs_folder = ""
        user_name = expanduser("~")
        operating_system = platform.system()
        dirpath = node_path(context)

        # -----------------------------------------------------------------------------
        if extension == ".blend":
            with bpy.data.libraries.load(source) as (data_from, data_to):

                texts = [
                    name for name in data_from.texts if name.endswith("f")]

        try:
            lck = texts[0]

        except:
            lck = "00000000"

        if lck.find("°j4C") == -1:
            if lck.find("8yl!") == -1:
                if lck.find("5c*7") == -1:
                    verified = "False"
                else:
                    verified = "True"
            else:
                verified = "True"
        else:
            verified = "True"

        if dirpath != "" and extension == ".blend" and verified == "True":

            try:
                destination = dirpath
                shutil.copy(source, destination)

                self.report({'INFO'}, "File installed successfully.")

            # If source and destination are same
            except shutil.SameFileError:
                self.report({'WARNING'}, "File already installed.")

            # If there is any permission issue
            except PermissionError:
                self.report({'ERROR'}, "Permission denied.")

            # If source or destination doesn't Exist.
            except IOError as e:
                self.report({'ERROR'}, 'Error: %s' % e.strerror)

            # For other errors
            except:
                self.report({'ERROR'}, "Error occurred while installing file.")

        elif extension != ".blend":
            self.report({'ERROR'}, "The file must be a .blend file!")

        elif dirpath == "":
            self.report(
                {'WARNING'}, "Your Operating system is not supported yet. Please open a OS-Request on GitHub.")

        elif verified == "False":
            self.report({'ERROR'}, "Your file is not licensed!")

        return {'FINISHED'}


class PROCEDURALNODES_OT_CheckGumroad(bpy.types.Operator):
    """Checkout Gumroad for more cool Addons and Blender Files"""
    bl_idname = "proceduralnodes.check_gumroad"
    bl_label = "Checkout Gumroad for extension packs and more..."
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.wm.url_open(url="https://gumroad.com/blenderdefender")
        return {'FINISHED'}


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
        PROCEDURALNODES_MT_main_menu.__name__,
        text="Procedural Nodes",
        icon='PRESET_NEW',
    )


classes = (
    PROCEDURALNODES_OT_add_group,
    PROCEDURALNODES_OT_InstallFile,
    PROCEDURALNODES_OT_CheckGumroad,
    PROCEDURALNODES_MT_main_menu,
    PROCEDURALNODES_APT_preferences,
)


def register():
    addon_updater_ops.register(bl_info)
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.NODE_MT_add.append(menu_func)


def unregister():
    addon_updater_ops.unregister()
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.NODE_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
