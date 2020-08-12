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

import shutil

import platform

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
# -----------------------------------------------------------------------------


# The destination file name is missing here. There are two possibilities: 1. When copying the file, the same filename as the source file will be used or 2. a random filename with a 6-digit number will be assigned.
destination = dirpath
# This is the path that should be entered later in the preferences.
source = os.path.join(user_name, 'Desktop', 'Eye.blend')
# print(source)
shutil.copy(source, destination)
# --> Copies the Source file to destination file.


# -----------------------------------------------------------------------------
# Test: Load a text from a .blend File.
filepath = "//untitled.blend"


# load all texts
with bpy.data.libraries.load(filepath) as (data_from, data_to):
    text = [name for name in data_from.texts if name.endswith("y")]

print(text[0])

# data_from.texts
