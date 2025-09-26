# Blender-Camera-Manager
A Blender add-on that makes working with multiple cameras easy and efficient.
With this tool you can quickly add cameras **directly from your viewport**, switch between them, cycle through all cameras, and even render the scene from every camera automatically.

---

## Features
- **Add Camera From View**: Creates a new camera at your current 3D View position and orientation.  
- **Set Active Camera**: Quickly switch the active camera from a list of cameras in the scene.  
- **Cycle Cameras**: Switch to the next camera in the scene with one click.  
- **Render All Cameras**: Automatically renders the scene from every camera and saves the images to a `renders/` folder next to your `.blend` file.  

---

## Installation
1. Download the Python file (`camera_manager.py`) from this repository.  
2. In Blender, go to **Edit → Preferences → Add-ons**.  
3. Click **Install…**, then select the `.py` file.  
4. Enable the add-on by checking the box next to **Camera Manager**.

---

## Usage
1. Open the **3D View Sidebar (N key)** → **Camera Manager** tab.  
2. **Add Camera** → creates a camera at your current viewport view.  
3. **Set Active** → click a camera in the list to make it the active camera.  
4. **Cycle Cameras** → flip through cameras one by one.  
5. **Render All** → renders the scene from all cameras automatically. Images are saved in a `renders/` folder alongside your `.blend` file.

---

## Example Workflow
1. Navigate to the desired viewport angle.  
2. Click **Add Camera** → camera spawns exactly at that angle.  
3. Repeat to add multiple cameras.  
4. Use **Cycle Cameras** or **Set Active** to preview shots.  
5. Click **Render All** → get individual renders for all cameras automatically.  

---

## Development
- Built with Blender API (`bpy`) and Python 3.x (shipped with Blender 3.x/4.x).  
