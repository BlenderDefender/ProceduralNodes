# ##### BEGIN GPL LICENSE BLOCK #####
#
#    Copyright (C) <2020>  <Blender Defender>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
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
from bpy.props import (
    StringProperty,
)
from bpy.types import (
    Operator,
    Menu,
    AddonPreferences,
)

from bpy_extras.io_utils import ImportHelper

import os
from os.path import expanduser

import shutil

import platform

bl_info = {
    "name": "Procedural Nodes",
    "description": "Useful and cool node groups",
    "author": "Blender Defender",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Node Editors > Add > BD",
    "description": "Add node groups directly to the node editors",
    "warning": "",
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
    if operating_system == "Windows":
        dirpath = os.path.join(user_name, 'AppData', 'Roaming',
                               'Blender Foundation', 'Blender', bl_vs_folder, 'scripts', 'addons')
    elif operating_system == "Linux":
        dirpath = os.path.join('home', user_name, '.config',
                               'blender', bl_vs_folder, 'scripts', 'addons')
    elif operating_system == "Darwin":
        dirpath = ""
    else:
        dirpath = ""

    return dirpath


class NODE_OT_Test(Operator):
    """Add a node template"""
    bl_idname = "node.ot_test"
    bl_label = "Add node group template"
    bl_description = "Add node group template"
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


class NODE_MT_Test(Menu):
    bl_label = "Node Template"

    def draw(self, context):
        layout = self.layout

        # Test call, as long as the Operator is not in the addon prefs.
        layout.operator("test.install_file")

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
                NODE_OT_Test.bl_idname,
                text=group_name,
            )
            props.filepath = filepath
            props.group_name = group_name


class OT_InstallFile(Operator, ImportHelper):

    bl_idname = "test.install_file"
    bl_label = "Install"

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
            #            print("File is not licensed")
            lck = "00000000"

#        print(lck)

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
                # --> Copies the Source file to destination file.
#                print("File installed successfully.")
                self.report({'INFO'}, "File installed successfully.")

            # If source and destination are same
            except shutil.SameFileError:
                #                print("File already installed.")
                self.report({'WARNING'}, "File already installed.")

            # If there is any permission issue
            except PermissionError:
                #                print("Permission denied.")
                self.report({'ERROR'}, "Permission denied.")

            # If source or destination doesn't Exist.
            except IOError as e:
                #                 print('Error: %s' % e.strerror)
                self.report({'ERROR'}, 'Error: %s' % e.strerror)
            # For other errors
            except:
                #                print("Error occurred while installing file.")
                self.report({'ERROR'}, "Error occurred while installing file.")
        elif extension != ".blend":
            #            print("Wrong file format!")
            self.report({'ERROR'}, "The file must be a .blend file!")

        elif dirpath == "":
            #            print("Your Operating system is not supported yet. Please open a OS-Request on GitHub.")
            self.report(
                {'WARNING'}, "Your Operating system is not supported yet. Please open a OS-Request on GitHub.")

        elif verified == "False":
            #            print("Your file is not licensed!")
            self.report({'ERROR'}, "Your file is not licensed!")


#        print('Selected file:', self.filepath)
#        print('File name:', filename)
#        print('File extension:', extension)
#        print(source)

        return {'FINISHED'}


class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        layout.operator("test.install_file")


def menu_func(self, context):
    self.layout.menu(
        NODE_MT_Test.__name__,
        text="Procedural Nodes",
        icon='PRESET_NEW',
    )


classes = (
    NODE_OT_Test,
    NODE_MT_Test,
    OT_InstallFile,
    #    NodeTemplatePrefs
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.NODE_MT_add.append(menu_func)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.NODE_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
