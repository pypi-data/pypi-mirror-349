import time
from xes_neo.__init__  import __version__

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def timecall():
    return time.time()

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError # evil ValueError that doesn't tell you what the wrong value was

def str_to_list(s):
    arr = [float(i) for i in list(s.split(","))]
    return arr

def norm(val):
    return np.linalg.norm(val)


def banner():
    """
    https://patorjk.com/software/taag/#p=display&h=2&v=0&f=Univers&t=XES%20NEO
    """
    banner_str = ('''
                                XES Neo ver %s
__________________________________________________________________________________
                                                                                   
                                                                                   
ooooooo  ooooo oooooooooooo  .oooooo..o     ooooo      ooo oooooooooooo   .oooooo.   
 `8888    d8'  `888'     `8 d8P'    `Y8     `888b.     `8' `888'     `8  d8P'  `Y8b  
   Y888..8P     888         Y88bo.           8 `88b.    8   888         888      888 
    `8888'      888oooo8     `"Y8888o.       8   `88b.  8   888oooo8    888      888 
   .8PY888.     888    "         `"Y88b      8     `88b.8   888    "    888      888 
  d8'  `888b    888       o oo     .d8P      8       `888   888       o `88b    d88' 
o888o  o88888o o888ooooood8 8""88888P'      o8o        `8  o888ooooood8  `Y8bood8P' 
                                                                                
__________________________________________________________________________________

    '''% __version__)

    return banner_str
