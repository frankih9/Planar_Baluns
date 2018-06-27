import numpy as np
import gdspy

def Balun_X_Build(L, W, S, Pri, Sec, tl=37, C_Name='BALUN_X'):
    '''
    Planar balun with X crossovers
    Center tap point of the secondary is indicated with a via structure
    
    L : Overall length of the octagonal balun
    W : Width of the metal track
    S : Spacing between the metal tracks
    Pri : Number of turns of the primary
    Sec : Number of turns of the secondary
    tl : Upper metal layer number
    C_Name : Cell name for the balun
    
    '''
    
    #########################################################
    # Create temporary GDS cell as rotation might be needed #
    ###################################### ##################
    poly_cell = gdspy.Cell('temp',exclude_from_current=False)
    
    #############################################################
    # Create GDS cell of the crossover clearances of the tracks #
    ###################################### ######################
    CLR = gdspy.Cell('CLR', exclude_from_current=False)
    
    ########################################
    # Determine number of shared turns (T) #
    ########################################
    T = min([Pri, Sec]) 
    
    ##################################################        
    # Start of left to right placement of crossovers #
    ##################################################
    # xl is starting point for leftmost X crossover
    # xs is the step size for the X crossover
    # xn is the number of X crossover on each half about y-axis
    xl = -L/2 + W + S/2    
    xs = 2*(W + S)    
    xn = int((Pri + Sec) / 2)
    
    for step in range(xn):    
        X = gdspy.CellReference('X', rotation = 90)          
        X.translate(xl+step*xs, 0)       
        poly_cell.add(X)
        
        clear = gdspy.Rectangle(X.get_bounding_box()[0] + [-S/2, W], X.get_bounding_box()[1] + [S/2, -W], tl)
        CLR.add(clear)
                    
        XM = gdspy.CellReference('XM', rotation = 90)          
        XM.translate(-xl-step*xs, 0)        
        poly_cell.add(XM) 
        
        clear = gdspy.Rectangle(XM.get_bounding_box()[0] + [-S/2, W], XM.get_bounding_box()[1] + [S/2, -W], tl)
        CLR.add(clear)   
                        
    # # jl is starting point for jumper
    # if (Pri + Sec) % 2:
    #     jl = -L/2 + (xn*xs) + W/2        
    #           
    #     J = gdspy.CellReference('J', rotation = 90)          
    #     J.translate(jl, 0)       
    #     poly_cell.add(J)
    #                 
    #     J = gdspy.CellReference('J', rotation = 90)          
    #     J.translate(-jl, 0)        
    #     poly_cell.add(J)   
        
    #End of left to right placement of crossovers
            
    ################################################        
    # Start of up and down placement of crossovers #
    ################################################
    # xl is starting point for bottom most X crossover
    # xs is the step size for the X crossover
    # xv is the number of X crossover on each half about x-axis
    xl = xl + (W+S)
    xv = T - 1
    
    for step in range(xv):
        X = gdspy.CellReference('X')          
        X.translate(0, xl+step*xs)       
        poly_cell.add(X)
        
        clear = gdspy.Rectangle(X.get_bounding_box()[0] + [W, -S/2], X.get_bounding_box()[1] + [-W, S/2], tl)
        CLR.add(clear)
                                                                
        XM = gdspy.CellReference('XM')          
        XM.translate(0, -xl-step*xs)        
        poly_cell.add(XM)
            
        clear = gdspy.Rectangle(XM.get_bounding_box()[0] + [W, -S/2], XM.get_bounding_box()[1] + [-W, S/2], tl)
        CLR.add(clear)
    #Place jumper below the x-axis first
    jl = -L/2 +(W+S) + (xv*xs) + W/2
    # J = gdspy.CellReference('J')          
    # J.translate(0, jl)       
    # poly_cell.add(J)
    
    # if Pri == Sec:
    #     #Place jumper above the x-axis
    #     J = gdspy.CellReference('J')          
    #     J.translate(0, -jl)       
    #     poly_cell.add(J) 
    # # If Pri == Sec, then the crossover placements along the y-axis has ended.
    #
    # When Pri is not equal to Sec, then the process of fitting 'X' and '-' structures
    # along the y-axis is repeated for the remaining tracks.
    if Pri != Sec:
        # Start of crossover placement below the x-axis
        #
        # xl is starting point for remaining X crossovers below x-axis
        # xs is the step size for the X crossover
        # xv is the number of X crossovers below x-axis
        xv = int(abs(Sec-Pri)/2)
        xl = jl + 1.5*(W+S)
        
        for step in range(xv):
            X = gdspy.CellReference('X')          
            X.translate(0, xl + step*xs)       
            poly_cell.add(X)
            
            clear = gdspy.Rectangle(X.get_bounding_box()[0] + [W, -S/2], X.get_bounding_box()[1] + [-W, S/2], tl)
            CLR.add(clear)
        
        # # If the remaining tracks are not divisible by 2,
        # # then there is one track remaining for an '-' structure
        # if abs(Sec-Pri)%2:
        #     J = gdspy.CellReference('J')         
        #     J.translate(0, jl + (xv*xs) + (W+S))       
        #     poly_cell.add(J)    
        #
        # End placement of crossovers below x-axis
                
        # Start of crossover placement above the x-axis
        # xl is starting point for remaining X crossovers above x-axis (1 less turns then previous)
        # xs is the step size for the X crossover
        # xv is the number of X crossovers above x-axis (2 more turns then previous)
        xv = int((abs(Sec-Pri) + 1)/2)
        xl = -jl - 0.5*(W+S) 
        for step in range(xv):
            XM = gdspy.CellReference('XM')          
            XM.translate(0, xl - step*xs)       
            poly_cell.add(XM) 
            
            clear = gdspy.Rectangle(XM.get_bounding_box()[0] + [W, -S/2], XM.get_bounding_box()[1] + [-W, S/2], tl)
            CLR.add(clear)  
        
        # # If the remaining tracks are not divisible by 2,
        # # then there is one track remaining for an '-' structure
        # if (abs(Sec-Pri) + 1)%2:
        #     J = gdspy.CellReference('J')           
        #     J.translate(0, -jl - (xv*xs) )       
        #     poly_cell.add(J)
    #
    # End of up/down placement of crossovers
        
    ##############################        
    # Add in/out port extensions #
    ##############################
    P = gdspy.CellReference('P')
    poly_cell.add(P)
    
    
    ########################
    # Add and clear tracks #
    ########################
    # Clear the outer tracks at ports
    p1 = P.get_bounding_box()[0][0] + W 
    p2 = P.get_bounding_box()[1][0] - W
    CLR.add(gdspy.Rectangle((p1, -L/2), (p2, -L/2 + W + S/2), tl))
    CLR.add(gdspy.Rectangle((p1, L/2), (p2, L/2 - W - S/2), tl))
    #
    TR = gdspy.CellReference('TR')
    CLR = gdspy.CellReference('CLR')
    # Boolean for clearance
    poly_cell.add(gdspy.fast_boolean(TR, CLR, 'not', layer=tl))
                    
    #########################################
    # Place ctap via structure to secondary #
    #########################################
    if Sec <= Pri:
        VIA = gdspy.CellReference('VIA_ARR')
        VIA.translate(0,-L/2 + W/2 + (2*Sec-1)*(W+S))
        poly_cell.add(VIA)
    else:
        VIA = gdspy.CellReference('VIA_ARR')
        if (Sec-Pri)%2:
            VIA.translate(0, -L/2 + W/2 + (Pri+Sec-1)*(W+S))
            #VIA.translate(0, L/2 - W/2 - (Pri+Sec-1)*(W+S))
            poly_cell.add(VIA)
        else:
            VIA.translate(0, L/2 - W/2 - (Pri+Sec-1)*(W+S))
            #VIA.translate(0, -L/2 + W/2 + (Pri+Sec-1)*(W+S))
            poly_cell.add(VIA)
    
    #####################################################################
    # Logic for rotating balun so the secondary is always on the bottom #
    #####################################################################
    rot = 0
    
    # If T/2 is even
    if T%2:
        if Pri >= Sec:
            rot = True
    
    # If T/2 is odd
    else:
        if Sec > Pri:
            rot = True           
    balun_ref = gdspy.CellReference('temp', (0,0), rotation=rot*180)
    balun_cell = gdspy.Cell(C_Name, exclude_from_current=False) 
    balun_cell.add(balun_ref).flatten()
       
        
       
    