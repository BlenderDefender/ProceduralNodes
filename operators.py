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

import os
import shutil
# -----------------------------------------------------------------------------
import bpy
from bpy.types import (
    Operator,
    AddonPreferences,
)
from bpy.props import (
    StringProperty,
    BoolProperty,
)

from bpy_extras.io_utils import ImportHelper


from .functions.main_functions import (
    node_path,
    node_template_add,
)

from .functions.blenderdefender_functions import upgrade


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


class PROCEDURALNODES_OT_upgrade(Operator):
    """Upgrade from free to donation version"""
    bl_idname = "proceduralnodes.upgrade"
    bl_label = "Upgrade!"

    password: StringProperty(name="")

    def execute(self, context):
        """Upgrade to donation version"""
        from .functions.dict.dict import decoding
        import os

        self.report({'INFO'}, upgrade(os.path.join(os.path.expanduser("~"),
                                                   "Blender Addons Data",
                                                   "io-voodoo-tracks",
                                                   "data.blenderdefender"),
                                      decoding,
                                      self.password))
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "password")
        layout.label(text="Please enter your passcode. Don't have one?")
        layout.operator(
            "wm.url_open", text="Get one!").url = "https://gumroad.com/l/ImportVoodooCameraTracks"
        layout.label(text="Didn't receive Email with passcode?")
        layout.label(text="Please open an issue on GitHub.")
        layout.label(text="I will help as soon as possible!")


classes = (
    PROCEDURALNODES_OT_add_group,
    PROCEDURALNODES_OT_InstallFile,
    PROCEDURALNODES_OT_upgrade,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
