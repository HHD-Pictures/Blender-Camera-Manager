bl_info = {
    "name": "Camera Manager",
    "author": "Herohunter Pictures",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Camera Manager",
    "description": "Manage, switch, and render multiple cameras",
    "category": "3D View"
}

import bpy
import os

class CM_OT_AddCamera(bpy.types.Operator):
    bl_idname = "cm.add_camera"
    bl_label = "Add Camera"
    bl_description = "Add a new camera at the current viewport position and angle"

    def execute(self, context):
        for area in context.window.screen.areas:
            if area.type == 'VIEW_3D':
                view3d = area.spaces.active
                if view3d.region_3d.view_perspective != 'CAMERA':
                    view_matrix = view3d.region_3d.view_matrix.copy()
                    view_perspective = view3d.region_3d.view_perspective
                    break
        
        bpy.ops.object.camera_add()
        cam_obj = context.active_object
        
        context.scene.camera = cam_obj
        
        for area in context.window.screen.areas:
            if area.type == 'VIEW_3D':
                view3d = area.spaces.active
                if view_perspective != 'CAMERA':
                    view3d.region_3d.view_matrix = view_matrix
                
                override = context.copy()
                override["area"] = area
                override["region"] = area.regions[-1]
                override["space_data"] = view3d
                bpy.ops.view3d.camera_to_view(override)
                break

        return {'FINISHED'}

class CM_OT_SetActive(bpy.types.Operator):
    bl_idname = "cm.set_active"
    bl_label = "Set Active Camera"

    cam_name: bpy.props.StringProperty()

    def execute(self, context):
        cam_obj = bpy.data.objects.get(self.cam_name)
        if cam_obj:
            context.scene.camera = cam_obj
        return {'FINISHED'}


class CM_OT_RenderAll(bpy.types.Operator):
    bl_idname = "cm.render_all"
    bl_label = "Render All Cameras"
    bl_description = "Render the scene from each camera"

    def execute(self, context):
        scene = context.scene
        original_camera = scene.camera
        
        if bpy.data.filepath:
            blend_dir = os.path.dirname(bpy.data.filepath)
            output_dir = os.path.join(blend_dir, "renders")
        else:
            output_dir = os.path.join(bpy.app.tempdir, "renders")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']
        
        if not cameras:
            self.report({'WARNING'}, "No cameras found in the scene")
            return {'CANCELLED'}

        original_filepath = scene.render.filepath
        original_resolution_x = scene.render.resolution_x
        original_resolution_y = scene.render.resolution_y
        original_percentage = scene.render.resolution_percentage

        try:
            for i, cam in enumerate(cameras):
                self.report({'INFO'}, f"Rendering camera {i+1}/{len(cameras)}: {cam.name}")
                
                scene.camera = cam
                
                context.view_layer.update()
                
                filepath = os.path.join(output_dir, cam.name)
                scene.render.filepath = filepath
                
                bpy.ops.render.render(write_still=True)
                
        except Exception as e:
            self.report({'ERROR'}, f"Rendering failed: {str(e)}")
            return {'CANCELLED'}
        
        finally:
            scene.camera = original_camera
            scene.render.filepath = original_filepath
            scene.render.resolution_x = original_resolution_x
            scene.render.resolution_y = original_resolution_y
            scene.render.resolution_percentage = original_percentage

        self.report({'INFO'}, f"All renders saved to: {output_dir}")
        return {'FINISHED'}


class CM_OT_CycleCameras(bpy.types.Operator):
    bl_idname = "cm.cycle_cameras"
    bl_label = "Cycle Cameras"
    bl_description = "Switch to the next camera in the scene"

    def execute(self, context):
        scene = context.scene
        cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']
        if not cameras:
            return {'CANCELLED'}

        if scene.camera not in cameras:
            scene.camera = cameras[0]
        else:
            idx = cameras.index(scene.camera)
            scene.camera = cameras[(idx + 1) % len(cameras)]
        return {'FINISHED'}


class CM_PT_MainPanel(bpy.types.Panel):
    bl_label = "Camera Manager"
    bl_idname = "CM_PT_mainpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Camera Manager'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        
        layout.operator("cm.add_camera", icon="CAMERA_DATA")

        
        box = layout.box()
        box.label(text="Cameras in Scene:")
        for cam in [obj for obj in scene.objects if obj.type == 'CAMERA']:
            row = box.row()
            row.label(text=cam.name, icon="CAMERA_DATA")
            op = row.operator("cm.set_active", text="Set Active")
            op.cam_name = cam.name

        layout.separator()

        
        layout.operator("cm.render_all", icon="RENDER_STILL")
        layout.operator("cm.cycle_cameras", icon="FILE_REFRESH")


classes = [
    CM_OT_AddCamera,
    CM_OT_SetActive,
    CM_OT_RenderAll,
    CM_OT_CycleCameras,
    CM_PT_MainPanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
