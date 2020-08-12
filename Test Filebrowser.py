import bpy
from bpy.types import Operator

from bpy_extras.io_utils import ImportHelper

import os


class OT_TestOpenFilebrowser(Operator, ImportHelper):

    bl_idname = "test.open_filebrowser"
    bl_label = "Install"

    def execute(self, context):
        """Do something with the selected file(s)."""

        filename = os.path.basename(self.filepath)
        extension = os.path.splitext(filename)[1]

        print('Selected file:', self.filepath)
        print('File name:', filename)
        print('File extension:', extension)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OT_TestOpenFilebrowser)


def unregister():
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)


if __name__ == "__main__":
    register()

# test call
bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')
