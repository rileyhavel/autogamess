from .dictionaries import templates

#Class for input parameters
class Input:
    'GAMESS(US) input parameters'

    class Control:
        'Control class of GAMESS(US) input'

        def __init__(self, params):
            self.scftyp = params.split('SCFTYP=')[1].split()[0]
            self.mult   = params.split('MULT='  )[1].split()[0]
            self.nprint = params.split('NPRINT=')[1].split()[0]
            self.coord  = params.split('COORD=' )[1].split()[0]
            self.runtyp = params.split('RUNTYP=')[1].split()[0]
            self.icut   = params.split('ICUT='  )[1].split()[0]
            self.itol   = params.split('ITOL='  )[1].split()[0]
            self.maxit  = params.split('MAXIT=' )[1].split()[0]
            self.qmttol = params.split('QMTTOL=')[1].split()[0]
            self.icharg = params.split('ICHARG=')[1].split()[0]
            self.ispher = params.split('ISPHER=')[1].split()[0]

    class System:
        'System class of GAMESS(US) input'

        def __init__(self, params):
            self.mwords = params.split('MWORDS=')[1].split()[0]
            self.memddi = params.split('MEMDDI=')[1].split()[0]

    class Statpt:
        'Statpt class of GAMESS(US) input'

        def __init__(self, params):
            self.opttol = params.split('OPTTOL=')[1].split()[0]
            self.nstep  = params.split('NSTEP=' )[1].split()[0]

    class SCF:
        'SCF class of GAMESS(US) input'

        def __init__(self, params):
            self.dirscf = params.split('DIRSCF=')[1].split()[0]
            self.fdiff  = params.split('FDIFF=' )[1].split()[0]
            self.conv   = params.split('CONV='  )[1].split()[0]

    class DFT:
        'DFT class of GAMESS(US) input'
        pass

    class Basis:
        'Basis class of GAMESS(US) input'
        pass

    def __init__(self, template):

        if '.txt' in template:
            read_txt(template)
        else:
            self.defaults(template)

    def read_txt(self, txtfile):

        for line in read_file(txtfile):
            line.split()

    def defaults(self, template):
        params       = templates[template]
        self.Control = self.Control(params['Control'])
        self.System  = self.System( params['System'] )
        self.Statpt  = self.Statpt( params['Statpt'] )
        self.SCF     = self.SCF(    params['SCF']    )
        self.DFT     = self.DFT()
        self.Basis   = self.Basis()

    def write_inp(self, file_name, version):
        f = open(file_name, 'w')
        f.write('!'+ version +'\n')
        f.write('!  by Brian C. Ferrari \n')
        f.write('!\n')
        f.writelines(self.Control.make_list)
        f.writelines(self.System.make_list)