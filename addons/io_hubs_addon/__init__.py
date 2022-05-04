bl_info = {
    "name": "Hubs Blender Addon",
    "author": "Mozilla Hubs",
    "description": "Tools for developing GLTF assets for Mozilla Hubs",
    "blender": (2, 92, 0),
    "version": (0, 1, 0),
    "location": "",
    "wiki_url": "https://github.com/MozillaReality/hubs-blender-exporter",
    "tracker_url": "https://github.com/MozillaReality/hubs-blender-exporter/issues",
    "support": "COMMUNITY",
    "warning": "",
    "category": "Generic"
}

import sys


# Determine if we are running inside Blender to load dependencies (mostly to allow accesing bl_info from outside the Blender runtime)
if 'blender' in sys.argv[0].lower():
    from .io import gltf_exporter
    from . import (nodes, components)

    def register():
        print('Register Addon')

        gltf_exporter.register()
        nodes.register()
        components.register()

    def unregister():
        components.unregister()
        nodes.unregister()
        gltf_exporter.unregister()

        print('Addon unregistered')

    # called by gltf-blender-io after it has loaded

    glTF2ExportUserExtension = gltf_exporter.glTF2ExportUserExtension

    def register_panel():
        return gltf_exporter.register_export_panel()
