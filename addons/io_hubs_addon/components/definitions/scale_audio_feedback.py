from bpy.props import FloatProperty
from .hubs_component import HubsComponent
from ..types import Category, NodeType, PanelType


class ScaleAudioFeedback(HubsComponent):
    _definition = {
        'id': 'scale-audio-feedback',
        'name': 'hubs_component_scale_audio_feedback',
        'display_name': 'Scale Audio Feedback',
        'category': Category.AVATAR,
        'node_type': NodeType.NODE,
        'panel_type': PanelType.OBJECT_DATA
    }

    minScale: FloatProperty(name="Min Scale",
                            description="Min Scale",
                            default=1.0)

    maxScale: FloatProperty(name="Max Scale",
                            description="Max Scale",
                            default=1.5)
