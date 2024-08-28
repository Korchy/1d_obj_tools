# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_obj_tools

import bmesh
import bpy
from bpy.props import FloatProperty, StringProperty
from bpy.types import Operator, Panel, Scene
from bpy.utils import register_class, unregister_class
import itertools

bl_info = {
    "name": "OBJ Tools",
    "description": "Tools for processing OBJ files",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > OBJ Tools",
    "doc_url": "https://github.com/Korchy/1d_obj_tools",
    "tracker_url": "https://github.com/Korchy/1d_obj_tools",
    "category": "All"
}


# MAIN CLASS

class OBJTools:

    dest_postfix = '_s'

    @classmethod
    def shift(cls, context, shift_x, shift_y, shift_z):
        # shift all vertices in OBJ by X,Y,Z coordinates
        src_obj = context.active_object
        # # current mode
        # mode = src_obj.mode
        # # switch to OBJECT mode
        # if src_obj.mode == 'EDIT':
        #     bpy.ops.object.mode_set(mode='OBJECT')
        # # switch to "edge selection" mode
        # context.tool_settings.mesh_select_mode = (False, True, False)
        # # process object
        # # get data from source mesh
        # bm = bmesh.new()
        # bm.from_mesh(src_obj.data)
        # bm.edges.ensure_lookup_table()
        # # process edges
        # if similar:
        #     # all combinations of materials
        #     # Pavel Kotelevec - enable working with sama mats on both linked faces. In testing (may work not proper).
        #     # mat_pairs = [set(face.material_index for face in edge.link_faces) for edge in bm.edges if edge.select
        #     #              and len(set(face.material_index for face in edge.link_faces)) > 1]
        #     mat_pairs = [set(face.material_index for face in edge.link_faces) for edge in bm.edges if edge.select]
        #     # get all materials id list
        #     mat_ids = set(itertools.chain(*mat_pairs))
        #     # deselect all edges
        #     cls._deselect_all(bm=bm)
        #     # select edges that have two materials from this list on linked faces
        #     for edge in bm.edges:
        #         edge_mats = set(face.material_index for face in edge.link_faces)
        #         # if len(edge_mats) > 1:
        #         #     if all(item in mat_ids for item in edge_mats):
        #         #         edge.select = True
        #         if all(item in mat_ids for item in edge_mats):
        #             edge.select = True
        # else:
        #     # only pairs of materials
        #     # get pairs of material on edge faces (for selected edges)
        #     mat_pairs = set(
        #         [frozenset(face.material_index for face in edge.link_faces) for edge in bm.edges if edge.select]
        #     )
        #     # mat_pairs = set(pair for pair in mat_pairs if len(pair) == 2)   # filter same material edges
        #     # deselect all edges
        #     cls._deselect_all(bm=bm)
        #     # select edges with same materials on linked faces
        #     for edge in bm.edges:
        #         if set(face.material_index for face in edge.link_faces) in mat_pairs:
        #             edge.select = True
        # # save changed data to mesh
        # bm.to_mesh(src_obj.data)
        # bm.free()
        # # return mode back
        # context.scene.objects.active = src_obj
        # bpy.ops.object.mode_set(mode=mode)

    # @staticmethod
    # def _deselect_all(bm):
    #     # remove all selection from edges and vertices in bmesh
    #     for face in bm.faces:
    #         face.select = False
    #     for edge in bm.edges:
    #         edge.select = False
    #     for vertex in bm.verts:
    #         vertex.select = False

    @staticmethod
    def ui(layout, context):
        # ui panel
        # Shift
        layout.prop(
            data=context.scene,
            property='objtools_pref_obj_file_path',
            text=''
        )
        col = layout.column(align=True)
        col.prop(
            data=context.scene,
            property='objtools_pref_shift_x'
        )
        col.prop(
            data=context.scene,
            property='objtools_pref_shift_y'
        )
        col.prop(
            data=context.scene,
            property='objtools_pref_shift_z'
        )
        layout.operator(
            operator='objtools.shift',
            icon='GO_LEFT'
        )


# OPERATORS

class OBJTools_OT_shift(Operator):
    bl_idname = 'objtools.shift'
    bl_label = 'Shift'
    bl_description = 'Shift all OBJ vertices by XYZ coordinates'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        OBJTools.shift(
            context=context,
            shift_x=context.scene.objtools_pref_shift_x,
            shift_y=context.scene.objtools_pref_shift_y,
            shift_z=context.scene.objtools_pref_shift_z
        )
        return {'FINISHED'}


# PANELS

class OBJTools_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "OBJ Tools"
    bl_category = '1D'

    def draw(self, context):
        OBJTools.ui(
            layout=self.layout,
            context=context
        )


# REGISTER

def register(ui=True):
    Scene.objtools_pref_obj_file_path = StringProperty(
        name='OBJ File Path',
        subtype='FILE_PATH',
        default='i:/dev/blender/_zakaz/PavelKotelevec/obj_tools/_all/Тетрапилон_0_4.obj'    # TODO: remove later
    )
    Scene.objtools_pref_shift_x = FloatProperty(
        name='Shift X',
        default=0.0
    )
    Scene.objtools_pref_shift_y = FloatProperty(
        name='Shift Y',
        default=0.0
    )
    Scene.objtools_pref_shift_z = FloatProperty(
        name='Shift Z',
        default=0.0
    )
    register_class(OBJTools_OT_shift)
    if ui:
        register_class(OBJTools_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(OBJTools_PT_panel)
    unregister_class(OBJTools_OT_shift)
    del Scene.objtools_pref_shift_z
    del Scene.objtools_pref_shift_y
    del Scene.objtools_pref_shift_x
    del Scene.objtools_pref_obj_file_path


if __name__ == "__main__":
    register()
