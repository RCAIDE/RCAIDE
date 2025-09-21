# RCAIDE/Library/Plots/Geometry/plot_3d_vehicle_vlm_panelization.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Library.Plots.Geometry.plot_3d_vehicle import make_object, make_wireframe, CustomInteractorStyle 

# python imports  
import vtk
import matplotlib.colors as mcolors   
# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
def plot_3d_vehicle_vlm_panelization(vortex_distribution,  
                                     save_figure              = False,
                                     show_wing_control_points = True,
                                     save_filename            = "VLM_Panelization", 
                                     camera_eye_x             = -1, 
                                     camera_eye_y             = -1, 
                                     camera_eye_z             = 0.35,    
                                     panel_opacity            = 1.0,     
                                     edge_opacity             = 1.0,                    
                                     panel_color              = 'grey',                
                                     edge_color               = 'black',    
                                     control_point_color      = 'red',   
                                     control_point_opacity    = 1.0,
                                     control_point_size       = 0.1, 
                                     show_figure              = True):
    """
    Creates a 3D visualization of vehicle vortex lattice method (VLM) panelization.

    Parameters
    ----------
    vehicle : Vehicle
        RCAIDE vehicle data structure containing geometry information
        
    alpha : float, optional
        Transparency value between 0 and 1 (default: 1.0) 
        
    save_figure : bool, optional
        Flag for saving the figure (default: False)
        
    show_wing_control_points : bool, optional
        Flag to display VLM control points (default: True)
        
    save_filename : str, optional
        Name of file for saved figure (default: "VLM_Panelization")
        
    axis_limit : float, optional
        Minimum x-axis plot limit (default: 20)  
        
    show_figure : bool, optional
        Flag to display the figure (default: True)

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Figure handle containing the generated plot

    Notes
    -----
    Creates an interactive 3D visualization showing:
        - VLM panels on lifting surfaces
        - Control points (optional)
        - Customizable view and axis limits
    
    If vehicle's vortex distribution is not available, generates a new one with:
        - 25 spanwise vortices
        - 5 chordwise vortices
        - Linear spanwise spacing
        - No fuselage or nacelle modeling
    
    **Major Assumptions**
    
    * Lifting surfaces are represented by flat panels
    * Control points are at 3/4 chord of each panel
    * Vortex lines are at 1/4 chord of each panel
    
    **Definitions**
    
    'Control Point'
        Location where boundary condition is enforced
    'Vortex Line'
        Line of bound vorticity representing lift
    'Panel'
        Discrete element of lifting surface
    """

    # unpack vortex distribution 
    VD = vortex_distribution      

    # -------------------------------------------------------------------------
    # PLOT VORTEX LATTICE
    # -------------------------------------------------------------------------         
    panel_rgb_color      = mcolors.to_rgb(panel_color)
    edge_rgb_color       = mcolors.to_rgb(edge_color)
    cpt_rgb_color        = mcolors.to_rgb(control_point_color)
    
    renderer = vtk.vtkRenderer()
    make_object(renderer, VD,panel_rgb_color,panel_opacity)
    make_wireframe(renderer, VD,edge_rgb_color,panel_opacity)
      
    if  show_wing_control_points:
        for i in  range(len(VD.XC[0])):
            x =  VD.XC[0][i]
            y =  VD.YC[0][i]
            z =  VD.ZC[0][i] 
        
            # 1. Create a sphere source
            sphereSource = vtk.vtkSphereSource()
            sphereSource.SetRadius(control_point_size)  # Set the radius of the sphere
            sphereSource.SetCenter(x, y, z) # Set the center of the sphere
            sphereSource.SetPhiResolution(30) # Set resolution in phi direction
            sphereSource.SetThetaResolution(30) # Set resolution in theta direction
        
            # 2. Create a mapper
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(sphereSource.GetOutputPort())
            
            # 3. Create an actor
            actor = vtk.vtkActor()
            actor.SetMapper(mapper) 
            actor.GetProperty().SetColor(cpt_rgb_color[0], cpt_rgb_color[1], cpt_rgb_color[2])             
                         
            # 4. Create a renderer
            renderer = vtk.vtkRenderer()
            renderer.AddActor(actor)  
  
    # Set camera and background
    camera = vtk.vtkCamera()
    camera.SetPosition(camera_eye_x, camera_eye_y, camera_eye_z)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 0, 1)

    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()
    renderer.SetBackground(1.0, 1.0, 1.0)  
    
    # 5. Create a render window to display the scene
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(1500, 1500)
    renderWindow.SetWindowName(save_filename)
    
    # 6. Create an interactor to handle user input (mouse, keyboard)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Use the custom interactor style
    custom_style = CustomInteractorStyle()
    renderWindowInteractor.SetInteractorStyle(custom_style)
    
    if save_figure:
        # Create a vtkWindowToImageFilter to capture the render window content
        window_to_image = vtk.vtkWindowToImageFilter()
        window_to_image.SetInput(renderWindow)
        window_to_image.SetInputBufferTypeToRGBA()  # or RGB
        window_to_image.ReadFrontBufferOff()  # Read from back buffer for off-screen rendering
        window_to_image.Update()
        
        # Create a vtkPNGWriter to save the image
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(save_filename + ".png")
        writer.SetInputConnection(window_to_image.GetOutputPort())
        writer.Write() 

    # Start the VTK interactor
    if show_figure:  
        renderWindowInteractor.Initialize()
        renderWindow.Render() # Render the scene initially
        renderWindowInteractor.Start()  
    return  
