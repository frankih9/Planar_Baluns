import gdspy

def Balun_XI_Build(L, W, S, Pri, Sec, tl=37, C_Name = 'BALUN_XI'):
    '''
    
    Planar balun with XI crossovers
    Center tap point of the secondary is extended with a square
    
    L : Overall length of the octagonal balun.
    
    W : Width of the metal track.
    
    S : Spacing between the metal tracks.
    
    Pri : Number of turns of the primary.
          An integer that is >= 1.  
    Sec : Number of turns of the secondary.
          An even integer >= 2.
          
    tl : Upper metal GDS layer number.
         The default of 37 is the top metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS. 
    
    C_Name : Cell name for the balun.
    
    
    '''
    ######################################
    # Create GDS cell of the final balun #
    ###################################### 
    balun_cell = gdspy.Cell(C_Name, exclude_from_current=False)
    
    #############################################################
    # Create GDS cell of the crossover clearances of the tracks #
    ###################################### ######################
    CLR = gdspy.Cell('CLR', exclude_from_current=False)
    
    ####################################################################
    # Logic for determining turn expansion on the Primary or Secondary #
    ####################################################################
    # ex_p => bool, expansion on the priamry?
    # ex_s => bool, expansion on the secondary?
    ex_p = False
    ex_s = False
    
    # Determine if 1:2 ratio of Primary to Secondary turns is chosen
    if Sec/2 != Pri:
        if Sec/2 < Pri:
            ex_p = True
        else:
            ex_s = True
              
    ############################################################################        
    # Start of left to right placement of crossovers and their track clearance #
    ############################################################################
    # xil is starting point for leftmost 'XI' crossover
    # xis is the step size for the 'XI' crossover
    # xin is the number of 'XI' crossover on each half about y-axis
    xil = -L/2 + (1.5*W+S)    
    xis = 3*(W+S)    
    
    # Find xin
    if Sec/2 == Pri:
        xin = int((Pri + Sec)/3)
    else:
        if Sec/2 < Pri:
            xin = int(Sec/2)
        else:
            xin = Pri
            
    # Place 'XI' and 'XIM' in alternating order
    for step in range(xin):    
        # Left half
        XI = gdspy.CellReference('XI', rotation = 90, x_reflection = step%2)          
        XI.translate(xil+step*xis, 0)       
        balun_cell.add(XI)
        
        clear = gdspy.Rectangle(XI.get_bounding_box()[0] + [-S/2, W], XI.get_bounding_box()[1] + [S/2, -W], tl)
        CLR.add(clear)
                    
        # Right half
        XIM = gdspy.CellReference('XIM', rotation = 90, x_reflection = step%2)          
        XIM.translate(-xil-step*xis, 0)        
        balun_cell.add(XIM)
        
        clear = gdspy.Rectangle(XIM.get_bounding_box()[0] + [-S/2, W], XIM.get_bounding_box()[1] + [S/2, -W], tl)
        CLR.add(clear)
        
    # xl is starting point for leftmost 'X' crossover
    # xs is the step size for the 'X' crossover
    # xn is the number of 'X' crossover on each half about y-axis
    xl = -L/2 + xin*xis + (W+0.5*S)
    xs = 2*(W + S)
    xn = int((Pri + Sec - 3*xin)/2)
    
    # If there is turn expansion(no longer a 1:2 balun), place 'X' and 'XM'
    for step in range(xn):
        # Left half
        X = gdspy.CellReference('X', rotation = 90, x_reflection = step%2)          
        X.translate(xl + step*xs, 0)       
        balun_cell.add(X)
        
        clear = gdspy.Rectangle(X.get_bounding_box()[0] + [-S/2, W], X.get_bounding_box()[1] + [S/2, -W], tl)
        CLR.add(clear)
        
        # Right half
        XM = gdspy.CellReference('XM', rotation = 90, x_reflection = step%2)          
        XM.translate(-xl - step*xs, 0)       
        balun_cell.add(XM)
        
        clear = gdspy.Rectangle(XM.get_bounding_box()[0] + [-S/2, W], XM.get_bounding_box()[1] + [S/2, -W], tl)
        CLR.add(clear)
    
    # # If the turns expanded are not even, place '-'                                        
    # if (Pri + Sec - 3*xin)%2:
    #     # jl is starting point for leftmost '-' crossover
    #     jl = -L/2 + (Pri + Sec)*(W+S) - W/2 -S
    #     
    #     # Left half
    #     J = gdspy.CellReference('J', rotation = 90) 
    #     J.translate(jl, 0)
    #     balun_cell.add(J)
    #     
    #     # Right half
    #     J = gdspy.CellReference('J', rotation = 90) 
    #     J.translate(-jl, 0)
    #     balun_cell.add(J)
        
    # End of routine for left to right placement of crossovers
            
    #####################################################################
    # Generate a list of crossovers above the x-axis from the outermost #
    # for the case that the balun is 1:2                                #
    #####################################################################
    CO_UPPER=['XM']
    for index in range(xin):
        if index==0:
            continue
        if (index % 2):
            CO_UPPER.pop()
            CO_UPPER.append('XXM')
            CO_UPPER.append('J')
        else:
            CO_UPPER.pop()
            CO_UPPER.append('XM')
            CO_UPPER.append('XM')
            
    #####################################################################        
    # Generate a list of crossovers below the x-axis from the outermost #
    # for the case that the balun is 1:2                                #
    #####################################################################
    CO_LOWER=['J']
    for index in range(xin):
        if index==0:
            continue
        if (index % 2):
            CO_LOWER.pop()
            CO_LOWER.append('X')
            CO_LOWER.append('X')
        else:
            CO_LOWER.pop()
            CO_LOWER.append('XX')
            CO_LOWER.append('J')
             
    #####################################################################        
    # Modify the lists for the crossovers for either above or below the #
    # the x-axis to account for turn expansion in the primary           #
    #####################################################################
    if ex_p == True:
        if xin%2:
            CO_LOWER.pop()
            
            ex_tl = Pri + Sec - (3*xin - 1)
            xn = int(ex_tl/2)
            for step in range(xn):
                CO_LOWER.append('X')
            if ex_tl%2:
                CO_LOWER.append('J')
            
            ex_tu = Pri + Sec - (3*xin)
            xn = int(ex_tu/2)
            for step in range(xn):
                CO_UPPER.append('XM')
            if ex_tu%2:
                CO_UPPER.append('J')    
        else:
            CO_UPPER.pop()
            
            ex_tu = Pri + Sec - (3*xin - 1)
            xn = int(ex_tu/2)
            for step in range(xn):
                CO_UPPER.append('XM')
            if ex_tu%2:
                CO_UPPER.append('J')
            
            ex_tl = Pri + Sec - (3*xin)
            xn = int(ex_tl/2)
            for step in range(xn):
                 CO_LOWER.append('X')
            if ex_tl%2:
                 CO_LOWER.append('J')
    
    #####################################################################        
    # Modify the lists for the crossovers for either above or below the #
    # the x-axis to account for turn expansion in the secondary         #
    #####################################################################                          
    if ex_s == True:
        if xin%2:
            CO_UPPER.pop()
            #ex_tu => extension of turns for upper crossovers
            ex_tu = Pri + Sec - (3*xin - 2)
            xn = int(ex_tu/4)
            for step in range(xn):
                CO_UPPER.append('XXM')
            if ex_tu%4 > 0:
                CO_UPPER.append('XM')
            #ex_tl => extension of turns for lower crossovers
            ex_tl = Pri + Sec - (3*xin)
            xn = int(ex_tl/4)
            for step in range(xn):
                CO_LOWER.append('XX')
            if ex_tl%4 > 0:
                CO_LOWER.append('X')
        else:
            CO_LOWER.pop()
            
            ex_tl = Pri + Sec - (3*xin - 2)
            xn = int(ex_tl/4)
            for step in range(xn):
                CO_LOWER.append('XX')
            if ex_tl%4 > 0:
                CO_LOWER.append('X')
            
            ex_tu = Pri + Sec - (3*xin)
            xn = int(ex_tu/4)
            for step in range(xn):
                 CO_UPPER.append('XXM')
            if ex_tu%4 > 0:
                 CO_UPPER.append('XM')
                 
    ##############################################################################        
    # Start of upper to lower placement of crossovers and their track clearances #
    ##############################################################################    
    # x_loc and y_loc is the uppermost starting point    
    x_loc = 0        
    y_loc = L/2 - W - S
    
    # Place the crossovers above the x-axis
    # for cell in CO_UPPER:
    #     CO_cell = gdspy.CellReference(cell)
    #     y_shift = CO_cell.get_bounding_box()[1][1]
    #     y_loc = y_loc - y_shift
    #     CO_cell.translate(x_loc, y_loc)
    #     balun_cell.add(CO_cell)
    #     clear = gdspy.Rectangle(CO_cell.get_bounding_box()[0] + [W, -S/2], CO_cell.get_bounding_box()[1] + [-W, S/2], tl)
    #     CLR.add(clear)
    #     y_loc = y_loc - y_shift - S 
    
    for cell in CO_UPPER:
        if cell != 'J':
            CO_cell = gdspy.CellReference(cell)
            y_shift = CO_cell.get_bounding_box()[1][1]
            y_loc = y_loc - y_shift
            CO_cell.translate(x_loc, y_loc)
            balun_cell.add(CO_cell)
            clear = gdspy.Rectangle(CO_cell.get_bounding_box()[0] + [W, -S/2], CO_cell.get_bounding_box()[1] + [-W, S/2], tl)
            CLR.add(clear)
        else:
            y_shift = W
        y_loc = y_loc - y_shift - S          
       
    # x_loc and y_loc is the lowermost starting point
    x_loc = 0        
    y_loc = -L/2 + 2*(W + S)
    
    #Place the crossovers below the x-axis
    # for cell in CO_LOWER:
    #     CO_cell = gdspy.CellReference(cell)
    #     y_shift = CO_cell.get_bounding_box()[1][1]
    #     y_loc = y_loc + y_shift
    #     CO_cell.translate(x_loc, y_loc)
    #     balun_cell.add(CO_cell)
    #     clear = gdspy.Rectangle(CO_cell.get_bounding_box()[0] + [W, -S/2], CO_cell.get_bounding_box()[1] + [-W, S/2], tl)
    #     CLR.add(clear)
    #     y_loc = y_loc + y_shift + S 
    
    for cell in CO_LOWER:
        if cell != 'J':
            CO_cell = gdspy.CellReference(cell)
            y_shift = CO_cell.get_bounding_box()[1][1]
            y_loc = y_loc + y_shift
            CO_cell.translate(x_loc, y_loc)
            balun_cell.add(CO_cell)
            clear = gdspy.Rectangle(CO_cell.get_bounding_box()[0] + [W, -S/2], CO_cell.get_bounding_box()[1] + [-W, S/2], tl)
            CLR.add(clear)
        else:
            y_shift = W
        y_loc = y_loc + y_shift + S     
    # End of routine for upper to lower placement of crossovers
    
    ##############################      
    # Add in/out port extensions #
    ##############################
    P = gdspy.CellReference('P')
    balun_cell.add(P)    
                
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
    balun_cell.add(gdspy.fast_boolean(TR, CLR, 'not', layer=tl))
    
    # ##############      
    # # Add jumper #
    # ############## 
    # # A jumper will always be at this location for this balun topology          
    # x_loc = 0
    # y_loc = -L/2 + (1.5*W+S)
    # J = gdspy.CellReference('J') 
    # J.translate(x_loc, y_loc)
    # balun_cell.add(J)
    
     
    ###############################                    
    # Add center tap to secondary #
    ###############################
    # The secondary center tap will always be at this location for this balun topology
    x_loc = 0
    y_loc = -L/2 + (W/2+S)
    ctap = gdspy.CellReference('SQ')
    ctap.translate(x_loc, y_loc)
    balun_cell.add(ctap)
    
    ##############################
    # Flatten the balun GDS cell #
    ##############################
    balun_cell.flatten()
       
    