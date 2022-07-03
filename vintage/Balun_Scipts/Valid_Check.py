import numpy as np
import gdspy

def max_tracks(L, W, S, limit = 'XX'):
    '''
    
    Determine the maximum number of tracks based on length given by 'limit'
    
    L : Overall length of the octagonal balun.
    
    W : Width of the metal track.
    
    S : Spacing between the metal tracks.
    
    limit : If None, the inner most track is 0 length.
            Usually a crossover is passed in and its length determines
            the minimum length of the inner most track. 
    
    '''
    
    if limit == None:
        length = 0
        
    else:
        CO = gdspy.CellReference(limit)
        length = 2*CO.get_bounding_box()[1][0]
    
    #preliminary calculations of some constants
    tanz = np.tan(np.pi/8)
    ld2tanz = length/(2*tanz)
    WpS = W +S
    
    tracks = -(ld2tanz + W - L/2)/WpS + 1
    
    return int(tracks)

                              
def Ratio_X(Pri, Sec):
    '''
    
    Determine whether the turn ratio for 'Balun_X' is valid
    
    Pri : Number of turns of the primary.
    
    Sec : Number of turns of the secondary.
    
      
    '''
    valid = True
    
    if Pri == 0 or Sec == 0:
        valid = False
        
    return valid            


def Ratio_XX(Pri, Sec):
    '''
    
    Determine whether the turn ratio for 'Balun_XX' is valid
    
    Pri : Number of turns of the primary.
    
    Sec : Number of turns of the secondary.
    
      
    '''
    valid = True
    
    if Pri == 0 or Sec == 0:
        valid = False
        
    elif Pri != Sec:
        if Pri%2 or Sec%2:
            valid = False
    
    return valid    


def Ratio_XI(Pri, Sec):
    '''
    
    Determine whether the turn ratio for 'Balun_XI' is valid
    
    Pri : Number of turns of the primary.
    
    Sec : Number of turns of the secondary.
    
      
    '''
    valid = True
    
    if Pri == 0 or Sec == 0:
        valid = False
        
    elif Sec%2:   
        valid = False
    
    return valid        
   