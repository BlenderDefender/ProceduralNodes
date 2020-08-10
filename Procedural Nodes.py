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

# -----------------------------------------------------------------------------
# Test: Get the current user.
from os.path import expanduser
home = expanduser("~")
print(home)

# -----------------------------------------------------------------------------
# Test: Get the current Blender version without the subversion.
input_str = bpy.app.version_string

# Printing original string
print("Original string: " + input_str)

result_str = ""

for i in range(0, len(input_str)):
    if i < 4:
        result_str = result_str + input_str[i]

# Printing string after removal
print("String after removal of i'th character : " + result_str)
