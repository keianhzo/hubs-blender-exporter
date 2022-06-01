from ..hubs_component import HubsComponent
from ..types import Category, PanelType, NodeType


class NavMesh(HubsComponent):
    _definition = {
        'name': 'nav-mesh',
        'display_name': 'Navigation Mesh',
        'category': Category.SCENE,
        'node_type': NodeType.NODE,
        'panel_type': PanelType.OBJECT,
        'icon': 'GRID'
    }

    @classmethod
    def poll(cls, context):
        return context.object.type == 'MESH'
