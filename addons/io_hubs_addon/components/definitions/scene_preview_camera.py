from bpy.types import Operator, Image
from bpy.props import PointerProperty
from ..hubs_component import HubsComponent
from ..types import Category, PanelType, NodeType
from ..utils import is_gpu_available
from ...utils import rgetattr, rsetattr
import bpy
import os
from mathutils import Matrix
from math import radians
from ..gizmos import CustomModelGizmo, bone_matrix_world
from ..models import scene_preview_camera

IMAGE_NAME = "scene_preview_camera"
PREVIEW_SIZE = (1920, 1080)


def get_image_path(name):
    return f"{bpy.app.tempdir}/{name}.png"


def update_image_editors(img):
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.spaces.active.image = img


class RenderOperator(Operator):
    bl_idname = "render.hubs_render"
    bl_label = "Hubs Render"

    rendering = False
    done = False
    cancelled = False
    saved_props = {}
    camera_object = None
    camera_data = None

    def render_post(self, scene, depsgraph):
        self.done = True
        self.rendering = False

    def render_cancelled(self, scene, depsgraph):
        self.cancelled = True

    def setup_render(self, context):
        self.camera_data = bpy.data.cameras.new(name='Temp Hubs Camera Data')
        self.camera_data.type = "PERSP"
        self.camera_data.clip_start = 0.1
        self.camera_data.clip_end = 2000
        self.camera_data.lens_unit = "FOV"
        self.camera_data.angle = radians(80)

        self.camera_object = bpy.data.objects.new('Temp Hubs Camera Object', self.camera_data)
        self.camera_object.matrix_world = context.active_object.matrix_world.copy()
        rot_offset = Matrix.Rotation(radians(90), 4, 'X')
        self.camera_object.matrix_world = self.camera_object.matrix_world @ rot_offset
        bpy.context.scene.collection.objects.link(self.camera_object)

        use_compositor = context.scene.hubs_scene_reflection_probe_properties.use_compositor
        output_path = get_image_path(IMAGE_NAME)

        overrides = [
            ("preferences.view.render_display_type", "NONE"),
            ("scene.camera", self.camera_object),
            ("scene.cycles.device", "GPU" if is_gpu_available(context) else "CPU"),
            ("scene.render.resolution_x", PREVIEW_SIZE[0]),
            ("scene.render.resolution_y", PREVIEW_SIZE[1]),
            ("scene.render.resolution_percentage", 100),
            ("scene.render.image_settings.file_format", "PNG"),
            ("scene.render.filepath", output_path),
            ("scene.render.use_compositing", use_compositor),
            ("scene.use_nodes", use_compositor)
        ]

        for (prop, value) in overrides:
            if prop not in self.saved_props:
                self.saved_props[prop] = rgetattr(bpy.context, prop)
            rsetattr(bpy.context, prop, value)

    def restore_render(self):
        bpy.context.scene.collection.objects.unlink(self.camera_object)
        bpy.data.cameras.remove(self.camera_data)

        for prop in self.saved_props:
            rsetattr(bpy.context, prop, self.saved_props[prop])

    def execute(self, context):
        bpy.app.handlers.render_post.append(self.render_post)
        bpy.app.handlers.render_cancel.append(self.render_cancelled)

        self.saved_props = {}
        self.cancelled = False
        self.done = False
        self.rendering = False

        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        context.window_manager.modal_handler_add(self)

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.cancelled or self.done:
                self.restore_render()

                bpy.app.handlers.render_post.remove(self.render_post)
                bpy.app.handlers.render_cancel.remove(self.render_cancelled)

                context.window_manager.event_timer_remove(self._timer)

                bpy.context.scene.render.use_lock_interface = False

                if self.cancelled:
                    img_path = get_image_path(IMAGE_NAME)
                    if os.path.exists(img_path):
                        os.remove(img_path)

                    self.report({'WARNING'}, 'Preview camera render cancelled')
                    return {"CANCELLED"}

                #  Remove the old image if it exists
                context.active_object.hubs_component_scene_preview_camera['preview'] = None
                for img in bpy.data.images:
                    if img.name == IMAGE_NAME:
                        if img.users:
                            continue
                        bpy.data.images.remove(img)
                        break

                img_path = get_image_path(IMAGE_NAME)
                img = bpy.data.images.load(filepath=img_path)
                img.name = IMAGE_NAME

                update_image_editors(img)

                # Assign pack and remove from disk the new image
                context.active_object.hubs_component_scene_preview_camera['preview'] = img
                img.pack()
                new_filepath = get_image_path(IMAGE_NAME)
                img.packed_files[0].filepath = new_filepath
                img.filepath_raw = new_filepath
                img.filepath = new_filepath
                if os.path.exists(img_path):
                    os.remove(img_path)

                self.report({'INFO'}, 'Preview camera render finished')
                return {"FINISHED"}

            elif not self.rendering:
                try:
                    self.setup_render(context)

                    bpy.context.scene.render.use_lock_interface = True

                    if bpy.ops.render.render("INVOKE_DEFAULT", write_still=True) != {'CANCELLED'}:
                        self.rendering = True

                except Exception as e:
                    print(e)
                    self.cancelled = True
                    self.report(
                        {'ERROR'}, 'Preview camera render  error %s' % e)

        return {"PASS_THROUGH"}


class ScenePreviewCamera(HubsComponent):
    _definition = {
        'name': 'scene-preview-camera',
        'display_name': 'Scene Preview Camera',
        'category': Category.SCENE,
        'node_type': NodeType.NODE,
        'panel_type': [PanelType.OBJECT, PanelType.BONE],
        'icon': 'CAMERA_DATA',
        'gizmo': 'waypoint',
        'version': (1, 0, 0)
    }

    preview: PointerProperty(
        name="Preview",
        description="Preview image",
        type=Image
    )

    def pre_export(self, export_settings, host, ob=None):
        global backup_name
        backup_name = host.name
        host.name = 'scene-preview-camera'

    def post_export(self, export_settings, host, ob=None):
        global backup_name
        host.name = backup_name
        backup_name = ""

    def draw(self, context, layout, panel):
        if not self.preview:
            row = layout.row()
            row.alert = True
            row.label(
                text="No preview found.",
                icon='ERROR')
        row = layout.row()
        row.prop(self, "preview")
        row = layout.row()
        row.operator(
            "render.hubs_render",
            text="Render Preview Camera"
        )

    def gather(self, export_settings, object):
        from ...io.utils import gather_texture
        return {
            "preview": {
                "__mhc_link_type": "texture",
                "index": gather_texture(self.preview, export_settings)
            }
        }

    @classmethod
    def update_gizmo(cls, ob, bone, target, gizmo):
        if bone:
            mat = bone_matrix_world(ob, bone)
        else:
            mat = ob.matrix_world.copy()

        rot_offset = Matrix.Rotation(radians(180), 4, 'Z')
        gizmo.matrix_basis = mat @ rot_offset
        gizmo.hide = not ob.visible_get()

    @classmethod
    def create_gizmo(cls, ob, gizmo_group):
        gizmo = gizmo_group.gizmos.new(CustomModelGizmo.bl_idname)
        gizmo.object = ob
        setattr(gizmo, "hubs_gizmo_shape", scene_preview_camera.SHAPE)
        gizmo.setup()
        gizmo.use_draw_scale = False
        gizmo.use_draw_modal = False
        gizmo.color = (0.8, 0.8, 0.8)
        gizmo.alpha = 0.5
        gizmo.scale_basis = 1.0
        gizmo.hide_select = True
        gizmo.color_highlight = (0.8, 0.8, 0.8)
        gizmo.alpha_highlight = 1.0

        return gizmo

    @ staticmethod
    def register():
        bpy.utils.register_class(RenderOperator)

    @ staticmethod
    def unregister():
        bpy.utils.unregister_class(RenderOperator)
