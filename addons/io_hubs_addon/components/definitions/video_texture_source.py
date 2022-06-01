from bpy.props import IntVectorProperty, IntProperty
from ..hubs_component import HubsComponent
from ..types import Category, PanelType, NodeType
from ..utils import children_recursive


class VideoTextureSource(HubsComponent):
    _definition = {
        'name': 'video-texture-source',
        'display_name': 'Video Texture Source',
        'category': Category.SCENE,
        'node_type': NodeType.NODE,
        'panel_type': PanelType.OBJECT,
        'icon': 'VIEW_CAMERA'
    }

    resolution: IntVectorProperty(name="Resolution",
                                  description="Resolution",
                                  size=2,
                                  subtype="DIRECTION",
                                  default=[1280, 720])

    fps: IntProperty(
        name="FPS", description="FPS", default=15)

    @classmethod
    def poll(cls, context):
        # TODO Should we listen to scene graph updates and remove the component if this is no longer satisfied to avoid dangling components?
        return context.object.type == 'CAMERA' or [x for x in children_recursive(context.object) if x.type == "CAMERA"]
