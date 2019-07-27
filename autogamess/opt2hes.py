from .config import *

def opt2hes(optfile, logfile):
    """
    This function changes the coordinates in input files that have not
    yet been run, to reduce optimization runtimes.

    Parameters
    ----------
    optfile: string
        This should be a string that points to the input file of an
        already run optimization file. (FULL DIRECTORY STRING REQUIRED)
    logfile: string
        This should be a string that points to the log file of an
        already run optimization file. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    This function returns nothing.

    Example
    -------
    >>> import opt2hes as oh
    >>>
    >>> #Note the './' directory is the one the BATCH script is in
    >>> logfile = './Optimization_Log_Folder/IBv6_NH3_CCSD-T_CC6_opt.log'
    >>> optfile = './IBv6_NH3_CCSD-T_CC6_opt.inp'
    >>>
    >>> oh.opt2hes(inpfile, logfile)
    >>>
    """
    #Define force line
    force     = ' $FORCE METHOD=FULLNUM NVIB=2 PROJCT=.TRUE. $END\n'
    if ('_B3LYP_' in optfile) or ('_MP2_' in optfile):
        force = ' $FORCE METHOD=SEMINUM NVIB=2 PROJCT=.TRUE. $END\n'
    if ('_CC5_' in optfile) or ('_CC6_' in optfile) or ('_PCseg-4_' in optfile):
        force = ' $FORCE METHOD=FULLNUM NVIB=2 PROJCT=.TRUE. $END\n'

    #Define Runtyps
    ropt = '=OPTIMIZE'
    rhes = '=HESSIAN'

    #Define file identifiers
    opt = '_opt'
    hes = '_hes'

    #Define Numerical Gradients commands
    numgrd0 = 'NUMGRD=.TRUE.'
    numgrd1 = 'NUMGRD=.T.'

    #Open, read in, and close log file
    f   = open(logfile, 'r')
    log = f.readlines()
    f.close()

    #Grabs optimized geometries tail index
    tfind = 'COORDINATES OF ALL ATOMS ARE'
    dtail = len(log) - ctr_f(tfind, log[::-1]) - 1

    #Grabs optimized geometries header index
    hfind = '***** EQUILIBRIUM GEOMETRY LOCATED *****'
    dhead = ctr_f(hfind, log) + 4

    #Checks to make sure head and tail exist
    if check_if_exists(logfile, ctr_f(hfind, log)):
        raise ValueError()

    #Assemble list of optimized geometry coordinates and get size
    coords = log[dhead : dtail]

    #Open, read in, and close input file
    f   = open(optfile, 'r')
    inp = f.readlines()
    f.close()

    #Replace OPTIMIZATION with HESSIAN
    i      = ctr_f(ropt, inp)
    inp[i] = inp[i].replace(ropt, rhes)

    #Remove Numerical Gradients from input file
    i = ctr_f(numgrd0, inp)
    if i is not -1:
        inp[i] = inp[i].replace(numgrd0, '')
    i = ctr_f(numgrd1, inp)
    if i is not -1:
        inp[i] = inp[i].replace(numgrd1, '')

    #Insert force line into hessian input
    if ctr_f(force, inp) is -1:
        inp.insert(ctr_f('$SCF', inp), force)

    #Replace coordinates in file
    i    = ctr_f('$DATA', inp)
    data = inp[i:]
    for coord in coords:
        temp   = [x.replace(' ', '') for x in data]
        index  = ctr_f(coord.split('.0')[0].replace(' ',''), temp)
        j      = ctr_f(data[index], inp)
        inp[j] = coord
        del data[index]

    #Open, write, and close input file
    hesfile = optfile.replace(opt, hes)
    f       = open(hesfile, 'w')
    f.writelines(inp)
    f.close()

    return
