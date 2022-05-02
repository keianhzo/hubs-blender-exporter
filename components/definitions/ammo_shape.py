from bpy.props import FloatProperty, EnumProperty, FloatVectorProperty, BoolProperty
from .hubs_component import HubsComponent
from ..types import Category, PanelType, NodeType


class AmmoShape(HubsComponent):
    _definition = {
        'id': 'ammo-shape',
        'name': 'hubs_component_ammo_shape',
        'display_name': 'Ammo Shape',
        'category': Category.SCENE,
        'node_type': NodeType.NODE,
        'panel_type': PanelType.OBJECT,
        'icon': 'SCENE_DATA'
    }

    type: EnumProperty(
        name="Type",
        description="Type",
        items=[("box", "Box Collider", "A box-shaped primitive collision shape"),
               ("sphere", "Sphere Collider",
                "A primitive collision shape which is represents a sphere"),
               ("hull", "Convex Hull", "A convex hull wrapped around the objects vertices. A good analogy for a convex hull is an elastic membrane or balloon under pressure which is placed around a given set of vertices. When released the membrane will assume the shape of the convex hull."),
               ("mesh", "Mesh Collider", "A shape made of the actual vertecies of the object. This can be expensive for large meshes.")],
        default="hull")

    fit: EnumProperty(
        name="Shape Fitting Mode",
        description="Shape fitting mode",
        items=[("all", "Automatic fit all", "Automatically match the shape to fit the object's vertecies"),
               ("manual", "Manual fit", "Use the manually specified dimensions to define the shape, ignoring the object's vertecies")],
        default="all")

    halfExtents: FloatVectorProperty(
        name="Half Extents", description="Half dimensions of the collider. (Only used when fit is set to \"manual\" and type is set ot \"box\").", unit='LENGTH', subtype="XYZ_LENGTH", default=(0.5, 0.5, 0.5))

    minHalfExtent: FloatProperty(
        name="Min Half Extent", description="The minimum size to use when automatically generating half extents. (Only used when fit is set to \"all\" and type is set ot \"box\")", unit="LENGTH", default=0.0)

    maxHalfExtent: FloatProperty(
        name="Max Half Extent", description="The maximum size to use when automatically generating half extents. (Only used when fit is set to \"all\" and type is set ot \"box\")", unit="LENGTH", default=1000.0)

    sphereRadius: FloatProperty(
        name="Sphere Radius", description="Radius of the sphere collider. (Only used when fit is set to \"manual\" and type is set ot \"sphere\")", unit="LENGTH", default=0.5)

    offset: FloatVectorProperty(
        name="Offset", description="An offset to apply to the collider relative to the object's origin.", unit='LENGTH', subtype="XYZ", default=(0.0, 0.0, 0.0))

    includeInvisible: BoolProperty(
        name="Include Invisible", description="Include invisible objects when generating a collider. (Only used if \"fit\" is set to \"all\")", default=False)
