import sys                        # Provides Information About Python Interpreter Constants,
                                  # Functions, & Methods
from io import StringIO           # Implements A File-Like Class That Reads And Writes A String
                                  # Buffer (i.e., A Memory File)
from IPython import get_ipython   # Simple Function To Call To Get The Current Interactive Shell
                                  # Instance

#-------------------------------------------------------------------------------------------------#
#  CLASS NAME:  ipynb_Exit()                                                                      #
#  PURPOSE:     This class contains attributes and methods that can be used to establish and      #
#               terminate a connection to a Db2 server or database.                               #
#-------------------------------------------------------------------------------------------------#
class ipynb_Exit(SystemExit):
    """Exit Exception for IPython. Exception temporarily redirects stderr to buffer."""

    #---------------------------------------------------------------------------------------------#
    #  FUNCTION NAME:  __init()__                                                                 #
    #  PURPOSE:        This method initializes an instance of the ipynb_Exit class.               #
    #---------------------------------------------------------------------------------------------#
    def __init__(self):
        sys.stderr = StringIO()        # Redirect sys.stderr to a StringIO (memory buffer) object.

    #---------------------------------------------------------------------------------------------#
    #  FUNCTION NAME:  __init()__                                                                 #
    #  PURPOSE:        This method cleans up when an instance of the ipynb_Exit class is          #
    #                  deleted.                                                                   #
    #---------------------------------------------------------------------------------------------#
    def __del__(self):
        sys.stderr = sys.__stderr__    # Restore sys.stderr to the original values it had at
                                       # the start of the program.

#-------------------------------------------------------------------------------------------------#
#  FUNCTION:  customExit()                                                                        #
#  PURPOSE:     This function contains attributes and methods that can be used to establish and   #
#               terminate a connection to a Db2 server or database.                               #
#-------------------------------------------------------------------------------------------------#
def customExit(returnCode=0):
    if returnCode is 0:
        ipynb_Exit()
    else:
        raise ipynb_Exit

#-------------------------------------------------------------------------------------------------#
# If An Application Running With IPython (i.e., A Jupyter Notebook) Calls The Exit Function,      #
# Call A Custom Exit Routine So The Jupyter Notebook Will Not Stop Running; Otherwise, Call The   #
# Default Exit Routine                                                                            #
#-------------------------------------------------------------------------------------------------#
if get_ipython():    
    exit = customExit                  # Rebind To The Custom Exit Function
else:
    exit = exit                    