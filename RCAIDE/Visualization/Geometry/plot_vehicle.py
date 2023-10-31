## @ingroup Plots-Geometry
# plot_vehicle.py
#
# Created : Mar 2020, M. Clarke
# Modified: Apr 2020, M. Clarke
# Modified: Jul 2020, M. Clarke
# Modified: Jul 2021, E. Botero
# Modified: Oct 2021, M. Clarke
# Modified: Dec 2021, M. Clarke
# Modified: Feb 2022, R. Erhard
# Modified: Mar 2022, R. Erhard
# Modified: Sep 2022, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from Legacy.trunk.S.Core import Data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Legacy.trunk.S.Analyses.Aerodynamics import Vortex_Lattice
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_vortex_distribution    import generate_vortex_distribution 

from RCAIDE.Methods.Aerodynamics.Airfoil.import_airfoil_geometry import import_airfoil_geometry
from RCAIDE.Methods.Aerodynamics.Airfoil.compute_naca_4series_geometry    import compute_naca_4series_geometry
from RCAIDE.Components.Airfoils import Airfoil

from Legacy.trunk.S.Plots.Geometry.plot_vehicle import plot_wing, plot_propeller_wake, generate_fuselage_points, \
     plot_fuselage_geometry, plot_nacelle_geometry



## @ingroup Plots-Geometry
def plot_vehicle(vehicle, elevation_angle = 30,azimuthal_angle = 210, axis_limits = 10, plot_axis = False,
                 save_figure = False, plot_control_points = True, save_filename = "Vehicle_Geometry"):
    """This plots vortex lattice panels created when Fidelity Zero  Aerodynamics
    Routine is initialized

    Assumptions:
    None

    Source:
    None

    Inputs:
    vehicle

    Outputs:
    Plots

    Properties Used:
    N/A
    """

    print("\nPlotting vehicle")

    # unpack vortex distribution
    try:
        VD = vehicle.vortex_distribution
    except:
        settings = Vortex_Lattice().settings
        settings.number_spanwise_vortices  = 25
        settings.number_chordwise_vortices = 5
        settings.spanwise_cosine_spacing   = False
        settings.model_fuselage            = False
        settings.model_nacelle             = False
        VD = generate_vortex_distribution(vehicle,settings)

    # initalize figure
    fig = plt.figure(save_filename)
    fig.set_size_inches(8,8)
    axes = plt.axes(projection='3d')
    axes.view_init(elev= elevation_angle, azim= azimuthal_angle)

    # -------------------------------------------------------------------------
    # PLOT WING
    # -------------------------------------------------------------------------
    wing_face_color = 'darkgrey'
    wing_edge_color = 'grey'
    wing_alpha_val  = 1
    plot_wing(axes,VD,wing_face_color,wing_edge_color,wing_alpha_val)
    if  plot_control_points:
        axes.scatter(VD.XC,VD.YC,VD.ZC, c='r', marker = 'o' )

    # -------------------------------------------------------------------------
    # PLOT WAKES
    # -------------------------------------------------------------------------
    wake_face_color = 'white'
    wake_edge_color = 'blue'
    wake_alpha      = 0.5
    for net in vehicle.networks:
        if "propellers" in net.keys():
            for prop in net.propellers:
                # plot propeller wake
                if prop.Wake.wake_method =="Fidelity_One":
                    plot_propeller_wake(axes, prop, wake_face_color, wake_edge_color, wake_alpha)
        if "lift_rotors" in net.keys():
            for rot in net.lift_rotors:
                # plot rotor wake
                if rot.Wake.wake_method =="Fidelity_One":
                    plot_propeller_wake(axes, rot, wake_face_color, wake_edge_color, wake_alpha)            
            

    # -------------------------------------------------------------------------
    # PLOT FUSELAGE
    # -------------------------------------------------------------------------
    fuselage_face_color = 'grey'
    fuselage_edge_color = 'darkgrey'
    fuselage_alpha      = 1
    for fus in vehicle.fuselages:
        # Generate Fuselage Geometry
        fus_pts = generate_fuselage_points(fus)

        # Plot Fuselage Geometry
        plot_fuselage_geometry(axes,fus_pts,fuselage_face_color,fuselage_edge_color,fuselage_alpha)

    # -------------------------------------------------------------------------
    # PLOT ENGINE
    # -------------------------------------------------------------------------
    nacelle_face_color       = 'darkred'
    nacelle_edge_color       = 'black'
    nacelle_alpha            = 1
    number_of_airfoil_points = 21
    for nacelle in vehicle.nacelles:  
        # Generate Nacelle Geoemtry
        nac_geo = generate_nacelle_points(nacelle,number_of_airfoil_points)
        
        # Plot Nacelle Geometry
        plot_nacelle_geometry(axes,nac_geo,nacelle_face_color,nacelle_edge_color,nacelle_alpha ) 

           
    # -------------------------------------------------------------------------
    # PLOT ENGINE
    # -------------------------------------------------------------------------
    network_face_color       = 'darkred'
    network_edge_color       = 'red'
    network_alpha            = 1
    number_of_airfoil_points = 21
    for network in vehicle.networks:
        plot_network(axes,network,number_of_airfoil_points,network_face_color,network_edge_color,network_alpha )

    axes.set_xlim(0,axis_limits*2)
    axes.set_ylim(-axis_limits,axis_limits)
    axes.set_zlim(-axis_limits,axis_limits)
    
    if not plot_axis:
        plt.axis('off')
        plt.grid(None)
    
    if save_figure:
        fig.savefig(save_filename)
    return


def generate_nacelle_points(nac,tessellation = 24,number_of_airfoil_points = 21):
    """ This generates the coordinate points on the surface of the nacelle

    Assumptions:
    None

    Source:
    None

    Inputs:
    nac                        - Nacelle data structure 
    tessellation               - azimuthal discretization of lofted body 
    number_of_airfoil_points   - discretization of airfoil geometry 
    
    Properties Used:
    N/A 
    """
     
    
    num_nac_segs = len(nac.Segments.keys())   
    theta        = np.linspace(0,2*np.pi,tessellation) 
    
    if num_nac_segs == 0:
        num_nac_segs = int(np.ceil(number_of_airfoil_points/2))
        nac_pts      = np.zeros((num_nac_segs,tessellation,3))
        naf          = nac.Airfoil
        
        if naf.NACA_4_series_flag == True:  
            naf.settings.number_of_points = num_nac_segs
            a_geo        = compute_naca_4series_geometry(naf)
            xpts         = np.repeat(np.atleast_2d(a_geo.x_coordinates[0]).T,tessellation,axis = 1)*nac.length
            zpts         = np.repeat(np.atleast_2d(a_geo.y_coordinates[0]).T,tessellation,axis = 1)*nac.length  
        
        elif naf.coordinate_file != None: 
            naf.settings.number_of_points = num_nac_segs
            a_geo        = import_airfoil_geometry(naf)
            xpts         = np.repeat(np.atleast_2d(np.take(a_geo.x_coordinates,[0],axis=0)).T,tessellation,axis = 1)*nac.length
            zpts         = np.repeat(np.atleast_2d(np.take(a_geo.y_coordinates,[0],axis=0)).T,tessellation,axis = 1)*nac.length
        
        else:
            # if no airfoil defined, use super ellipse as default
            a =  nac.length/2 
            b =  (nac.diameter - nac.inlet_diameter)/2 
            b = np.maximum(b,1E-3) # ensure 
            xpts =  np.repeat(np.atleast_2d(np.linspace(-a,a,num_nac_segs)).T,tessellation,axis = 1) 
            zpts = (np.sqrt((b**2)*(1 - (xpts**2)/(a**2) )))*nac.length 
            xpts = (xpts+a)*nac.length  

        if nac.flow_through: 
            zpts = zpts + nac.inlet_diameter/2  
                
        # create geometry 
        theta_2d = np.repeat(np.atleast_2d(theta),num_nac_segs,axis =0) 
        nac_pts[:,:,0] =  xpts
        nac_pts[:,:,1] =  zpts*np.cos(theta_2d)
        nac_pts[:,:,2] =  zpts*np.sin(theta_2d)  
                
    else:
        nac_pts = np.zeros((num_nac_segs,tessellation,3)) 
        for i_seg in range(num_nac_segs):
            a        = nac.Segments[i_seg].width/2
            b        = nac.Segments[i_seg].height/2
            r        = np.sqrt((b*np.sin(theta))**2  + (a*np.cos(theta))**2)
            nac_ypts = r*np.cos(theta)
            nac_zpts = r*np.sin(theta)
            nac_pts[i_seg,:,0] = nac.Segments[i_seg].percent_x_location*nac.length
            nac_pts[i_seg,:,1] = nac_ypts + nac.Segments[i_seg].percent_y_location*nac.length 
            nac_pts[i_seg,:,2] = nac_zpts + nac.Segments[i_seg].percent_z_location*nac.length  
            
    # rotation about y to orient propeller/rotor to thrust angle
    rot_trans =  nac.nac_vel_to_body()
    rot_trans =  np.repeat( np.repeat(rot_trans[ np.newaxis,:,: ],tessellation,axis=0)[ np.newaxis,:,:,: ],num_nac_segs,axis=0)    
    
    NAC_PTS  =  np.matmul(rot_trans,nac_pts[...,None]).squeeze()  
     
    # translate to body 
    NAC_PTS[:,:,0] = NAC_PTS[:,:,0] + nac.origin[0][0]
    NAC_PTS[:,:,1] = NAC_PTS[:,:,1] + nac.origin[0][1]
    NAC_PTS[:,:,2] = NAC_PTS[:,:,2] + nac.origin[0][2]
    return NAC_PTS

def get_blade_coordinates(prop,n_points,dim,i,aircraftRefFrame=True):
    """ This generates the coordinates of the blade surface for plotting in the aircraft frame (x-back, z-up)

    Assumptions:
    None

    Source:
    None

    Inputs:
    prop             - SUAVE rotor
    n_points         - number of points around airfoils of each blade section
    dim              - number for radial dimension
    i                - blade number
    aircraftRefFrame - boolean to convert the coordinates from rotor frame to aircraft frame 

    Properties Used:
    N/A
    """    
    # unpack
    num_B        = prop.number_of_blades
    airfoils     = prop.Airfoil_Components 
    beta         = prop.twist_distribution + prop.inputs.pitch_command
    a_o          = prop.start_angle
    b            = prop.chord_distribution
    r            = prop.radius_distribution
    MCA          = prop.mid_chord_alignment
    t            = prop.max_thickness_distribution
    a_loc        = prop.airfoil_polar_stations
    origin       = prop.origin
    
    if prop.rotation==1:
        # negative chord and twist to give opposite rotation direction
        b = -b    
        beta = -beta
    
    theta  = np.linspace(0,2*np.pi,num_B+1)[:-1]
    flip_1 =  (np.pi/2)
    flip_2 =  (np.pi/2)

    MCA_2d             = np.repeat(np.atleast_2d(MCA).T,n_points,axis=1)
    b_2d               = np.repeat(np.atleast_2d(b).T  ,n_points,axis=1)
    t_2d               = np.repeat(np.atleast_2d(t).T  ,n_points,axis=1)
    r_2d               = np.repeat(np.atleast_2d(r).T  ,n_points,axis=1)
    airfoil_le_offset  = np.repeat(b[:,None], n_points, axis=1)/2  

    # get airfoil coordinate geometry
    if len(airfoils.keys())>0:
        xpts  = np.zeros((dim,n_points))
        zpts  = np.zeros((dim,n_points))
        max_t = np.zeros(dim)
        for i,airfoil in enumerate(airfoils):
            airfoil.settings.number_of_points = n_points
            geometry     = import_airfoil_geometry(airfoil)
            locs         = np.where(np.array(a_loc) == i )
            xpts[locs]   = geometry.x_coordinates  
            zpts[locs]   = geometry.y_coordinates  
            max_t[locs]  = geometry.thickness_to_chord 

    else: 
        airfoil_new = Airfoil()
        airfoil_new.settings.NACA_4_series_digits = '2410'
        airfoil_new.settings.number_of_points = n_points
        airfoil_data = compute_naca_4series_geometry(airfoil_new)
        xpts         = np.repeat(np.atleast_2d(airfoil_data.x_coordinates) ,dim,axis=0)
        zpts         = np.repeat(np.atleast_2d(airfoil_data.y_coordinates) ,dim,axis=0)
        max_t        = np.repeat(airfoil_data.thickness_to_chord,dim,axis=0)
            
    # store points of airfoil in similar format as Vortex Points (i.e. in vertices)
    max_t2d = np.repeat(np.atleast_2d(max_t).T ,n_points,axis=1)

    xp      = (- MCA_2d + xpts*b_2d - airfoil_le_offset)     # x-coord of airfoil
    yp      = r_2d*np.ones_like(xp)                          # radial location
    zp      = zpts*(t_2d/max_t2d)                            # former airfoil y coord

    prop_vel_to_body = prop.prop_vel_to_body()
    cpts             = len(prop_vel_to_body[:,0,0])
    
    matrix        = np.zeros((len(zp),n_points,3)) # radial location, airfoil pts (same y)
    matrix[:,:,0] = xp
    matrix[:,:,1] = yp
    matrix[:,:,2] = zp
    matrix        = np.repeat(matrix[None,:,:,:], cpts, axis=0)

    
    # ROTATION MATRICES FOR INNER SECTION
    # rotation about y axis to create twist and position blade upright
    trans_1        = np.zeros((dim,3,3))
    trans_1[:,0,0] = np.cos(flip_1 - beta)
    trans_1[:,0,2] = -np.sin(flip_1 - beta)
    trans_1[:,1,1] = 1
    trans_1[:,2,0] = np.sin(flip_1 - beta)
    trans_1[:,2,2] = np.cos(flip_1 - beta)
    trans_1        = np.repeat(trans_1[None,:,:,:], cpts, axis=0)

    # rotation about x axis to create azimuth locations
    trans_2 = np.array([[1 , 0 , 0],
                   [0 , np.cos(theta[i] + a_o + flip_2 ), -np.sin(theta[i] +a_o +  flip_2)],
                   [0,np.sin(theta[i] + a_o + flip_2), np.cos(theta[i] + a_o + flip_2)]])
    trans_2 = np.repeat(trans_2[None,:,:], dim, axis=0)
    trans_2 = np.repeat(trans_2[None,:,:,:], cpts, axis=0)

    # rotation about y to orient propeller/rotor to thrust angle (from propeller frame to aircraft frame)
    trans_3 =  prop_vel_to_body
    trans_3 =  np.repeat(trans_3[:, None,:,: ],dim,axis=1) 
    
    trans     = np.matmul(trans_2,trans_1)
    rot_mat   = np.repeat(trans[:,:, None,:,:],n_points,axis=2)    

    # ---------------------------------------------------------------------------------------------
    # ROTATE POINTS
    if aircraftRefFrame:
        # rotate all points to the thrust angle with trans_3
        mat  =  np.matmul(np.matmul(rot_mat,matrix[...,None]).squeeze(axis=-1), trans_3)
    else:
        # use the rotor frame
        mat  =  np.matmul(rot_mat,matrix[...,None]).squeeze(axis=-1)
    # ---------------------------------------------------------------------------------------------
    # create empty data structure for storing geometry
    G = Data()
    
    # store node points
    G.X  = mat[:,:,:,0] + origin[0][0]
    G.Y  = mat[:,:,:,1] + origin[0][1]
    G.Z  = mat[:,:,:,2] + origin[0][2]
    
    # store points
    G.XA1  = mat[:,:-1,:-1,0] + origin[0][0]
    G.YA1  = mat[:,:-1,:-1,1] + origin[0][1]
    G.ZA1  = mat[:,:-1,:-1,2] + origin[0][2]
    G.XA2  = mat[:,:-1,1:,0]  + origin[0][0]
    G.YA2  = mat[:,:-1,1:,1]  + origin[0][1]
    G.ZA2  = mat[:,:-1,1:,2]  + origin[0][2]

    G.XB1  = mat[:,1:,:-1,0] + origin[0][0]
    G.YB1  = mat[:,1:,:-1,1] + origin[0][1]
    G.ZB1  = mat[:,1:,:-1,2] + origin[0][2]
    G.XB2  = mat[:,1:,1:,0]  + origin[0][0]
    G.YB2  = mat[:,1:,1:,1]  + origin[0][1]
    G.ZB2  = mat[:,1:,1:,2]  + origin[0][2]
    
    return G

def plot_network(axes,network,number_of_airfoil_points,prop_face_color,prop_edge_color,prop_alpha):
    """ This plots the 3D surface of the network

    Assumptions:
    None

    Source:
    None

    Inputs:
    network            - network data structure
    network_face_color - color of panel
    network_edge_color - color of panel edge
    network_alpha      - translucency:  1 = opaque , 0 = transparent

    Properties Used:
    N/A
    """

    if ('propellers' in network.keys()):

        for prop in network.propellers:

            # Generate And Plot Propeller/Rotor Geometry
            plot_propeller_geometry(axes,prop,0,number_of_airfoil_points,prop_face_color,prop_edge_color,prop_alpha)

    if ('lift_rotors' in network.keys()):

        for rotor in network.lift_rotors:

            # Generate and Plot Propeller/Rotor Geometry
            plot_propeller_geometry(axes,rotor,0,number_of_airfoil_points,prop_face_color,prop_edge_color,prop_alpha)

    return 

def plot_propeller_geometry(axes,prop,cpt=0,number_of_airfoil_points = 21,
                            prop_face_color='red',prop_edge_color='darkred',prop_alpha=1):
    """ This plots a 3D surface of the  propeller

    Assumptions:
    None

    Source:
    None

    Inputs:
    axes                       - plotting axes
    prop                       - SUAVE propeller for which to plot the geometry
    cpt                        - control point at which to plot the propeller
    number_of_airfoil_points   - discretization of airfoil geometry 
    

    Properties Used:
    N/A
    """
    num_B     = prop.number_of_blades 
    af_pts    = number_of_airfoil_points-1
    dim       = len(prop.radius_distribution)

    for i in range(num_B):
        G = get_blade_coordinates(prop,number_of_airfoil_points,dim,i)
        # ------------------------------------------------------------------------
        # Plot Propeller Blade
        # ------------------------------------------------------------------------
        for sec in range(dim-1):
            for loc in range(af_pts):
                X = [G.XA1[cpt,sec,loc],
                     G.XB1[cpt,sec,loc],
                     G.XB2[cpt,sec,loc],
                     G.XA2[cpt,sec,loc]]
                Y = [G.YA1[cpt,sec,loc],
                     G.YB1[cpt,sec,loc],
                     G.YB2[cpt,sec,loc],
                     G.YA2[cpt,sec,loc]]
                Z = [G.ZA1[cpt,sec,loc],
                     G.ZB1[cpt,sec,loc],
                     G.ZB2[cpt,sec,loc],
                     G.ZA2[cpt,sec,loc]]
                prop_verts = [list(zip(X, Y, Z))]
                prop_collection = Poly3DCollection(prop_verts)
                prop_collection.set_facecolor(prop_face_color)
                prop_collection.set_edgecolor(prop_edge_color)
                prop_collection.set_alpha(prop_alpha)
                axes.add_collection3d(prop_collection)
    return