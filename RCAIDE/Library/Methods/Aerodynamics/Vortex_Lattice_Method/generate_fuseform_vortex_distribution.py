# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/generate_fuseform_vortex_distribution.py
# 
# Created:  Apr 2026, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core                                  import Data  
  
# package imports 
import numpy as np
# ----------------------------------------------------------------------
#  generate_fuseform_vortex_distribution
# ----------------------------------------------------------------------
def generate_fuseform_vortex_distribution(VD,fus,n_cw,n_sw,spc,precision):
    """ This generates the vortex distribution points on a fuselage or nacelle component
    Assumptions: 
    If nacelle has segments defined, the mean width and height of the nacelle is used
    Source:   
    None
    
    Inputs:   
    VD                   - vortex distribution
    
    Properties Used:
    N/A
    """    
    # geometry values
    origin     = fus.origin[0]
 
    # ------------------------------------------------
    # Horizontal Fuselage Sections 
    # ------------------------------------------------
    fhs        = Data()        
    fhs.origin = np.zeros((n_sw+1,3))        
    fhs.chord  = np.zeros((n_sw+1))         
    fhs.sweep  = np.zeros((n_sw+1))

    fhs_xa1 = np.zeros(n_cw*n_sw)
    fhs_ya1 = np.zeros(n_cw*n_sw)
    fhs_za1 = np.zeros(n_cw*n_sw)
    fhs_xa2 = np.zeros(n_cw*n_sw)
    fhs_ya2 = np.zeros(n_cw*n_sw)
    fhs_za2 = np.zeros(n_cw*n_sw)
    fhs_xb1 = np.zeros(n_cw*n_sw)
    fhs_yb1 = np.zeros(n_cw*n_sw)
    fhs_zb1 = np.zeros(n_cw*n_sw)
    fhs_yb2 = np.zeros(n_cw*n_sw)
    fhs_xb2 = np.zeros(n_cw*n_sw)
    fhs_zb2 = np.zeros(n_cw*n_sw)
    fhs_xah = np.zeros(n_cw*n_sw)
    fhs_yah = np.zeros(n_cw*n_sw)
    fhs_zah = np.zeros(n_cw*n_sw)
    fhs_xbh = np.zeros(n_cw*n_sw)
    fhs_ybh = np.zeros(n_cw*n_sw)
    fhs_zbh = np.zeros(n_cw*n_sw)
    fhs_xch = np.zeros(n_cw*n_sw)
    fhs_ych = np.zeros(n_cw*n_sw)
    fhs_zch = np.zeros(n_cw*n_sw)
    fhs_xc  = np.zeros(n_cw*n_sw)
    fhs_yc  = np.zeros(n_cw*n_sw)
    fhs_zc  = np.zeros(n_cw*n_sw)
    fhs_xac = np.zeros(n_cw*n_sw)
    fhs_yac = np.zeros(n_cw*n_sw)
    fhs_zac = np.zeros(n_cw*n_sw)
    fhs_xbc = np.zeros(n_cw*n_sw)
    fhs_ybc = np.zeros(n_cw*n_sw)
    fhs_zbc = np.zeros(n_cw*n_sw)
    fhs_x   = np.zeros((n_cw+1)*(n_sw+1))
    fhs_y   = np.zeros((n_cw+1)*(n_sw+1))
    fhs_z   = np.zeros((n_cw+1)*(n_sw+1))      
    

    # ------------------------------------------------
    # Vertical Fuselage Sections 
    # ------------------------------------------------         
    fvs        = Data() 
    fvs.origin = np.zeros((n_sw+1,3))
    fvs.chord  = np.zeros((n_sw+1)) 
    fvs.sweep  = np.zeros((n_sw+1))

    fvs_xa1 = np.zeros(n_cw*n_sw)
    fvs_ya1 = np.zeros(n_cw*n_sw)
    fvs_za1 = np.zeros(n_cw*n_sw)
    fvs_xa2 = np.zeros(n_cw*n_sw)
    fvs_ya2 = np.zeros(n_cw*n_sw)
    fvs_za2 = np.zeros(n_cw*n_sw)
    fvs_xb1 = np.zeros(n_cw*n_sw)
    fvs_yb1 = np.zeros(n_cw*n_sw)
    fvs_zb1 = np.zeros(n_cw*n_sw)
    fvs_yb2 = np.zeros(n_cw*n_sw)
    fvs_xb2 = np.zeros(n_cw*n_sw)
    fvs_zb2 = np.zeros(n_cw*n_sw)
    fvs_xah = np.zeros(n_cw*n_sw)
    fvs_yah = np.zeros(n_cw*n_sw)
    fvs_zah = np.zeros(n_cw*n_sw)
    fvs_xbh = np.zeros(n_cw*n_sw)
    fvs_ybh = np.zeros(n_cw*n_sw)
    fvs_zbh = np.zeros(n_cw*n_sw)
    fvs_xch = np.zeros(n_cw*n_sw)
    fvs_ych = np.zeros(n_cw*n_sw)
    fvs_zch = np.zeros(n_cw*n_sw)
    fvs_xc  = np.zeros(n_cw*n_sw)
    fvs_yc  = np.zeros(n_cw*n_sw)
    fvs_zc  = np.zeros(n_cw*n_sw)
    fvs_xac = np.zeros(n_cw*n_sw)
    fvs_yac = np.zeros(n_cw*n_sw)
    fvs_zac = np.zeros(n_cw*n_sw)
    fvs_xbc = np.zeros(n_cw*n_sw)
    fvs_ybc = np.zeros(n_cw*n_sw)
    fvs_zbc = np.zeros(n_cw*n_sw)
    fvs_x   = np.zeros((n_cw+1)*(n_sw+1))
    fvs_y   = np.zeros((n_cw+1)*(n_sw+1))
    fvs_z   = np.zeros((n_cw+1)*(n_sw+1))    

    # Compute the curvature of the nose/tail given fineness ratio. Curvature is derived from general quadratic equation
    # This method relates the fineness ratio to the quadratic curve formula via a spline fit interpolation
    if isinstance(fus, RCAIDE.Library.Components.Fuselages.Fuselage): 
        vec1               = [2 , 1.5, 1.2 , 1]
        vec2               = [1  ,1.57 , 3.2,  8]
        x                  = np.linspace(0,1,4)
        fus_nose_curvature =  np.interp(np.interp(fus.fineness.nose,vec2,x), x , vec1)
        fus_tail_curvature =  np.interp(np.interp(fus.fineness.tail,vec2,x), x , vec1)
        semispan_h = fus.width * 0.5
        semispan_v = fus.heights.maximum * 0.5
        si         = np.arange(1,((n_sw*2)+2))
        spacing    = np.cos((2*si - 1)/(2*len(si))*np.pi)
        h_array    = semispan_h*spacing[0:int((len(si)+1)/2)][::-1]
        v_array    = semispan_v*spacing[0:int((len(si)+1)/2)][::-1]
        
        if spc == True: # discretize wing using cosine spacing     
            n               = np.linspace(n_sw+1,0,n_sw+1)         # vectorize
            thetan          = n*(np.pi/2)/(n_sw+1)                 # angular stations 
            h_array   = semispan_h*np.cos(thetan)    
            v_array   = semispan_v*np.cos(thetan)      
        else:    
            h_array  = np.linspace(0,semispan_h,n_sw+1)  
            v_array  = np.linspace(0,semispan_h,n_sw+1)   

        for i in range(n_sw+1):
            fhs_cabin_length  = fus.lengths.total - (fus.lengths.nose + fus.lengths.tail)
            fhs.nose_length   = ((1 - ((abs(h_array[i]/semispan_h))**fus_nose_curvature ))**(1/fus_nose_curvature))*fus.lengths.nose
            fhs.tail_length   = ((1 - ((abs(h_array[i]/semispan_h))**fus_tail_curvature ))**(1/fus_tail_curvature))*fus.lengths.tail
            fhs.nose_origin   = fus.lengths.nose - fhs.nose_length
            fhs.origin[i][:]  =  np.array([0 , h_array[i], 0.])  # np.array([fhs.nose_origin , h_array[i], 0.]) # Local origin
            fhs.chord[i]      = fus.lengths.total #fhs_cabin_length + fhs.nose_length + fhs.tail_length

            fvs_cabin_length  = fus.lengths.total - (fus.lengths.nose + fus.lengths.tail)
            fvs.nose_length   = ((1 - ((abs(v_array[i]/semispan_v))**fus_nose_curvature ))**(1/fus_nose_curvature))*fus.lengths.nose
            fvs.tail_length   = ((1 - ((abs(v_array[i]/semispan_v))**fus_tail_curvature ))**(1/fus_tail_curvature))*fus.lengths.tail
            fvs.nose_origin   = fus.lengths.nose - fvs.nose_length
            fvs.origin[i][:]  = np.array([origin[0] + fvs.nose_origin , origin[1] , origin[2]+  v_array[i]])
            fvs.chord[i]      = fvs_cabin_length + fvs.nose_length + fvs.tail_length

        fhs.sweep[:] = np.concatenate([np.arctan((fhs.origin[:,0][1:] - fhs.origin[:,0][:-1])/(fhs.origin[:,1][1:]  - fhs.origin[:,1][:-1])) ,np.zeros(1)])
        fvs.sweep[:] = np.concatenate([np.arctan((fvs.origin[:,0][1:] - fvs.origin[:,0][:-1])/(fvs.origin[:,2][1:]  - fvs.origin[:,2][:-1])) ,np.zeros(1)])

    # ---------------------------------------------------------------------------------------
    # STEP 9: Define coordinates of panels horseshoe vortices and control points  
    # ---------------------------------------------------------------------------------------        
    fhs_eta_a = h_array[:-1] 
    fhs_eta_b = h_array[1:]            
    fhs_del_y = h_array[1:] - h_array[:-1]
    fhs_eta   = h_array[1:] - fhs_del_y/2

    fvs_eta_a = v_array[:-1] 
    fvs_eta_b = v_array[1:]                  
    fvs_del_y = v_array[1:] - v_array[:-1]
    fvs_eta   = v_array[1:] - fvs_del_y/2 

    fhs_cs = np.concatenate([fhs.chord,fhs.chord])
    fvs_cs = np.concatenate([fvs.chord,fvs.chord])
    
    fus_h_area = 0
    fus_v_area = 0    

    # define coordinates of horseshoe vortices and control points       
    for idx_y in range(n_sw):  
        idx_x = np.arange(n_cw)
        
        # ------------------------------------------------
        # Horizontal Fuselage Sections 
        # ------------------------------------------------
        delta_x_a = fhs.chord[idx_y]/n_cw      
        delta_x_b = fhs.chord[idx_y + 1]/n_cw    
        delta_x   = (fhs.chord[idx_y]+fhs.chord[idx_y + 1])/(2*n_cw)

        fhs_xi_a1 = fhs.origin[idx_y][0] + delta_x_a*idx_x                    # x coordinate of top left corner of panel
        fhs_xi_ah = fhs.origin[idx_y][0] + delta_x_a*idx_x + delta_x_a*0.25   # x coordinate of left corner of panel
        fhs_xi_a2 = fhs.origin[idx_y][0] + delta_x_a*idx_x + delta_x_a        # x coordinate of bottom left corner of bound vortex 
        fhs_xi_ac = fhs.origin[idx_y][0] + delta_x_a*idx_x + delta_x_a*0.75   # x coordinate of bottom left corner of control point vortex  
        fhs_xi_b1 = fhs.origin[idx_y+1][0] + delta_x_b*idx_x                  # x coordinate of top right corner of panel      
        fhs_xi_bh = fhs.origin[idx_y+1][0] + delta_x_b*idx_x + delta_x_b*0.25 # x coordinate of right corner of bound vortex         
        fhs_xi_b2 = fhs.origin[idx_y+1][0] + delta_x_b*idx_x + delta_x_b      # x coordinate of bottom right corner of panel
        fhs_xi_bc = fhs.origin[idx_y+1][0] + delta_x_b*idx_x + delta_x_b*0.75 # x coordinate of bottom right corner of control point vortex         
        fhs_xi_c  = (fhs.origin[idx_y][0] + fhs.origin[idx_y+1][0])/2  + delta_x*idx_x + delta_x*0.75   # x coordinate three-quarter chord control point for each panel
        fhs_xi_ch = (fhs.origin[idx_y][0] + fhs.origin[idx_y+1][0])/2  + delta_x*idx_x + delta_x*0.25   # x coordinate center of bound vortex of each panel 
 
        fhs_xa1[idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_a1                       + fus.origin[0][0]  
        fhs_ya1[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta_a[idx_y]  + fus.origin[0][1]  
        fhs_za1[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]
        fhs_xa2[idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_a2                       + fus.origin[0][0]  
        fhs_ya2[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta_a[idx_y]  + fus.origin[0][1] 
        fhs_za2[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]      
        fhs_xb1[idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_b1                       + fus.origin[0][0]  
        fhs_yb1[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta_b[idx_y]  + fus.origin[0][1] 
        fhs_zb1[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]
        fhs_xb2[idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_b2                       + fus.origin[0][0] 
        fhs_yb2[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta_b[idx_y]  + fus.origin[0][1] 
        fhs_zb2[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]       
        fhs_xah[idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_ah                       + fus.origin[0][0]   
        fhs_yah[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta_a[idx_y]  + fus.origin[0][1]  
        fhs_zah[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]             
        fhs_xbh[idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_bh                       + fus.origin[0][0] 
        fhs_ybh[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta_b[idx_y]  + fus.origin[0][1]  
        fhs_zbh[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]    
        fhs_xch[idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_ch                       + fus.origin[0][0]  
        fhs_ych[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta[idx_y]    + fus.origin[0][1]                
        fhs_zch[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]     
        fhs_xc [idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_c                        + fus.origin[0][0]  
        fhs_yc [idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta[idx_y]    + fus.origin[0][1]  
        fhs_zc [idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]       
        fhs_xac[idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_ac                       + fus.origin[0][0]  
        fhs_yac[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta_a[idx_y]  + fus.origin[0][1]
        fhs_zac[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]
        fhs_xbc[idx_y*n_cw:(idx_y+1)*n_cw] = fhs_xi_bc                       + fus.origin[0][0]  
        fhs_ybc[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fhs_eta_b[idx_y]  + fus.origin[0][1]                             
        fhs_zbc[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][2]              
        fhs_x[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = np.concatenate([fhs_xi_a1,np.array([fhs_xi_a2[-1]])]) + fus.origin[0][0]  
        fhs_y[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = np.ones(n_cw+1)*fhs_eta_a[idx_y]  + fus.origin[0][1]                             
        fhs_z[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = np.zeros(n_cw+1)                  + fus.origin[0][2]

        fus_h_area += ((fhs.chord[idx_y]+fhs.chord[idx_y + 1])/2)*(fhs_eta_b[idx_y] - fhs_eta_a[idx_y])

        # store this strip's discretization information
        LE_inds        = np.full(n_cw, False)
        TE_inds        = np.full(n_cw, False)
        LE_inds[0]     = True
        TE_inds[-1]    = True
        
        RNMAX          = np.ones(n_cw, np.int16)*n_cw
        panel_numbers  = np.linspace(1,n_cw,n_cw, dtype=np.int16)
        exposed_leading_edge_flag = 1
        
        VD.leading_edge_indices      = np.append(VD.leading_edge_indices   , LE_inds       ) 
        VD.trailing_edge_indices     = np.append(VD.trailing_edge_indices  , TE_inds       )            
        VD.panels_per_strip          = np.append(VD.panels_per_strip       , RNMAX         )
        VD.chordwise_panel_number    = np.append(VD.chordwise_panel_number , panel_numbers )   
        VD.exposed_leading_edge_flag = np.append(VD.exposed_leading_edge_flag, exposed_leading_edge_flag)


        LE_inds        = np.full(n_cw, False)
        TE_inds        = np.full(n_cw, False)
        LE_inds[0]     = True
        TE_inds[-1]    = True
        
        RNMAX          = np.ones(n_cw, np.int16)*n_cw
        panel_numbers  = np.linspace(1,n_cw,n_cw, dtype=np.int16)
        exposed_leading_edge_flag = 1
        
        VD.leading_edge_indices      = np.append(VD.leading_edge_indices   , LE_inds       ) 
        VD.trailing_edge_indices     = np.append(VD.trailing_edge_indices  , TE_inds       )            
        VD.panels_per_strip          = np.append(VD.panels_per_strip       , RNMAX         )
        VD.chordwise_panel_number    = np.append(VD.chordwise_panel_number , panel_numbers )   
        VD.exposed_leading_edge_flag = np.append(VD.exposed_leading_edge_flag, exposed_leading_edge_flag)
     

        ## ------------------------------------------------        
        ## Vertical Fuselage Sections 
        ## ------------------------------------------------                   
        #delta_x_a = fvs.chord[idx_y]/n_cw      
        #delta_x_b = fvs.chord[idx_y + 1]/n_cw    
        #delta_x   = (fvs.chord[idx_y]+fvs.chord[idx_y + 1])/(2*n_cw)   

        #fvs_xi_a1 = fvs.origin[idx_y][0] + delta_x_a*idx_x                    # z coordinate of top left corner of panel
        #fvs_xi_ah = fvs.origin[idx_y][0] + delta_x_a*idx_x + delta_x_a*0.25   # z coordinate of left corner of panel
        #fvs_xi_a2 = fvs.origin[idx_y][0] + delta_x_a*idx_x + delta_x_a        # z coordinate of bottom left corner of bound vortex 
        #fvs_xi_ac = fvs.origin[idx_y][0] + delta_x_a*idx_x + delta_x_a*0.75   # z coordinate of bottom left corner of control point vortex  
        #fvs_xi_b1 = fvs.origin[idx_y+1][0] + delta_x_b*idx_x                    # z coordinate of top right corner of panel      
        #fvs_xi_bh = fvs.origin[idx_y+1][0] + delta_x_b*idx_x + delta_x_b*0.25   # z coordinate of right corner of bound vortex         
        #fvs_xi_b2 = fvs.origin[idx_y+1][0] + delta_x_b*idx_x + delta_x_b        # z coordinate of bottom right corner of panel
        #fvs_xi_bc = fvs.origin[idx_y+1][0] + delta_x_b*idx_x + delta_x_b*0.75   # z coordinate of bottom right corner of control point vortex         
        #fvs_xi_c  = (fvs.origin[idx_y][0] + fvs.origin[idx_y+1][0])/2 + delta_x *idx_x + delta_x*0.75     # z coordinate three-quarter chord control point for each panel
        #fvs_xi_ch = (fvs.origin[idx_y][0] + fvs.origin[idx_y+1][0])/2 + delta_x *idx_x + delta_x*0.25     # z coordinate center of bound vortex of each panel 


        #fvs_xa1[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_a1                       + fus.origin[0][0]  
        #fvs_za1[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta_a[idx_y]  + fus.origin[0][2]  
        #fvs_ya1[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][1]
        #fvs_xa2[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_a2                       + fus.origin[0][0]  
        #fvs_za2[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta_a[idx_y]  + fus.origin[0][2] 
        #fvs_ya2[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][1]      
        #fvs_xb1[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_b1                       + fus.origin[0][0]  
        #fvs_zb1[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta_b[idx_y]  + fus.origin[0][2] 
        #fvs_yb1[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][1]
        #fvs_xb2[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_b2                       + fus.origin[0][0] 
        #fvs_zb2[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta_b[idx_y]  + fus.origin[0][2] 
        #fvs_yb2[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][1]       
        #fvs_xah[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_ah                       + fus.origin[0][0]   
        #fvs_zah[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta_a[idx_y]  + fus.origin[0][2]  
        #fvs_yah[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][1]             
        #fvs_xbh[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_bh                       + fus.origin[0][0] 
        #fvs_zbh[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta_b[idx_y]  + fus.origin[0][2]  
        #fvs_ybh[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][1]    
        #fvs_xch[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_ch                       + fus.origin[0][0]  
        #fvs_zch[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta[idx_y]    + fus.origin[0][2]                
        #fvs_ych[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][1]       
        #fvs_xac[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_ac                       + fus.origin[0][0]  
        #fvs_zac[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta_a[idx_y]  + fus.origin[0][2]
        #fvs_yac[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][1]
        #fvs_xbc[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_bc                       + fus.origin[0][0]  
        #fvs_zbc[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta_b[idx_y]  + fus.origin[0][2]                             
        #fvs_ybc[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                  + fus.origin[0][1]    
        
        #fvs_xc[idx_y*n_cw:(idx_y+1)*n_cw] = fvs_xi_c                       + fus.origin[0][0]  
        #fvs_zc[idx_y*n_cw:(idx_y+1)*n_cw] = np.ones(n_cw)*fvs_eta[idx_y]   + fus.origin[0][2]  
        #fvs_yc[idx_y*n_cw:(idx_y+1)*n_cw] = np.zeros(n_cw)                 + fus.origin[0][1]  
        #fvs_x[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = np.concatenate([fvs_xi_a1,np.array([fvs_xi_a2[-1]])]) + fus.origin[0][0]  
        #fvs_z[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = np.ones(n_cw+1)*fvs_eta_a[idx_y] + fus.origin[0][2]               
        #fvs_y[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = np.zeros(n_cw+1)                 + fus.origin[0][1]
        
        #fus_v_area += ((fvs.chord[idx_y]+fvs.chord[idx_y + 1])/2)*(fvs_eta_b[idx_y] - fvs_eta_a[idx_y])
        
        ## store this strip's discretization information
        #LE_inds        = np.full(n_cw, False)
        #TE_inds        = np.full(n_cw, False)
        #LE_inds[0]     = True
        #TE_inds[-1]    = True
        
        #RNMAX          = np.ones(n_cw, np.int16)*n_cw
        #panel_numbers  = np.linspace(1,n_cw,n_cw, dtype=np.int16)
        #exposed_leading_edge_flag = 1
        
        #VD.leading_edge_indices      = np.append(VD.leading_edge_indices   , LE_inds       ) 
        #VD.trailing_edge_indices     = np.append(VD.trailing_edge_indices  , TE_inds       )            
        #VD.panels_per_strip          = np.append(VD.panels_per_strip       , RNMAX         )
        #VD.chordwise_panel_number    = np.append(VD.chordwise_panel_number , panel_numbers )   
        #VD.exposed_leading_edge_flag = np.append(VD.exposed_leading_edge_flag, exposed_leading_edge_flag)
        
        

        #LE_inds        = np.full(n_cw, False)
        #TE_inds        = np.full(n_cw, False)
        #LE_inds[0]     = True
        #TE_inds[-1]    = True
        
        #RNMAX          = np.ones(n_cw, np.int16)*n_cw
        #panel_numbers  = np.linspace(1,n_cw,n_cw, dtype=np.int16)
        #exposed_leading_edge_flag = 1
        
        #VD.leading_edge_indices      = np.append(VD.leading_edge_indices   , LE_inds       ) 
        #VD.trailing_edge_indices     = np.append(VD.trailing_edge_indices  , TE_inds       )            
        #VD.panels_per_strip          = np.append(VD.panels_per_strip       , RNMAX         )
        #VD.chordwise_panel_number    = np.append(VD.chordwise_panel_number , panel_numbers )   
        #VD.exposed_leading_edge_flag = np.append(VD.exposed_leading_edge_flag, exposed_leading_edge_flag) 
    
    # ------------------------------------------------     
    # Horizontal Fuselage Sections 
    # ------------------------------------------------  
    # xyz positions for the right side of this fuselage's outermost panels
    fhs_x[-(n_cw+1):] = np.concatenate([fhs_xi_b1,np.array([fhs_xi_b2[-1]])])+ fus.origin[0][0]  
    fhs_y[-(n_cw+1):] = np.ones(n_cw+1)*fhs_eta_b[idx_y]  + fus.origin[0][1]                             
    fhs_z[-(n_cw+1):] = np.zeros(n_cw+1)                  + fus.origin[0][2]
    fhs_cs =  (fhs.chord[:-1]+fhs.chord[1:])/2 
    
    VD.wing_areas.append(np.array(fus_h_area, dtype=precision))
    VD.wing_areas.append(np.array(fus_h_area, dtype=precision))
    VD.symmetric_wings = np.append(VD.symmetric_wings,True)   
    VD.vertical_wing =  np.append(VD.vertical_wing, int(0)) 
    
    # store points of horizontal section of fuselage 
    fhs_cs  = np.concatenate([fhs_cs, fhs_cs]) 
    fhs_xah = np.concatenate([fhs_xah, fhs_xah])
    fhs_yah = np.concatenate([fhs_yah,-fhs_yah])
    fhs_zah = np.concatenate([fhs_zah, fhs_zah])
    fhs_xbh = np.concatenate([fhs_xbh, fhs_xbh])
    fhs_ybh = np.concatenate([fhs_ybh,-fhs_ybh])
    fhs_zbh = np.concatenate([fhs_zbh, fhs_zbh])
    fhs_xch = np.concatenate([fhs_xch, fhs_xch])
    fhs_ych = np.concatenate([fhs_ych,-fhs_ych])
    fhs_zch = np.concatenate([fhs_zch, fhs_zch])
    fhs_xa1 = np.concatenate([fhs_xa1, fhs_xa1])
    fhs_ya1 = np.concatenate([fhs_ya1,-fhs_ya1])
    fhs_za1 = np.concatenate([fhs_za1, fhs_za1])
    fhs_xa2 = np.concatenate([fhs_xa2, fhs_xa2])
    fhs_ya2 = np.concatenate([fhs_ya2,-fhs_ya2])
    fhs_za2 = np.concatenate([fhs_za2, fhs_za2])
    fhs_xb1 = np.concatenate([fhs_xb1, fhs_xb1])
    fhs_yb1 = np.concatenate([fhs_yb1,-fhs_yb1])    
    fhs_zb1 = np.concatenate([fhs_zb1, fhs_zb1])
    fhs_xb2 = np.concatenate([fhs_xb2, fhs_xb2])
    fhs_yb2 = np.concatenate([fhs_yb2,-fhs_yb2])            
    fhs_zb2 = np.concatenate([fhs_zb2, fhs_zb2])
    fhs_xac = np.concatenate([fhs_xac, fhs_xac])
    fhs_yac = np.concatenate([fhs_yac,-fhs_yac])
    fhs_zac = np.concatenate([fhs_zac, fhs_zac])            
    fhs_xbc = np.concatenate([fhs_xbc, fhs_xbc])
    fhs_ybc = np.concatenate([fhs_ybc,-fhs_ybc])
    fhs_zbc = np.concatenate([fhs_zbc, fhs_zbc])
    fhs_xc  = np.concatenate([fhs_xc , fhs_xc ])
    fhs_yc  = np.concatenate([fhs_yc ,-fhs_yc])
    fhs_zc  = np.concatenate([fhs_zc , fhs_zc ])     
    fhs_x   = np.concatenate([fhs_x  , fhs_x  ])
    fhs_y   = np.concatenate([fhs_y  ,-fhs_y ])
    fhs_z   = np.concatenate([fhs_z  , fhs_z  ])   

    # increment fuslage lifting surface sections  
    VD.n_f     += 2    
    VD.n_cp    += len(fhs_xch)
    VD.n_w     += 2 
    VD.counter += 1
    
    # store this fuselage's discretization information 
    n_panels         = n_sw*n_cw
    first_panel_ind  = VD.XAH.size
    first_strip_ind  = [VD.chordwise_breaks.size, VD.chordwise_breaks.size+n_sw]
    chordwise_breaks =  first_panel_ind + np.arange(0,2*n_panels)[0::n_cw]        
    
    VD.chordwise_breaks = np.append(VD.chordwise_breaks, np.int32(chordwise_breaks))
    VD.spanwise_breaks  = np.append(VD.spanwise_breaks , np.int32(first_strip_ind ))            
    VD.n_sw             = np.append(VD.n_sw            , np.int16([n_sw, n_sw])    )
    VD.n_cw             = np.append(VD.n_cw            , np.int16([n_cw, n_cw])    )
    VD.surface_ID       = np.append(VD.surface_ID      , np.ones(len(fhs_xch)) * VD.counter)
    VD.surface_ID_full  = np.append(VD.surface_ID_full , np.ones(((n_sw+1)*(n_cw+1))*2) * VD.counter)

    VD.vortex_lift.append(False)
    VD.vortex_lift.append(False)   
    
    # Store fuselage in vehicle vector  
    VD.XAH    = np.append(VD.XAH  , np.array(fhs_xah  , dtype=precision))
    VD.YAH    = np.append(VD.YAH  , np.array(fhs_yah  , dtype=precision))
    VD.ZAH    = np.append(VD.ZAH  , np.array(fhs_zah  , dtype=precision))
    VD.XBH    = np.append(VD.XBH  , np.array(fhs_xbh  , dtype=precision))
    VD.YBH    = np.append(VD.YBH  , np.array(fhs_ybh  , dtype=precision))
    VD.ZBH    = np.append(VD.ZBH  , np.array(fhs_zbh  , dtype=precision))
    VD.XCH    = np.append(VD.XCH  , np.array(fhs_xch  , dtype=precision))
    VD.YCH    = np.append(VD.YCH  , np.array(fhs_ych  , dtype=precision))
    VD.ZCH    = np.append(VD.ZCH  , np.array(fhs_zch  , dtype=precision))
    VD.XA1    = np.append(VD.XA1  , np.array(fhs_xa1  , dtype=precision))
    VD.YA1    = np.append(VD.YA1  , np.array(fhs_ya1  , dtype=precision))
    VD.ZA1    = np.append(VD.ZA1  , np.array(fhs_za1  , dtype=precision))
    VD.XA2    = np.append(VD.XA2  , np.array(fhs_xa2  , dtype=precision))
    VD.YA2    = np.append(VD.YA2  , np.array(fhs_ya2  , dtype=precision))
    VD.ZA2    = np.append(VD.ZA2  , np.array(fhs_za2  , dtype=precision))
    VD.XB1    = np.append(VD.XB1  , np.array(fhs_xb1  , dtype=precision))
    VD.YB1    = np.append(VD.YB1  , np.array(fhs_yb1  , dtype=precision))
    VD.ZB1    = np.append(VD.ZB1  , np.array(fhs_zb1  , dtype=precision))
    VD.XB2    = np.append(VD.XB2  , np.array(fhs_xb2  , dtype=precision))
    VD.YB2    = np.append(VD.YB2  , np.array(fhs_yb2  , dtype=precision))
    VD.ZB2    = np.append(VD.ZB2  , np.array(fhs_zb2  , dtype=precision))
    VD.XAC    = np.append(VD.XAC  , np.array(fhs_xac  , dtype=precision))
    VD.YAC    = np.append(VD.YAC  , np.array(fhs_yac  , dtype=precision))
    VD.ZAC    = np.append(VD.ZAC  , np.array(fhs_zac  , dtype=precision))
    VD.XBC    = np.append(VD.XBC  , np.array(fhs_xbc  , dtype=precision))
    VD.YBC    = np.append(VD.YBC  , np.array(fhs_ybc  , dtype=precision))
    VD.ZBC    = np.append(VD.ZBC  , np.array(fhs_zbc  , dtype=precision))
    VD.XC     = np.append(VD.XC   , np.array(fhs_xc   , dtype=precision))
    VD.YC     = np.append(VD.YC   , np.array(fhs_yc   , dtype=precision))
    VD.ZC     = np.append(VD.ZC   , np.array(fhs_zc   , dtype=precision))
    VD.CS     = np.append(VD.CS   , np.array(fhs_cs   , dtype=precision))
    VD.X      = np.append(VD.X    , np.array(fhs_x    , dtype=precision))
    VD.Y      = np.append(VD.Y    , np.array(fhs_y    , dtype=precision))
    VD.Z      = np.append(VD.Z    , np.array(fhs_z    , dtype=precision))   

    ## ------------------------------------------------     
    ## Vertical Fuselage Sections 
    ## ------------------------------------------------

    #fvs_x[-(n_cw+1):] = np.concatenate([fvs_xi_a1,np.array([fvs_xi_a2[-1]])]) + fus.origin[0][0]  
    #fvs_z[-(n_cw+1):] = np.ones(n_cw+1)*fvs_eta_a[idx_y] + fus.origin[0][2]               
    #fvs_y[-(n_cw+1):] = np.zeros(n_cw+1)                 + fus.origin[0][1]   
    #fvs_cs =  (fvs.chord[:-1]+fvs.chord[1:])/2    
    
    #VD.wing_areas.append(np.array(fus_v_area, dtype=precision))
    #VD.wing_areas.append(np.array(fus_v_area, dtype=precision))
    #VD.symmetric_wings = np.append(VD.symmetric_wings,True)    
    #VD.vertical_wing =  np.append(VD.vertical_wing, int(1)) 

    ## store points of horizontal section of fuselage  
    #fvs_cs  = np.concatenate([fvs_cs, fvs_cs])
    #fvs_xah = np.concatenate([fvs_xah, fvs_xah])
    #fvs_yah = np.concatenate([fvs_yah, fvs_yah])
    #fvs_zah = np.concatenate([fvs_zah,-fvs_zah])
    #fvs_xbh = np.concatenate([fvs_xbh, fvs_xbh])
    #fvs_ybh = np.concatenate([fvs_ybh, fvs_ybh])
    #fvs_zbh = np.concatenate([fvs_zbh,-fvs_zbh])
    #fvs_xch = np.concatenate([fvs_xch, fvs_xch])
    #fvs_ych = np.concatenate([fvs_ych, fvs_ych])
    #fvs_zch = np.concatenate([fvs_zch,-fvs_zch])
    #fvs_xa1 = np.concatenate([fvs_xa1, fvs_xa1])
    #fvs_ya1 = np.concatenate([fvs_ya1, fvs_ya1])
    #fvs_za1 = np.concatenate([fvs_za1,-fvs_za1])
    #fvs_xa2 = np.concatenate([fvs_xa2, fvs_xa2])
    #fvs_ya2 = np.concatenate([fvs_ya2, fvs_ya2])
    #fvs_za2 = np.concatenate([fvs_za2,-fvs_za2])
    #fvs_xb1 = np.concatenate([fvs_xb1, fvs_xb1])
    #fvs_yb1 = np.concatenate([fvs_yb1, fvs_yb1])    
    #fvs_zb1 = np.concatenate([fvs_zb1,-fvs_zb1])
    #fvs_xb2 = np.concatenate([fvs_xb2, fvs_xb2])
    #fvs_yb2 = np.concatenate([fvs_yb2, fvs_yb2])            
    #fvs_zb2 = np.concatenate([fvs_zb2,-fvs_zb2])
    #fvs_xac = np.concatenate([fvs_xac, fvs_xac])
    #fvs_yac = np.concatenate([fvs_yac, fvs_yac])
    #fvs_zac = np.concatenate([fvs_zac,-fvs_zac])            
    #fvs_xbc = np.concatenate([fvs_xbc, fvs_xbc])
    #fvs_ybc = np.concatenate([fvs_ybc, fvs_ybc])
    #fvs_zbc = np.concatenate([fvs_zbc,-fvs_zbc])
    #fvs_xc  = np.concatenate([fvs_xc , fvs_xc ])
    #fvs_yc  = np.concatenate([fvs_yc , fvs_yc])
    #fvs_zc  = np.concatenate([fvs_zc ,-fvs_zc ])     
    #fvs_x   = np.concatenate([fvs_x  , fvs_x  ])
    #fvs_y   = np.concatenate([fvs_y  , fvs_y ])
    #fvs_z   = np.concatenate([fvs_z  ,-fvs_z  ])   

    ## increment fuslage lifting surface sections  
    #VD.n_f     += 2    
    #VD.n_cp    += len(fvs_xch)
    #VD.n_w     += 2 
    #VD.counter += 1
    
    ## store this fuselage's discretization information 
    #n_panels         = n_sw*n_cw
    #first_panel_ind  = VD.XAH.size
    #first_strip_ind  = [VD.chordwise_breaks.size, VD.chordwise_breaks.size+n_sw]
    #chordwise_breaks =  first_panel_ind + np.arange(0,2*n_panels)[0::n_cw]        
    
    #VD.chordwise_breaks = np.append(VD.chordwise_breaks, np.int32(chordwise_breaks))
    #VD.spanwise_breaks  = np.append(VD.spanwise_breaks , np.int32(first_strip_ind ))            
    #VD.n_sw             = np.append(VD.n_sw            , np.int16([n_sw, n_sw])    )
    #VD.n_cw             = np.append(VD.n_cw            , np.int16([n_cw, n_cw])    )
    #VD.surface_ID       = np.append(VD.surface_ID      , np.ones(len(fvs_xch)) * VD.counter)
    #VD.surface_ID_full  = np.append(VD.surface_ID_full , np.ones(((n_sw+1)*(n_cw+1))*2) * VD.counter)

    #VD.vortex_lift.append(False)
    #VD.vortex_lift.append(False)   
    
    ## Store fuselage in vehicle vector  
    #VD.XAH    = np.append(VD.XAH  , np.array(fvs_xah  , dtype=precision))
    #VD.YAH    = np.append(VD.YAH  , np.array(fvs_yah  , dtype=precision))
    #VD.ZAH    = np.append(VD.ZAH  , np.array(fvs_zah  , dtype=precision))
    #VD.XBH    = np.append(VD.XBH  , np.array(fvs_xbh  , dtype=precision))
    #VD.YBH    = np.append(VD.YBH  , np.array(fvs_ybh  , dtype=precision))
    #VD.ZBH    = np.append(VD.ZBH  , np.array(fvs_zbh  , dtype=precision))
    #VD.XCH    = np.append(VD.XCH  , np.array(fvs_xch  , dtype=precision))
    #VD.YCH    = np.append(VD.YCH  , np.array(fvs_ych  , dtype=precision))
    #VD.ZCH    = np.append(VD.ZCH  , np.array(fvs_zch  , dtype=precision))
    #VD.XA1    = np.append(VD.XA1  , np.array(fvs_xa1  , dtype=precision))
    #VD.YA1    = np.append(VD.YA1  , np.array(fvs_ya1  , dtype=precision))
    #VD.ZA1    = np.append(VD.ZA1  , np.array(fvs_za1  , dtype=precision))
    #VD.XA2    = np.append(VD.XA2  , np.array(fvs_xa2  , dtype=precision))
    #VD.YA2    = np.append(VD.YA2  , np.array(fvs_ya2  , dtype=precision))
    #VD.ZA2    = np.append(VD.ZA2  , np.array(fvs_za2  , dtype=precision))
    #VD.XB1    = np.append(VD.XB1  , np.array(fvs_xb1  , dtype=precision))
    #VD.YB1    = np.append(VD.YB1  , np.array(fvs_yb1  , dtype=precision))
    #VD.ZB1    = np.append(VD.ZB1  , np.array(fvs_zb1  , dtype=precision))
    #VD.XB2    = np.append(VD.XB2  , np.array(fvs_xb2  , dtype=precision))
    #VD.YB2    = np.append(VD.YB2  , np.array(fvs_yb2  , dtype=precision))
    #VD.ZB2    = np.append(VD.ZB2  , np.array(fvs_zb2  , dtype=precision))
    #VD.XAC    = np.append(VD.XAC  , np.array(fvs_xac  , dtype=precision))
    #VD.YAC    = np.append(VD.YAC  , np.array(fvs_yac  , dtype=precision))
    #VD.ZAC    = np.append(VD.ZAC  , np.array(fvs_zac  , dtype=precision))
    #VD.XBC    = np.append(VD.XBC  , np.array(fvs_xbc  , dtype=precision))
    #VD.YBC    = np.append(VD.YBC  , np.array(fvs_ybc  , dtype=precision))
    #VD.ZBC    = np.append(VD.ZBC  , np.array(fvs_zbc  , dtype=precision))
    #VD.XC     = np.append(VD.XC   , np.array(fvs_xc   , dtype=precision))
    #VD.YC     = np.append(VD.YC   , np.array(fvs_yc   , dtype=precision))
    #VD.ZC     = np.append(VD.ZC   , np.array(fvs_zc   , dtype=precision))
    #VD.CS     = np.append(VD.CS   , np.array(fvs_cs   , dtype=precision))
    #VD.X      = np.append(VD.X    , np.array(fvs_x    , dtype=precision))
    #VD.Y      = np.append(VD.Y    , np.array(fvs_y    , dtype=precision))
    #VD.Z      = np.append(VD.Z    , np.array(fvs_z    , dtype=precision))       
    
    return VD