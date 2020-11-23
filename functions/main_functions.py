import bpy
import os


def node_center(context):
    from mathutils import Vector
    loc = Vector((0.0, 0.0))
    node_selected = context.selected_nodes
    if node_selected:
        for node in node_selected:
            loc += node.location
        loc /= len(node_selected)
    return loc


def node_template_add(context, filepath, node_group, ungroup, report):
    """ Main function
    """

    space = context.space_data
    node_tree = space.node_tree
    node_active = context.active_node
    node_selected = context.selected_nodes

    if node_tree is None:
        report({'ERROR'}, "No node tree available")
        return

    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        assert(node_group in data_from.node_groups)
        data_to.node_groups = [node_group]
    node_group = data_to.node_groups[0]

    # add node!
    center = node_center(context)

    for node in node_tree.nodes:
        node.select = False

    node_type_string = {
        "ShaderNodeTree": "ShaderNodeGroup",
        "CompositorNodeTree": "CompositorNodeGroup",
        "TextureNodeTree": "TextureNodeGroup",
    }[type(node_tree).__name__]

    node = node_tree.nodes.new(type=node_type_string)
    node.node_tree = node_group

    is_fail = (node.node_tree is None)
    if is_fail:
        report({'WARNING'}, "Incompatible node type")

    node.select = True
    node_tree.nodes.active = node
    node.location = center

    if is_fail:
        node_tree.nodes.remove(node)
    else:
        if ungroup:
            bpy.ops.node.group_ungroup()

    # node_group.user_clear()
    # bpy.data.node_groups.remove(node_group)


def node_path(context):
    # Addons-Directory path:
    dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    return dirpath
