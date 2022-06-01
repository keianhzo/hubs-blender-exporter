from bpy.props import FloatVectorProperty, FloatProperty, BoolProperty, IntVectorProperty
from ..hubs_component import HubsComponent
from ..types import Category, NodeType, PanelType


class DirectionalLight(HubsComponent):
    _definition = {
        'name': 'directional-light',
        'display_name': 'Directional Light',
        'category': Category.ELEMENTS,
        'node_type': NodeType.NODE,
        'panel_type': PanelType.OBJECT,
        'icon': 'LIGHT_SUN'
    }

    color: FloatVectorProperty(name="Color",
                               description="Color",
                               subtype='COLOR',
                               default=(1.0, 1.0, 1.0, 1.0),
                               size=4,
                               min=0,
                               max=1)

    intensity: FloatProperty(name="Intensity",
                             description="Intensity",
                             default=1.0)

    castShadow: BoolProperty(name="Cast Shadow", default=True)

    shadowMapResolution: IntVectorProperty(name="Shadow Map Resolution",
                                           description="Shadow Map Resolution",
                                           size=2,
                                           subtype="DIRECTION",
                                           default=[512, 512])

    shadowBias: FloatProperty(name="Shadow Bias",
                              description="Shadow Bias",
                              default=1.0)

    shadowRadius: FloatProperty(name="Shadow Radius",
                                description="Shadow Radius",
                                default=1.0)
