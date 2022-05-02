from ..models import spawn_point
from ..gizmos import HubsGizmo
from ..types import Category, PanelType, NodeType
from .hubs_component import HubsComponent
from bpy.props import BoolProperty
import bpy


class Waypoint(HubsComponent):
    _definition = {
        'id': 'waypoint',
        'name': 'hubs_component_waypoint',
        'display_name': 'Waypoint',
        'category': Category.OBJECT,
        'node_type': NodeType.NODE,
        'panel_type': PanelType.OBJECT,
        'gizmo': 'waypoint',
        'icon': 'spawn-point.png'
    }

    canBeSpawnPoint: BoolProperty(
        name="canBeSpawnPoint",
        description="After each use, this waypoint will be disabled until the previous user moves away from it",
        default=False)

    canBeOccupied: BoolProperty(
        name="canBeOccupied",
        description="After each use, this waypoint will be disabled until the previous user moves away from it",
        default=False)

    canBeClicked: BoolProperty(
        name="canBeClicked",
        description="This waypoint will be visible in pause mode and clicking on it will teleport you to it",
        default=False)

    willDisableMotion: BoolProperty(
        name="willDisableMotion",
        description="Avatars will not be able to move while occupying his waypoint",
        default=False)

    willDisableTeleporting: BoolProperty(
        name="willDisableTeleporting",
        description="Avatars will not be able to teleport while occupying this waypoint",
        default=False)

    willMaintainInitialOrientation: BoolProperty(
        name="willMaintainInitialOrientation",
        description="Instead of rotating to face the same direction as the waypoint, avatars will maintain the orientation they started with before they teleported",
        default=False)

    snapToNavMesh: BoolProperty(
        name="snapToNavMesh",
        description="Avatars will move as close as they can to this waypoint but will not leave the ground",
        default=False)

    @classmethod
    def create_gizmo(cls, obj, gizmo_group):
        widget = gizmo_group.gizmos.new(HubsGizmo.bl_idname)
        setattr(widget, "hba_gizmo_shape", spawn_point.SHAPE)
        widget.setup()
        widget.matrix_basis = obj.matrix_world.normalized()
        widget.line_width = 3
        widget.color = (0.8, 0.8, 0.8)
        widget.alpha = 0.5
        widget.hide = not obj.visible_get()
        widget.hide_select = True
        widget.scale_basis = 1.0
        widget.use_draw_modal = True
        widget.color_highlight = (0.8, 0.8, 0.8)
        widget.alpha_highlight = 1.0

        op = widget.target_set_operator("transform.translate")
        op.constraint_axis = False, False, False
        op.orient_type = 'LOCAL'
        op.release_confirm = True

        def update(obj, gizmo):
            gizmo.matrix_basis = obj.matrix_world.normalized()
            bpy.context.view_layer.update()

        return widget, update
