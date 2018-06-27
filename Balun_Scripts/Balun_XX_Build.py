import gdspy

def Balun_XX_Build(L, W, S, Pri, Sec, tl=37, C_Name='BALUN_XX'):
    '''
    
    Planar balun with XX crossovers
    Center tap point of the secondary is extended with a square
    
    L : Overall length of the octagonal balun.
    
    W : Width of the metal track.
    
    S : Spacing between the metal tracks.
    
    Pri : Number of turns of the primary.
    
    Sec : Number of turns of the secondary.
    
    tl : Upper metal GDS layer number.
         The default of 37 is the top metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS. 
    
    C_Name : Cell name for the balun.
    
    
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
    # xxl is starting point for leftmost XX crossover
    # xxs is the step size for the XX crossover
    # xxn is the number of XX crossover on each half about y-axis
    xxl = -L/2 + (2*W+1.5*S)    
    xxs = 4*(W+S)    
    #xxn = int(np.floor(2*T/4))
    xxn = int(2*T/4)
    for step in range(xxn):    
        XX = gdspy.CellReference('XX', rotation = 90)          
        XX.translate(xxl+step*xxs, 0)       
        poly_cell.add(XX)
        
        clear = gdspy.Rectangle(XX.get_bounding_box()[0] + [-S/2, W], XX.get_bounding_box()[1] + [S/2, -W], tl)
        CLR.add(clear)
                    
        XXM = gdspy.CellReference('XXM', rotation = 90)          
        XXM.translate(-xxl-step*xxs, 0)        
        poly_cell.add(XXM)  
        
        clear = gdspy.Rectangle(XXM.get_bounding_box()[0] + [-S/2, W], XXM.get_bounding_box()[1] + [S/2, -W], tl)
        CLR.add(clear)  
                        
    # xl is starting point for leftmost X crossover
    # xs is the step size for the X crossover
    # xn is the number of X crossover on each half of the y-axis
    xl = -L/2 + (xxn*4*(W+S)) + (W+0.5*S)
    xs = 2*W+2*S 
    xn = int((Pri+Sec-4*(xxn))/2)
    
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
    #
    # End of left to right placement of crossovers
            
    ################################################
    # Start of up and down placement of crossovers #
    ################################################
    # xxl is starting point for bottom most XX crossover
    # xxs is the step size for the XX crossover
    # xxv is the number of XX crossover on each half about x-axis
    xxl = xxl + 2*(W+S)
    #xxv = int(np.floor((2*T-2)/4))
    xxv = int((2*T-2)/4)
    
    for step in range(xxv):
        XX = gdspy.CellReference('XX')          
        XX.translate(0, xxl+step*xxs)       
        poly_cell.add(XX)
        
        clear = gdspy.Rectangle(XX.get_bounding_box()[0] + [W, -S/2], XX.get_bounding_box()[1] + [-W, S/2], tl)
        CLR.add(clear)
                                                              
        XXM = gdspy.CellReference('XXM')          
        XXM.translate(0, -xxl-step*xxs)        
        poly_cell.add(XXM) 
        
        clear = gdspy.Rectangle(XXM.get_bounding_box()[0] + [W, -S/2], XXM.get_bounding_box()[1] + [-W, S/2], tl)
        CLR.add(clear)   
    
    # If 2*T-2 tracks is not divisible by 4(number of tracks for XX), then 
    # there should be two tracks remaining for either the Pri or the Sec 
    # for one X structure below the x-axis.
    # xv tests whether this is the case.
    xv = 4*xxv < 2*T-2    
    if xv:
        X = gdspy.CellReference('X')          
        X.translate(0, -L/2 + (xxv*4*(W+S)) + 2*(W+S) + W+0.5*S)       
        poly_cell.add(X)   
        
        clear = gdspy.Rectangle(X.get_bounding_box()[0] + [W, -S/2], X.get_bounding_box()[1] + [-W, S/2], tl)
        CLR.add(clear)
        # If Pri == Sec, then add the remining X structure above the x-axis.
        # When Pri != Sec, these two tracks are used to expand to remaining tracks
        # with the XX structure.  This is an arbitrary choice and the logic of which
        # is the Pri and which is the Sec will be worked out later. 
        if Pri == Sec:
            XM = gdspy.CellReference('XM')          
            XM.translate(0, L/2 - (xxv*4*(W+S)) - 2*(W+S) - (W+0.5*S))        
            poly_cell.add(XM) 
            
            clear = gdspy.Rectangle(XM.get_bounding_box()[0] + [W, -S/2], XM.get_bounding_box()[1] + [-W, S/2], tl)
            CLR.add(clear)
    # If Pri == Sec, then the crossover placements along the y-axis has ended.
    #
    # When Pri is not equal to Sec, then the process of fitting XX and X structures
    # along the y-axis is repeated for the remaining tracks.
    if Pri != Sec:
        # Start of crossover placement below the x-axis
        # xxl is starting point for remaining XX crossovers below x-axis
        # xxs is the step size for the XX crossover
        # xxv is the number of XX crossovers below x-axis
        xxv = int(abs(Sec-Pri)/4)
        xxl = -L/2 + (W+S)*2*T + 2*W+1.5*S
        
        for step in range(xxv):
            XX = gdspy.CellReference('XX')          
            XX.translate(0, xxl+step*xxs)       
            poly_cell.add(XX)
            
            clear = gdspy.Rectangle(XX.get_bounding_box()[0] + [W, -S/2], XX.get_bounding_box()[1] + [-W, S/2], tl)
            CLR.add(clear)
        # If the remaining tracks are not divisible by 4,
        # then there are two tracks remaining for an X structure
        if (Pri+Sec > 4*xxv+2*T):
            X = gdspy.CellReference('X')          
            X.translate(0, -L/2 + (W+S)*2*T + 4*(W+S)*xxv + W+0.5*S)       
            poly_cell.add(X)
            
            clear = gdspy.Rectangle(X.get_bounding_box()[0] + [W, -S/2], X.get_bounding_box()[1] + [-W, S/2], tl)
            CLR.add(clear)    
        #
        # End placement of crossovers below x-axis
                
        #################################################
        # Start of crossover placement above the x-axis #
        #################################################
        # xxl is starting point for remaining XX crossovers above x-axis (2 less turns then previous)
        # xxs is the step size for the XX crossover
        # xxv is the number of XX crossovers above x-axis (2 more turns then previous)
        xxv = int((abs(Sec-Pri)+2)/4) 
        xxl = L/2 - (W+S)*(2*T-2) - (2*W+1.5*S)  
        for step in range(xxv):
            XXM = gdspy.CellReference('XXM')          
            XXM.translate(0, xxl-step*xxs)       
            poly_cell.add(XXM)   
        
            clear = gdspy.Rectangle(XXM.get_bounding_box()[0] + [W, -S/2], XXM.get_bounding_box()[1] + [-W, S/2], tl)
            CLR.add(clear)
        # If the remaining tracks are not divisible by 4,
        # then there are two tracks remaining for an X structure
        if (Pri+Sec > 4*xxv+2*T-2):
            XM = gdspy.CellReference('XM')          
            XM.translate(0, L/2 - (W+S)*(2*T-2) - 4*(W+S)*xxv - (W+0.5*S))       
            poly_cell.add(XM)
            
            clear = gdspy.Rectangle(XM.get_bounding_box()[0] + [W, -S/2], XM.get_bounding_box()[1] + [-W, S/2], tl)
            CLR.add(clear)
    #
    # End of up/down placement of crossovers
        
    # ###############     
    # # Add jumpers #
    # ###############          
    # J = gdspy.CellReference('J') 
    # J.translate(0, L/2 - (1.5*W+S))
    # poly_cell.add(J)
    # 
    # J = gdspy.CellReference('J') 
    # J.translate(0, -L/2 + (1.5*W+S))
    # poly_cell.add(J)
    # # End
    
    
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
    
    #####################################################################
    # Logic for rotating balun so the secondary is always on the bottom #
    #####################################################################
    rot = 0
    # If T/2 is even
    if int(1- (T/2)%2):
        if Sec > Pri:
            rot = True
    
    # If T/2 is odd
    else:
        if Sec < Pri:
            rot = True           
    
    balun_ref = gdspy.CellReference('temp', (0,0), rotation=rot*180)
    balun_cell = gdspy.Cell(C_Name, exclude_from_current=False) 
    balun_cell.add(balun_ref)
                    
    ###############################                    
    # Add center tap to secondary #
    ###############################
    # The secondary center tap will always be at this location for this balun topology
    x_loc = 0
    y_loc = -L/2 + (W/2+S)
    ctap = gdspy.CellReference('SQ')
    ctap.translate(x_loc, y_loc)
    balun_cell.add(ctap).flatten()
       
    