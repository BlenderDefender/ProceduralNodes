
import bpy
from bpy.types import AddonPreferences

# -----------------------------------------------------------------------------
from . import addon_updater_ops

bl_info = {
    "name": "Procedural Nodes",
    "description": "Useful and cool node groups",
    "author": "Blender Defender",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Node Editors > Add > Procedural Nodes",
    "description": "Add pre-made node groups to the node editors",
    "warning": "Check Out Gumroad for extension packs and more",
    "doc_url": "",
    "category": "Node",
}


# -----------------------------------------------------------------------------
# Addon Preferences
class PROCEDURALNODES_APT_preferences(AddonPreferences):  # Procedural Nodes
    bl_idname = __package__

    # addon updater preferences

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
    )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        layout = self.layout
        mainrow = layout.row()
        col = mainrow.column()
        layout.operator("proceduralnodes.check_gumroad", icon='FUND')

        addon_updater_ops.update_settings_ui(self, context)

        layout.operator("proceduralnodes.install_file")


classes = (
    PROCEDURALNODES_APT_preferences,
)


def register():
    addon_updater_ops.register(bl_info)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    addon_updater_ops.unregister()
    for cls in classes:
        bpy.utils.unregister_class(cls)
