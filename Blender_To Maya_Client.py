bl_info = {
    "name": "Send To Maya",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 83, 0),
    "location": "View3D > Toolbar > Send To Maya",
    "description": "Sends selected meshes or entire scene to Maya",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export",
}

import bpy
import os
import tempfile
import socket

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 12345))
        client_socket.sendall(command.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response)  # Print the response from Maya for debugging

class SendSelectedToMaya(bpy.types.Operator):
    """Send Selected Meshes to Maya"""
    bl_idname = "export.send_selected_to_maya"
    bl_label = "Send Selected"
    
    def execute(self, context):
        # Determine the file path
        blend_filepath = bpy.data.filepath
        directory = os.path.dirname(blend_filepath) if blend_filepath else tempfile.gettempdir()
        filename = "SelectedMeshes.fbx"
        path = os.path.join(directory, filename)
        
        # Export selected meshes as FBX
        bpy.ops.export_scene.fbx(filepath=path, use_selection=True)
        
        # Send command to Maya
        pathToSend = path.replace('\\', '\\\\')
        send_command(f"mayaFbxImport('{pathToSend}')")
        
        self.report({'INFO'}, "Selected meshes sent to Maya")
        return {'FINISHED'}

class SendSceneToMaya(bpy.types.Operator):
    """Send Entire Scene to Maya"""
    bl_idname = "export.send_scene_to_maya"
    bl_label = "Send Scene"
    
    def execute(self, context):
        # Determine the file path
        blend_filepath = bpy.data.filepath
        directory = os.path.dirname(blend_filepath) if blend_filepath else tempfile.gettempdir()
        filename = "EntireScene.fbx"
        path = os.path.join(directory, filename)
        
        # Export the entire scene as FBX
        bpy.ops.export_scene.fbx(filepath=path, use_selection=False)
        
        # Send command to Maya
        pathToSend = path.replace('\\', '\\\\')
        send_command(f"mayaFbxImport('{pathToSend}')")
        
        self.report({'INFO'}, "Entire scene sent to Maya")
        return {'FINISHED'}

class SendToMayaPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Send To Maya"
    bl_idname = "OBJECT_PT_send_to_maya"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Maya"
    
    def draw(self, context):
        layout = self.layout
        layout.operator(SendSelectedToMaya.bl_idname)
        layout.operator(SendSceneToMaya.bl_idname)

def register():
    bpy.utils.register_class(SendSelectedToMaya)
    bpy.utils.register_class(SendSceneToMaya)
    bpy.utils.register_class(SendToMayaPanel)

def unregister():
    bpy.utils.unregister_class(SendSelectedToMaya)
    bpy.utils.unregister_class(SendSceneToMaya)
    bpy.utils.unregister_class(SendToMayaPanel)

if __name__ == "__main__":
    register()