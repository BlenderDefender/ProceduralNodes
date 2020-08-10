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

from os.path import expanduser
import bpy

import os
from os.path import expanduser

# Declare Blender Full version name and Blender Folder version name string:
bl_vs_full = bpy.app.version_string
bl_vs_folder = ""
user_name = expanduser("~")


# Modify bl_vs_full to Output a shortened path:
for i in range(0, len(bl_vs_full)):
    if i < 4:
        bl_vs_folder = bl_vs_folder + bl_vs_full[i]

# Join the path to be the Addons-Directory path:
bl_addons_folder = os.path.join(user_name, 'AppData', 'Roaming',
                                'Blender Foundation', 'Blender', bl_vs_folder, 'scripts', 'addons')

# /home/<user>/.config/blender/<version>/scripts/addons --> Linux
# C:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\<version>\scripts\addons --> Windows
# /Users/$USER/Library/Application Support/Blender/version/??????? --> unsure, MacOS

print("The Addons Directory path is: " + bl_addons_folder)


# -----------------------------------------------------------------------------
# Test: Get the current user.
home = expanduser("~")
print(home)

# -----------------------------------------------------------------------------
# Test: Load a text from a .blend File.
filepath = "//untitled.blend"


# load all texts
with bpy.data.libraries.load(filepath) as (data_from, data_to):
    text = [name for name in data_from.texts if name.endswith("y")]

print(text[0])

# data_from.texts
