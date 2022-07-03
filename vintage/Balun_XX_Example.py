'''
This script is to call the appropriate functions to generate baluns with the 
'XX' structure.  Also, this script assumes that the cells generated by the 
individual functions remain in memory so 'Balun_XX_Build' function can reference
to them and use them to construct the balun.  Apparently this is how 'gdspy' works.
For baluns that are not reducible to a 1:1, the turns on the primary and the 
secondary must be even. 
'''
import gdspy
import Balun_Scripts.Balun_Parts as BP
import Balun_Scripts.Valid_Check as VC
from Balun_Scripts.Balun_XX_Build import Balun_XX_Build

#########################
# Variables. Change me. #
#########################

# GDS cell name for the balun
Cell_Name = 'Balun_XX'

# via row and columns
viaM = 4
# Square via width
viaW = 1
# via spacing 
viaS = 1

# Length of the balun
balunLength = 300
# Width of each track
trackWidth = 9
# Spacing between tracks
trackSpacing = 3

# Turns in the primary
primaryTurns = 3
# Turns in the secondary
secondaryTurns = 3

##########################################
# Generate GDS cells of some balun parts #
##########################################
# Order is important as certain functions depend on previously generated GDS cells.

# Generate GDS cell for a square
BP.SQ(trackWidth)

# Generate GDS cell for the via array
BP.VIA(int(viaM), viaW, viaS)

# Generate the 'XX' crossover
BP.XX(trackWidth, trackSpacing)

# Generate the 'X' crossover
BP.X(trackWidth, trackSpacing)

#############################################################
# With the given balun parameters, will the balun be valid? #
#############################################################

# Total number of tracks is primary turns plus secondary turns
max_tracks = VC.max_tracks(balunLength, trackWidth, trackSpacing, 'XX')

# Total tracks should be even for 'XX' baluns
if max_tracks%2:
    max_tracks = max_tracks - 1
    
# If not 1:1, the turns on either the side must be even and not equal to zero   
ratio_valid = VC.Ratio_XX(int(primaryTurns), int(secondaryTurns))

if max_tracks >= (int(primaryTurns) + int(secondaryTurns)) and ratio_valid:
    
    ###############################################
    # Generate GDS cells of remaining balun parts #
    ###############################################
    # Generate the all the tracks
    BP.TR(balunLength, trackWidth, trackSpacing, int(primaryTurns), int(secondaryTurns))

    # Generate ports
    BP.P()
    
    #################################
    # Construct the 'XX' type balun #
    #################################
    Balun_XX_Build(balunLength, trackWidth, trackSpacing, int(primaryTurns), int(secondaryTurns), C_Name = Cell_Name)
    
    #####################################################
    # Only write the balun cell into the GDS file in um #
    #####################################################
    cell_list = []
    cell_list.append(Cell_Name)
    gdspy.write_gds(Cell_Name + '.gds', cells = cell_list, unit = 1.0e-6, precision = 1.0e-9)
    
    ################################################
    # Display all the GDS cells in current library #
    ################################################
    gdspy.LayoutViewer()
    

else:
    ##############################
    # Display issues with inputs #
    ##############################
    if max_tracks < (int(primaryTurns) + int(secondaryTurns)):
        print('Maximum number of tracks is: '+str(max_tracks))
        
    if ratio_valid == False:
        print('Turn ratio not valid!')