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
    node_center,
    node_path,
    node_template_add,
)


# Node Adding Operator
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


class PROCEDURALNODES_OT_CheckGumroad(Operator):
    """Checkout Gumroad for more cool Addons and Blender Files"""
    bl_idname = "proceduralnodes.check_gumroad"
    bl_label = "Checkout Gumroad for extension packs and more..."
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.wm.url_open(url="https://gumroad.com/blenderdefender")
        return {'FINISHED'}


classes = (
    PROCEDURALNODES_OT_add_group,
    PROCEDURALNODES_OT_InstallFile,
    PROCEDURALNODES_OT_CheckGumroad,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
