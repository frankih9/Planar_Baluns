import numpy as np
import gdspy

def SQ(lib, W, tl=37):
    '''
    
    Generate a W by W square. 
    
    W : Width of the metal track.
    
    tl : Upper metal GDS layer number.
         The default of 37 is the top metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS.  
    
    '''
    
    ###############################
    # Create GDS cell of a square #
    ###############################     
    SQ = lib.new_cell('SQ')
    
    ###################################
    # Add a W wide square to GDS cell #
    ###################################
    SQ.add(gdspy.Rectangle((W/2,W/2),(-W/2,-W/2),tl))
        
        
def J(lib, W, S, tl = 37, ext = None):
    '''
    
    Generate jumper crossover for use in baluns
        
    W : Width of the metal track.
    
    S : Spacing between the metal tracks.
    
    tl : Upper metal GDS layer number.
         The default of 37 is the top metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS.  
    
    '''
     
    ##########################
    # Some initial constants #
    ##########################  
    Stanz=S*np.tan(np.pi/8)
    WdSqr2 = W/np.sqrt(2)
    WpSd2 = W + S/2
    
    #######################################################################
    # If 'ext' = None, then the natural width of the crossover is used.   #
    # When 'ext' = 'XX' for example, the width is extended to 'XX' width. #  
    #######################################################################      
    if ext == None:
        edge_x = Stanz + WpSd2 + WdSqr2
        
    else:
        CO = gdspy.CellReference(ext)
        edge_x = CO.get_bounding_box()[1][0]
    
    #################################
    # Points of the straight jumper #
    #################################
    jumper=[]
    jumper.append((-edge_x , W/2))
    jumper.append((edge_x, -W/2))     
    
    #########################
    # Create jumper polygon #
    #########################
    shape = gdspy.Rectangle(jumper[0], jumper[1], tl)
            
    #################################
    # Create GDS cell and add shape #
    ################################# 
    J = lib.new_cell('J')
    J.add(shape)
    
    
def TR(lib,L, W, S, Pri, Sec, tl=37):
    '''
    
    Generate tracks for Balun
    
    L : Overall length of the octagonal balun.
    
    W : Width of the metal track.
    
    S : Spacing between the metal tracks.
    
    Pri : Number of turns of the primary.
    
    Sec : Number of turns of the secondary.
    
    tl : Upper metal layer number.
         The default of 37 is the top metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS. 
    
    '''
    
    tracks = Pri+Sec
    
    #preliminary calculations of some constants
    tanz = np.tan(np.pi/8)
    #x = S*tanz
               
    # Forms an octagonal wedge of 2*T metal strips
    # wedge is a list of lists for use with PolygonSet()
    wedge = []
    for t in range(tracks):
        pl = []
        pl.append(((L/2-t*W-t*S)*tanz, L/2-t*W-t*S))
        pl.append(((L/2-(t+1)*W-t*S)*tanz, L/2-(t+1)*W-t*S))
        pl.append((-1*(L/2-(t+1)*W-t*S)*tanz, L/2-(t+1)*W-t*S))
        pl.append((-1*(L/2-t*W-t*S)*tanz, L/2-t*W-t*S))
        wedge.append(pl)   
    
    # # Forms a rectangular strip to clear the middle of the wedge
    # # rect_clear is a list containing the two points of the rectangle
    # rect_clear = []
    # rclx = x+0.5*S+W*np.sqrt(2)+S/np.sqrt(2)
    # rcly = 0.5*L
    # rect_clear.append((-1.0*rclx,1.0*rcly))
    # rect_clear.append((1.0*rclx,0))
    
    # Generate the tracks of the octagon with rotated wedges. 
    ## The middle of the wedges at 0,90,180,and 270 degrees are cleared for crossovers
    TR = lib.new_cell('TR')
    for ang in range(8):
        shape = gdspy.PolygonSet(wedge, tl).rotate(ang*(np.pi/4))
        # clear = gdspy.Rectangle(rect_clear[0], rect_clear[1], tl).rotate(ang*(np.pi/4))
        # if not(ang%2):
        #     TR.add(gdspy.fast_boolean(shape, clear, 'not', layer=tl))
        # else:
        #     TR.add(shape)
        TR.add(shape)


def P(lib, sep = 'XX'):
    '''
    
    Generate ports for balun. 
    
    sep : Separation distance of the primary or the secondary ports
          extracted from the GDS cell of the widest crossover used.
          Default is the 'XX' cell.
    
    This function also depends on the GDS cell 'TR' and its dimension to
    extract the distance between the primary and secondary ports. 
    
    '''
    
    ##############################
    # Create GDS cell the ports  #
    ##############################  
    PORTS = lib.new_cell('P')
    
    ##############################
    # Get width of the crossover #
    ##############################
    CO = gdspy.CellReference(lib.cells[sep])
    sep_half = CO.get_bounding_box()[1][0] 
    
    ###########################
    # Get height of the balun #
    ###########################
    Trks = gdspy.CellReference(lib.cells['TR'])
    ports_sep_half = Trks.get_bounding_box()[1][1]
    
    ###################################
    # Get width of the port extension #
    ###################################
    Port_Ex = gdspy.CellReference(lib.cells['SQ'])
    W_half = Port_Ex.get_bounding_box()[1][1]
       
    ###############################################
    # Place the extention squares to create ports #
    ###############################################
    # Add Primary Port
    Port_Ex = gdspy.CellReference(lib.cells['SQ'])
    Port_Ex.translate(sep_half - W_half, ports_sep_half + W_half)
    PORTS.add(Port_Ex)
    
    Port_Ex = gdspy.CellReference(lib.cells['SQ'])
    Port_Ex.translate(-sep_half + W_half, ports_sep_half + W_half)
    PORTS.add(Port_Ex)
    
    # Add Secondary Port  
    Port_Ex = gdspy.CellReference(lib.cells['SQ'])
    Port_Ex.translate(sep_half - W_half, -ports_sep_half - W_half)
    PORTS.add(Port_Ex)
    
    Port_Ex = gdspy.CellReference(lib.cells['SQ'])
    Port_Ex.translate(-sep_half + W_half, -ports_sep_half - W_half)
    PORTS.add(Port_Ex).flatten()

        
def VIA(lib, m, w, s, vl=36):
    '''
    
    Generates via array for top metal and bottom metal interconnections
    
     m = number of rows and columns of the via array.
     
     w = width of a square via.
     
     s = the spacing between vias in the array.
     
     vl = GDS layer number for the via.
          The default value of 37 corresponds to the via between the top
          and 2nd metal layers of the MOCMOS technology.
     
     
    '''
    
    #########################################################
    # Create GDS cell the individual via and the via array  #
    #########################################################       
    v1 = lib.new_cell('VIA_1')
    var = lib.new_cell('VIA_ARR')
    
    ##############################################
    # The two points that defines the square via #
    ##############################################
    via=[]
    via.append((0.5*w,0.5*w))
    via.append((-0.5*w,-0.5*w))
    
    #########################
    # create via square via #
    #########################
    v1.add(gdspy.Rectangle(via[0],via[1],vl))
    
    ##########################################################################
    # translate from the center of the lower leftmost via to center of array #
    ########################################################################## 
    loc=-0.5*(m-1)*(w+s)
    
    #################################
    # Generate translated via array #
    #################################
    var.add(gdspy.CellArray(v1, m, m, (w+s,w+s), (loc,loc)))
    var.flatten()
    


def X(lib, W, S, tl=37, bl=33, ext = None):
    '''
    
    Generate X crossover
        
    W : Width of the metal track.
    
    S : Spacing between the metal tracks.
    
    tl : Upper metal layer number.
         The default of 37 is the top metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS. 
    
    bl : Lower metal layer number.
         The default of 33 is the 2nd metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS. 
    
    ext : GDS cell name of the width to use.
    
    '''   
                
    ##########################
    # Some initial constants #
    ##########################   
    Stanz = S*np.tan(np.pi/8)
    WdSqr2 = W/np.sqrt(2)
    WpSd2 = W + S/2   
    
    ###########################################################################
    # If 'ext' = None, then the natural width of the crossover is used.       #
    # When 'ext' = 'XX' for example, the 'X' width is extended to 'XX' width. #  
    ###########################################################################
    if ext == None:
        edge_x = Stanz + WpSd2 + WdSqr2
        
    else:
        CO = gdspy.CellReference(ext)
        edge_x = CO.get_bounding_box()[1][0]
        
        
    ############################        
    # Points for 'X' structure #
    ############################
    A2x = WpSd2 - WdSqr2
    A2y = WpSd2
    
    B2x = edge_x
    B2y = A2y
    
    C2x = B2x
    C2y = S/2
    
    D2x = S/2 + WdSqr2
    D2y = C2y
    
    #####################################################
    # Collect points of 'X' into list of list of tuples #
    #####################################################
    
    ###############################################
    # Top of the 'X' structure                    #
    # The upper right to lower left crossover _/- #
    ###############################################
    x2top=[]
    x2top.append((A2x, A2y))
    x2top.append((B2x, B2y))
    x2top.append((C2x, C2y))
    x2top.append((D2x, D2y))
    x2top.append((-A2x, -A2y))
    x2top.append((-B2x, -B2y))
    x2top.append((-C2x, -C2y))
    x2top.append((-D2x, -D2y))
    
    ###############################################
    # Bottom of the 'X' structure                 #
    # The lower right to upper left crossover -\_ #
    ###############################################
    x2bot=[]
    x2bot.append((-A2x, A2y))
    x2bot.append((-B2x, B2y))
    x2bot.append((-C2x, C2y))
    x2bot.append((-D2x, D2y))
    x2bot.append((A2x, -A2y))
    x2bot.append((B2x, -B2y))
    x2bot.append((C2x, -C2y))
    x2bot.append((D2x, -D2y))
    
    ##################################   
    # Generate 'X' crossover polygon #
    ##################################
    X_Shapes=[]
    X_Shapes.append(gdspy.Polygon(x2top, tl))
    X_Shapes.append(gdspy.Polygon(x2bot, bl))
    
    #####################################
    # Create GDS cell for 'X' crossover #
    #####################################         
    X = lib.new_cell('X')
    
    ##########################################
    # Add the 'X' polygons into the GDS cell #
    ##########################################
    for shape in X_Shapes:
        X.add(shape)      
    
    ########################
    # Add via to crossover #
    ########################
    
    #######################################################################
    # Use cell 'VIA_ARR' generated by function 'VIA' as the via structure #
    #######################################################################
    #via locations
    via_2l=[(edge_x - W/2, -0.5*(W + S)), (-(edge_x - W/2), 0.5*(W + S))]
    for v_loc in via_2l:
        VIA = gdspy.CellReference(lib.cells['VIA_ARR'])
        VIA.translate(v_loc[0],v_loc[1])
        X.add(VIA)
    #End of adding via
    
    X.flatten()
    #End of 'X' crossover generation
    
    ##################################################
    # Generate a mirrored version of 'X' called 'XM' #
    ##################################################
    XM = lib.new_cell('XM') 
    X_ref = gdspy.CellReference(lib.cells['X'], (0,0), x_reflection=True)
    XM.add(X_ref).flatten()
    #End of 'XM' crossover generation   

        
def XX(lib, W, S, tl=37, bl=33):
    '''
    
    Generate XX crossover
        
    W : Width of the metal track.
    
    S : Spacing between the metal tracks.
    
    tl : Upper metal layer number.
         The default of 37 is the top metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS. 
    
    bl : Lower metal layer number.
         The default of 33 is the 2nd metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS. 
       
    '''   
     
    ##########################
    # Some initial constants #
    ##########################
    tanz=np.tan(np.pi/8)
    x=S*tanz
    
    #############################        
    # Points for 'XX' structure #
    #############################
    A4x=2*W+1.5*S-W*np.sqrt(2)-S/np.sqrt(2)
    A4y=2*W+1.5*S
    B4x=x+S/2+S/np.sqrt(2)+W+W*np.sqrt(2)
    B4y=A4y
    C4x=B4x
    C4y=W+1.5*S
    D4x=1.5*S+W-S/np.sqrt(2)
    D4y=C4y
    E4x=W+S/2+S/np.sqrt(2)
    E4y=W+S/2
    F4x=B4x
    F4y=E4y
    G4x=B4x
    G4y=S/2
    H4x=S/np.sqrt(2)+W*np.sqrt(2)+S/2
    H4y=G4y
    
    ######################################################
    # Collect points of 'XX' into list of list of tuples #
    ######################################################
    
    ######################################################
    # Top of the 'XX' structure                          #
    # The two upper right to lower left crossover _/-    #
    ######################################################
    xtop=[[],[]]
    xtop[0].append((A4x,A4y))
    xtop[0].append((B4x,B4y))
    xtop[0].append((C4x,C4y))
    xtop[0].append((D4x,D4y))
    xtop[0].append((-1.0*E4x,-1.0*E4y))
    xtop[0].append((-1.0*F4x,-1.0*F4y))
    xtop[0].append((-1.0*G4x,-1.0*G4y))
    xtop[0].append((-1.0*H4x,-1.0*H4y))
    
    xtop[1].append((E4x,E4y))
    xtop[1].append((F4x,F4y))
    xtop[1].append((G4x,G4y))
    xtop[1].append((H4x,H4y))
    xtop[1].append((-1.0*A4x,-1.0*A4y))
    xtop[1].append((-1.0*B4x,-1.0*B4y))
    xtop[1].append((-1.0*C4x,-1.0*C4y))
    xtop[1].append((-1.0*D4x,-1.0*D4y))
    
    #####################################################
    # Bottom of the 'XX' structure                      #
    # The two lower right to upper left crossover -\_   #
    #####################################################
    xbot=[[],[]]
    xbot[0].append((A4x,-1.0*A4y))
    xbot[0].append((B4x,-1.0*B4y))
    xbot[0].append((C4x,-1.0*C4y))
    xbot[0].append((D4x,-1.0*D4y))
    xbot[0].append((-1.0*E4x,E4y))
    xbot[0].append((-1.0*F4x,F4y))
    xbot[0].append((-1.0*G4x,G4y))
    xbot[0].append((-1.0*H4x,H4y))
    
    xbot[1].append((E4x,-1.0*E4y))
    xbot[1].append((F4x,-1.0*F4y))
    xbot[1].append((G4x,-1.0*G4y))
    xbot[1].append((H4x,-1.0*H4y))
    xbot[1].append((-1.0*A4x,A4y))
    xbot[1].append((-1.0*B4x,B4y))
    xbot[1].append((-1.0*C4x,C4y))
    xbot[1].append((-1.0*D4x,D4y))
    
    ###################################   
    # Generate 'XX' crossover polygon #
    ###################################
    XX_Shapes=[]
    XX_Shapes.append(gdspy.PolygonSet(xtop, tl))
    XX_Shapes.append(gdspy.PolygonSet(xbot, bl))
    
    ######################################
    # Create GDS cell for 'XX' crossover #
    ######################################        
    XX = lib.new_cell('XX')
    
    ###########################################
    # Add the 'XX' polygons into the GDS cell #
    ###########################################
    for shape in XX_Shapes:
        XX.add(shape)
    
    ########################
    # Add via to crossover #
    ########################
    
    #######################################################################
    # Use cell 'VIA_ARR' generated by function 'VIA' as the via structure #
    #######################################################################
    #via locations
    via_4l=[(B4x-W/2,-0.5*(S+W)),(-1*(B4x-W/2),0.5*(S+W)),(B4x-W/2,-1.5*(W+S)),(-1*(B4x-W/2),1.5*(W+S))]
    for v_loc in via_4l:
        VIA = gdspy.CellReference(lib.cells['VIA_ARR'])
        VIA.translate(v_loc[0],v_loc[1])
        XX.add(VIA)
    #End of adding via
    
    XX.flatten()    
    #End of 'XX' crossover generation
    
    ####################################################
    # Generate a mirrored version of 'XX' called 'XXM' #
    ####################################################
    XX_ref = gdspy.CellReference(lib.cells['XX'], (0,0), x_reflection=True)
    XXM = lib.new_cell('XXM')
    XXM.add(XX_ref).flatten()
    #End of 'XXM' crossover generation    

 
   
def XI(lib, W, S, tl = 37, bl = 33, ext = None):
    '''
    
    Generate XI crossover
    
    W : Width of the metal track.
    
    S : Spacing between the metal tracks.
    
    tl : Upper metal layer number.
         The default of 37 is the top metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS. 
    
    bl : Lower metal layer number.
         The default of 33 is the 2nd metal layer of the MOCMOS technology.
         This is convenient when using 'Electric' to view the resulting GDS. 
    
    ext : GDS cell name of the width to use.
    
    '''
     
    ##########################
    # Some initial constants #
    ##########################
    Stanz = S*np.tan(np.pi/8)
    Wtanz = W*np.tan(np.pi/8)
    SdSqr2 = S/np.sqrt(2)
    WdSqr2 = W/np.sqrt(2)
    SpWd2 = S + W/2
    
    ############################################################################
    # If 'ext' = None, then the natural width of the crossover is used.        #
    # When 'ext' = 'XX' for example, the 'XI' width is extended to 'XX' width. #  
    ############################################################################
    if ext == None:
        edge_x = SpWd2 + WdSqr2 + W + Stanz
        
    else:
        CO = gdspy.CellReference(lib.cells[ext])
        edge_x = CO.get_bounding_box()[1][0]
    
    #############################        
    # Points for 'XI' structure #
    #############################
    A3x = SpWd2 + WdSqr2 - Wtanz
    A3y = SpWd2 + W
    
    B3x = edge_x
    B3y = A3y
    
    C3x = B3x
    C3y = SpWd2
    
    D3x = SpWd2 + WdSqr2
    D3y = C3y
    
    E3x = SdSqr2 + W/2 + Wtanz
    E3y = W/2
    
    F3x = B3x
    F3y = W/2
    
    G3x = B3x
    G3y = -W/2
    
    H3x = SdSqr2 + W/2
    H3y = -W/2
    
    I3x = H3x - Stanz
    I3y = -SpWd2
    
    L3x = I3x - Wtanz
    L3y = -SpWd2 - W
    
    J3x = B3x
    J3y = I3y
    
    K3x = B3x
    K3y = L3y
    
    ######################################################
    # Collect points of 'XI' into list of list of tuples #
    ######################################################
    
    ######################################################
    # Top of the 'XI' structure                          #
    # The two lower right to upper left crossover -\_    #
    ######################################################
    xtop=[[],[]]
    xtop[0].append((E3x,E3y))
    xtop[0].append((F3x,F3y))
    xtop[0].append((G3x,G3y))
    xtop[0].append((H3x,H3y))
    xtop[0].append((-1.0*I3x,-1.0*I3y))
    xtop[0].append((-1.0*J3x,-1.0*J3y))
    xtop[0].append((-1.0*K3x,-1.0*K3y))
    xtop[0].append((-1.0*L3x,-1.0*L3y))
    
    xtop[1].append((I3x,I3y))
    xtop[1].append((J3x,J3y))
    xtop[1].append((K3x,K3y))
    xtop[1].append((L3x,L3y))
    xtop[1].append((-1.0*E3x,-1.0*E3y))
    xtop[1].append((-1.0*F3x,-1.0*F3y))
    xtop[1].append((-1.0*G3x,-1.0*G3y))
    xtop[1].append((-1.0*H3x,-1.0*H3y))
    
    #############################################
    # Bottom of the 'XI' structure              #
    # Upper right to lower left crossover _/-   #
    #############################################
    xbot=[]
    xbot.append((A3x,A3y))
    xbot.append((B3x,B3y))
    xbot.append((C3x,C3y))
    xbot.append((D3x,D3y))
    xbot.append((-1.0*A3x,-1.0*A3y))
    xbot.append((-1.0*B3x,-1.0*B3y))
    xbot.append((-1.0*C3x,-1.0*C3y))
    xbot.append((-1.0*D3x,-1.0*D3y))
    
    ###################################   
    # Generate 'XI' crossover polygon #
    ###################################
    XI_Shapes=[]
    XI_Shapes.append(gdspy.PolygonSet(xtop, tl))
    XI_Shapes.append(gdspy.Polygon(xbot, bl))
    
    ######################################
    # Create GDS cell for 'XI' crossover #
    ######################################       
    XI = lib.new_cell('XI')
    
    ###########################################
    # Add the 'XI' polygons into the GDS cell #
    ###########################################
    for shape in XI_Shapes:
        XI.add(shape)
    
    ########################
    # Add via to crossover #
    ########################
    
    #######################################################################
    # Use cell 'VIA_ARR' generated by function 'VIA' as the via structure #
    #######################################################################
    #via locations
    via_3l=[(edge_x - W/2, (S + W)), (-(edge_x - W/2), -(S + W))]
    for v_loc in via_3l:
        VIA = gdspy.CellReference(lib.cells['VIA_ARR'])
        VIA.translate(v_loc[0],v_loc[1])
        XI.add(VIA)
    #End of adding via
    
    XI.flatten()    
    #End of 'XI' crossover generation
    
    ####################################################
    # Generate a mirrored version of 'XI' called 'XIM' #
    ####################################################
    XI_ref = gdspy.CellReference(lib.cells['XI'])
    XIM = lib.new_cell('XIM')
    XIM.add(XI_ref).flatten()
    #End of 'XIM' crossover generation    
   