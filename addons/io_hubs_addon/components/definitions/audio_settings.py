from bpy.props import FloatProperty, EnumProperty
from ..hubs_component import HubsComponent
from ..types import Category, PanelType, NodeType
from ..consts import DISTACE_MODELS, MAX_ANGLE


class AudioSettings(HubsComponent):
    _definition = {
        'name': 'audio-settings',
        'display_name': 'Audio Settings',
        'category': Category.SCENE,
        'node_type': NodeType.SCENE,
        'panel_type': [PanelType.SCENE],
        'icon': 'SPEAKER'
    }

    avatarDistanceModel: EnumProperty(
        name="Avatar Distance Model",
        description="Avatar Distance Model",
        items=DISTACE_MODELS,
        default="inverse")

    avatarRolloffFactor: FloatProperty(
        name="Avatar Rolloff Factor", default=2.0, min=0.0, soft_min=0.0)

    avatarRefDistance: FloatProperty(
        name="Avatar Ref Distance", description="Avatar Ref Distance", subtype="DISTANCE", default=1.0, min=0.0, soft_min=0.0)

    avatarMaxDistance: FloatProperty(
        name="Avatar Max Distance", description="Avatar Max Distance", subtype="DISTANCE", default=10000.0, min=0.0, soft_min=0.0)

    mediaVolume: FloatProperty(
        name="Media Volume", description="Media Volume", default=0.5, min=0.0, soft_min=0.0)

    mediaDistanceModel: EnumProperty(
        name="Media Distance Model",
        description="Media Distance Model",
        items=DISTACE_MODELS,
        default="inverse")

    mediaRolloffFactor: FloatProperty(
        name="Media Rolloff Factor", description="Media Rolloff Factor", default=2.0, min=0.0, soft_min=0.0)

    mediaRefDistance: FloatProperty(
        name="Media Ref Distance", description="Media Rolloff Factor", subtype="DISTANCE", default=2.0, min=0.0, soft_min=0.0)

    mediaMaxDistance: FloatProperty(
        name="Media Max Distance", description="Media Max Distance", subtype="DISTANCE", default=10000.0, min=0.0, soft_min=0.0)

    mediaConeInnerAngle: FloatProperty(
        name="Media Cone Inner Angle", description="Media Cone Inner Angle", subtype="ANGLE", default=MAX_ANGLE, min=0.0, soft_min=0.0, max=MAX_ANGLE, soft_max=MAX_ANGLE)

    mediaConeOuterAngle: FloatProperty(
        name="Media Cone Inner Angle", description="Media Cone Outer Angle", subtype="ANGLE", default=0.0, min=0.0, soft_min=0.0, max=MAX_ANGLE, soft_max=MAX_ANGLE)

    mediaConeOuterGain: FloatProperty(
        name="Media Cone Outer Gain", description="Media Cone Outer Gain", default=0.0, min=0.0, soft_min=0.0)
