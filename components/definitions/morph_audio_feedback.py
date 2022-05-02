import atexit
import bpy
from bpy.props import FloatProperty, StringProperty, BoolProperty, CollectionProperty, IntProperty
from bpy.types import PropertyGroup, Menu, Operator
from .hubs_component import HubsComponent
from ..types import Category, NodeType, PanelType


class ShapeKeysList(bpy.types.UIList):
    bl_idname = "HUBS_UL_SHAPE_KEYS_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        key_block = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            split = layout.split(factor=0.90, align=False)
            split.prop(key_block, "name", text="",
                       emboss=False, icon_value=icon)
            row = split.row(align=True)
            row.emboss = 'NONE_OR_STATUS'
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class AddShapeKeyOperator(Operator):
    bl_idname = "hubs_morph_audio_feedback.add_shape_key"
    bl_label = "Add Shape Key"

    shape_key_name: StringProperty(
        name="Shape Key Name", description="Shape Key Name", default="")

    def execute(self, context):
        ob = context.object
        shape_key = ob.hubs_component_morph_audio_feedback.shape_keys.add()
        shape_key.name = self.shape_key_name
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class RemoveShapeKeyOperator(Operator):
    bl_idname = "hubs_morph_audio_feedback.remove_shape_key"
    bl_label = "Add Shape Key"

    @classmethod
    def poll(self, context):
        return context.object.hubs_component_morph_audio_feedback.active_shape_key != -1

    def execute(self, context):
        active_shape_key = context.object.hubs_component_morph_audio_feedback.active_shape_key
        context.object.hubs_component_morph_audio_feedback.shape_keys.remove(
            active_shape_key)
        return {'FINISHED'}


def has_shape_key(shape_keys, shape_key):
    exists = False
    for item in shape_keys:
        if item.name == shape_key:
            exists = True
            break

    return exists


class ShapeKeysContextMenu(Menu):
    bl_idname = "HUBS_MT_SHAPE_KEYS_context_menu"
    bl_label = "Shape Key Specials"

    def draw(self, context):
        ob = context.object

        no_shape_keys = True
        if hasattr(ob.data.shape_keys, 'key_blocks'):
            for k, _ in ob.data.shape_keys.key_blocks.items():
                if not has_shape_key(context.object.hubs_component_morph_audio_feedback.shape_keys, k):
                    self.layout.operator(AddShapeKeyOperator.bl_idname, icon='SHAPEKEY_DATA',
                                         text=k).shape_key_name = k
                    no_shape_keys = False

        if no_shape_keys:
            self.layout.label(text="No shape keys available")


class ShapeKeyPropertyType(PropertyGroup):
    name: StringProperty(
        name="Shape Key name",
        description="Shape Key Name",
        default=""
    )


bpy.utils.register_class(ShapeKeyPropertyType)


@atexit.register
def unregister():
    bpy.utils.unregister_class(ShapeKeyPropertyType)


class MorphAudioFeedback(HubsComponent):
    _definition = {
        'id': 'morph-audio-feedback',
        'name': 'hubs_component_morph_audio_feedback',
        'display_name': 'Morph Audio Feedback',
        'category': Category.AVATAR,
        'node_type': NodeType.NODE,
        'panel_type': PanelType.OBJECT_DATA
    }

    shape_keys: CollectionProperty(
        type=ShapeKeyPropertyType,
        options={'HIDDEN', 'SKIP_SAVE'})

    active_shape_key: IntProperty(
        name="Active action index",
        description="Active action index",
        default=-1
    )

    minValue: FloatProperty(name="Min Value",
                            description="Min Value",
                            default=0.0,)

    maxValue: FloatProperty(name="Max Value",
                            description="Max Value",
                            default=1.0)

    def draw(self, layout):
        layout.label(text='Shape keys to morph:')

        row = layout.row()
        row.template_list(ShapeKeysList.bl_idname, "", self,
                          "shape_keys", self, "active_shape_key", rows=3)

        col = row.column(align=True)

        col.menu(ShapeKeysContextMenu.bl_idname, icon='ADD', text="")
        col.operator(RemoveShapeKeyOperator.bl_idname,
                     icon='REMOVE', text="")

        layout.separator()

        layout.prop(data=self, property='minValue')
        layout.prop(data=self, property='maxValue')

    @classmethod
    def poll(cls, context):
        return context.object.type == 'MESH'

    @staticmethod
    def register():
        bpy.utils.register_class(ShapeKeysList)
        bpy.utils.register_class(ShapeKeysContextMenu)
        bpy.utils.register_class(AddShapeKeyOperator)
        bpy.utils.register_class(RemoveShapeKeyOperator)

    @staticmethod
    def unregister():
        bpy.utils.unregister_class(ShapeKeysList)
        bpy.utils.unregister_class(ShapeKeysContextMenu)
        bpy.utils.unregister_class(AddShapeKeyOperator)
        bpy.utils.unregister_class(RemoveShapeKeyOperator)
