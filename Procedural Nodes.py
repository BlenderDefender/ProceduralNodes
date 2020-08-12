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
from bpy.types import Operator

from bpy_extras.io_utils import ImportHelper

import os
from os.path import expanduser

import shutil

import platform

# -----------------------------------------------------------------------------
# Test: Load a text from a .blend File.
filepath = "//untitled.blend"


# load all texts
with bpy.data.libraries.load(filepath) as (data_from, data_to):
    text = [name for name in data_from.texts if name.endswith("y")]

print(text[0])

# data_from.texts


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

        # Modify bl_vs_full to Output a shortened path:
        for i in range(0, len(bl_vs_full)):
            if i < 4:
                bl_vs_folder = bl_vs_folder + bl_vs_full[i]

        # Join the path to be the Addons-Directory path:
        if operating_system == "Windows":
            dirpath = os.path.join(user_name, 'AppData', 'Roaming',
                                   'Blender Foundation', 'Blender', bl_vs_folder, 'scripts', 'addons')
        elif operating_system == "Linux":
            dirpath = os.path.join(
                'home', user_name, '.config', 'blender', bl_vs_folder, 'scripts', 'addons')
        elif operating_system == "Darwin":
            dirpath = ""
        else:
            dirpath = ""
        # -----------------------------------------------------------------------------

         # The destination file name is missing here. There are two possibilities: 1. When copying the file, the same filename as the source file will be used or 2. a random filename with a 6-digit number will be assigned.

        if dirpath != "" and extension == ".blend":

            try:
                destination = dirpath
                # --> Copies the Source file to destination file.
                shutil.copy(source, destination)
                print("File installed successfully.")
                self.report({'INFO'}, "File installed successfully.")

            # If source and destination are same
            except shutil.SameFileError:
                print("File already installed.")
                self.report({'WARNING'}, "File already installed.")

            # If there is any permission issue
            except PermissionError:
                print("Permission denied.")
                self.report({'ERROR'}, "Permission denied.")

            # If source or destination doesn't Exist.
            except IOError as e:
                print('Error: %s' % e.strerror)
                self.report({'ERROR'}, 'Error: %s' % e.strerror)
            # For other errors
            except:
                print("Error occurred while installing file.")
                self.report({'ERROR'}, "Error occurred while installing file.")
        elif extension != ".blend":
            print("Wrong file format!")
            self.report({'ERROR'}, "Wrong file format!")

        elif dirpath == "":
            print(
                "Your Operating system is not supported yet. Please open a OS-Request on GitHub.")
            self.report(
                {'WARNING'}, "Your Operating system is not supported yet. Please open a OS-Request on GitHub.")


#        print('Selected file:', self.filepath)
#        print('File name:', filename)
#        print('File extension:', extension)
#        print(source)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OT_InstallFile)


def unregister():
    bpy.utils.unregister_class(OT_InstallFile)


if __name__ == "__main__":
    register()

# test call
bpy.ops.test.install_file('INVOKE_DEFAULT')
