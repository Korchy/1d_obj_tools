# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_obj_tools

from bpy.props import FloatProperty, StringProperty
from bpy.types import Operator, Panel, Scene
from bpy.utils import register_class, unregister_class
import fileinput

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
    def shift(cls, context, op, obj_file_path, shift_x, shift_y, shift_z):
        # shift all vertices in OBJ by X,Y,Z coordinates
        counter = 0
        with fileinput.FileInput(obj_file_path) as file:
            for line in file:
                if line.startswith('v '):
                    counter += 1
                    print(line)

        # show message on finish
        op.report(
            type={'INFO'},
            message='OBJ shifted, processed ' + str(counter) + ' lines.'
        )

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
            op=self,
            obj_file_path=context.scene.objtools_pref_obj_file_path,
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
