import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

bl_info = {
    "name": "Example Add-on Preferences",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 82, 0),
    "location": "SpaceBar Search -> Add-on Preferences Example",
    "description": "Example Add-on",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}


class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    )
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "filepath")
        layout.prop(self, "number")
        layout.prop(self, "boolean")
        layout.operator("addongen.hallo_world_operator")


class HelloWorldOperator(bpy.types.Operator):
    """ToolTip of HelloWorldOperator"""
    bl_idname = "addongen.hallo_world_operator"
    bl_label = "Hello World Operator"
    bl_options = {'REGISTER'}

    def execute(self, context):
        self.report({'INFO'}, "Hello World!")
        return {'FINISHED'}

# class OBJECT_OT_addon_prefs_example(Operator):
#    """Display example preferences"""
#    bl_idname = "object.addon_prefs_example"
#    bl_label = "Add-on Preferences Example"
#    bl_options = {'REGISTER', 'UNDO'}

#    def execute(self, context):
#        preferences = context.preferences
#        addon_prefs = preferences.addons[__name__].preferences

#        info = ("Path: %s, Number: %d, Boolean %r" %
#                (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

#        self.report({'INFO'}, info)
#        print(info)

#        return {'FINISHED'}


# Registration
def register():
    bpy.utils.register_class(HelloWorldOperator)
    bpy.utils.register_class(ExampleAddonPreferences)


def unregister():
    bpy.utils.unregister_class(HelloWorldOperator)
    bpy.utils.unregister_class(ExampleAddonPreferences)
