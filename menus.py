import bpy
import os

from bpy.types import Menu

from .functions.main_functions import node_path

from . import operators


def node_template_cache(context, *, reload=False):
    dirpath = node_path(context)

    if node_template_cache._node_cache_path != dirpath:
        reload = True

    node_cache = node_template_cache._node_cache
    if reload:
        node_cache = []
    if node_cache:
        return node_cache

    for fn in os.listdir(dirpath):
        if fn.endswith(".blend"):
            filepath = os.path.join(dirpath, fn)
            with bpy.data.libraries.load(filepath) as (data_from, data_to):
                for group_name in data_from.node_groups:
                    if not group_name.startswith("_"):
                        node_cache.append((filepath, group_name))

    node_template_cache._node_cache = node_cache
    node_template_cache._node_cache_path = dirpath

    return node_cache


node_template_cache._node_cache = []
node_template_cache._node_cache_path = ""


class PROCEDURALNODES_MT_main_menu(Menu):
    bl_label = "Node Groups"
    bl_idname = "PROCEDURALNODES_MT_main_menu"

    def draw(self, context):
        layout = self.layout

        dirpath = node_path(context)
        if dirpath == "":
            layout.label(
                text="Your Operating system is not supported yet. Please open a OS-Request on GitHub.")
            return

        try:
            node_items = node_template_cache(context)
        except Exception as ex:
            node_items = ()
            layout.label(text=repr(ex), icon='ERROR')

        for filepath, group_name in node_items:
            props = layout.operator(
                "proceduralnodes.add_group",
                text=group_name,
            )
            print(props)
            props.filepath = filepath
            props.group_name = group_name


classes = (
    PROCEDURALNODES_MT_main_menu,
)


def register():
    operators.register()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    operators.unregister()
    for cls in classes:
        bpy.utils.unregister_class(cls)
