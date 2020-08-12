import bpy
from bpy.types import Operator

from bpy_extras.io_utils import ImportHelper

import os


class OT_TestOpenFilebrowser(Operator, ImportHelper):

    bl_idname = "test.open_filebrowser"
    bl_label = "Open the file browser (yay)"

#    filter_glob: StringProperty(
#        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp; *.blend',
#        options={'HIDDEN'} )

#    some_boolean: BoolProperty(
#        name='Do a thing',
#        description='Do a thing with the file you\'ve selected',
#        default=True, )

    def execute(self, context):
        """Do something with the selected file(s)."""

        filename, extension = os.path.splitext(self.filepath)
        print('Selected file:', self.filepath)
        print('File name:', filename)
        print('File extension:', extension)
#        print('Some Boolean:', self.some_boolean)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OT_TestOpenFilebrowser)


def unregister():
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)


if __name__ == "__main__":
    register()

# test call
bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')
