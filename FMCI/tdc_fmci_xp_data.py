import StringIO
import re
import os

import numpy as np
    
from Auxiliary        import tdc_Mesh, tdc_Setup_Props
from Particles        import tdc_XP_Data
from Common_Data_Plot import tdc_Data, tdc_Data__with_Timetable


class tdc_FMCI_XP_Data_Base(tdc_Data):
    """
    Basic class for use for input in Full Monte Carlo Simulations
    Contains all fucntionality to save and restore data from ascii file
    --------
    Members:
    --------
    name     
    calc_id  
    i_ts     
    time     
    x        
    p        
    fmci_XP      
    """
    __particle_short_names = { 'Electrons' : 'E',
                               'Positrons' : 'P',
                               'Protons'   : 'I',
                               'Pairs'     : 'G' }

    default_ascii_filename_format = 'xp_%04d.dat'

    def __init__(self):
        """
        Contains class members in one place
        """
        self.ascii_filename = None

        # name and calc_id
        self.name    = None
        self.calc_id = None
        self.i_ts    = None
        self.time    = None
        # data members
        self.x       = None
        self.p       = None
        self.fmci_XP = None

    @staticmethod
    def init_from_ascii(filename, **kwargs):
        """
        return tdc_FMCI_XP_Data_Base instance initialized from ascii
        data file 'filename'
        """
        fmci_xp_data=tdc_FMCI_XP_Data_Base()
        fmci_xp_data.read_from_ascii(filename)
        return fmci_xp_data

    def save_to_ascii(self, filename, print_progress=True):
        """
        Save class data to ascii file 'filename''
        ---------------
        File Structure::
        ---------------
        
        #>>params_data:
        nx=
        np=

        #>>x:
        x

        #>>p:
        p

        #>>XP: (rows:%4d, columns:%4d)
        fmci_XP

        #>>params_physics:
        particle=
        time=

        #>>params_TDC:
        calc_id=
        i_ts=

        -------------
        """
        out=StringIO.StringIO()
        # --------------------------------
        # create string with data
        # --------------------------------
        # params_data:
        out.write('#>>params_data:\n')
        out.write('nx=%d\n' % self.x.size)        
        out.write('np=%d\n' % self.p.size)
        # x:
        out.write('\n#>>x:\n')
        np.savetxt(out, self.x, fmt='%1.8E')
        # p:
        out.write('\n#>>p:\n')
        np.savetxt(out, self.p, fmt='%1.8E')
        # fmci_XP:
        out.write('\n#>>XP: (rows:%4d, columns:%4d)\n' % (self.x.size,self.p.size))
        np.savetxt(out, self.fmci_XP, fmt='%1.8E')
        # params_physics:
        out.write('\n#>>params_physics:\n')
        out.write('particle=%s\n' % self.__particle_short_names[self.name])        
        out.write('time=%1.8E\n'  % self.time)
        # params_TDC:
        out.write('\n#>>params_TDC:\n')
        out.write('calc_id=%s\n' % self.calc_id)        
        out.write('i_ts=%d\n' % self.i_ts)
        # --------------------------------
        # save to file 
        # --------------------------------
        f=open(filename,'w')
        f.write(out.getvalue())
        f.close()
        out.close()
        if print_progress:
            print '\nContent saved in "%s" \n' % filename

    def read_from_ascii(self, filename):
        """
        read class data from ascii file 'filename'
        """
        self.ascii_filename = filename
        # read file content into a string
        f=open(filename,'r')
        file_str=f.read()
        f.close()
        # make dictionary with file content
        reg_exp_data_groups=re.compile(r'^#>>(\w+):.*\n',re.M)
        file_dict=self.make_data_dict_from_str(reg_exp_data_groups,file_str)
        # read arrays ------------------------------
        self.x=np.loadtxt(StringIO.StringIO(file_dict['x']))
        self.p=np.loadtxt(StringIO.StringIO(file_dict['p']))
        self.fmci_XP=np.loadtxt(StringIO.StringIO(file_dict['XP']))
        # regular expression for extracting parameter=value
        reg_exp_param_val=re.compile(r'\n*(\w+)=',re.M)
        # read params_physics -----------------------
        params_physics_dict=self.make_data_dict_from_str(reg_exp_param_val,file_dict['params_physics'])
        self.name=self.__get_particle_name(params_physics_dict['particle'])
        self.time=float(params_physics_dict['time'])
        # read params_TDC ---------------------------
        params_TDC_dict=self.make_data_dict_from_str(reg_exp_param_val,file_dict['params_TDC'])
        self.calc_id=params_TDC_dict['calc_id']
        self.i_ts=int(params_TDC_dict['i_ts'])

    def make_data_dict_from_str(self,reg_exp,data_str):
        """
        - split string using reg_exp
        - delete first entry (before reg_exp, usually empty if no header)
        - make dictionary out of the splitted list
        - delete trailing \n in values
        """
        data_list=reg_exp.split(data_str)
        data_list.pop(0)
        data_dict=dict(zip(data_list[0::2],data_list[1::2]))
        # get rid of \n at the end of the strings
        reg_exp_strip_n=re.compile(r'\n$')
        for key in data_dict.keys():
            data_dict[key]=reg_exp_strip_n.sub('',data_dict[key])
        return data_dict

    def __repr__(self):
        s  = 'tdc_FMCI_XP_Data_Base:\n'
        s += ' particle name : %s\n' % self.name
        s += '       calc_id : %s\n' % self.calc_id
        s += '          i_ts : %g\n' % self.i_ts
        # partition 
        s += ' nx: %4d;  x: [%g, %g]\n'       % (len(self.x),self.x[0],self.x[-1])
        s += ' np: %4d;  p: [%1.2e, %1.2e]\n' % (len(self.p),self.p[0],self.p[-1])
        return s

    def read(self, 
             i_ts, 
             print_progress=True, 
             filename_format=None):
        """
        read *ascii file* from the same directory as the current file
        """
        if self.ascii_filename is None:
            raise Exception("tdc_FMCI_XP_Data_Base: this class was not set up from an ascii file!")
        if filename_format is None:
            filename_format = self.default_ascii_filename_format 
        dirname = os.path.dirname(self.ascii_filename)
        filename = os.path.join(dirname, filename_format % i_ts)
        self.read_from_ascii(filename)
            
    def get_time(self):
        return self.time

    def __get_particle_name(self,short_name):
        """
        """
        for (key,val) in self.__particle_short_names.items():
            if val==short_name:
                return key
        raise Exception('%s: could not get particle name for %s!' % (str(self),short_name) )
        
    def set_xp_partition(self,xp_partition):
        print 'Can not change xp_partition for tdc_FMCI_XP_Data_Base!\n'
        
    def fill_fmci_XP_array(self,**kwargs):
        print 'Can not re-calculate fmci_XP array in tdc_FMCI_XP_Data_Base!\n'
        


class tdc_FMCI_XP_Data(tdc_Data__with_Timetable,tdc_FMCI_XP_Data_Base):
    """
    Class
    """
        
    def __init__(self, calc_id, particle_name, xp_partition):
        """
        - opens particle HDF5 file, 
        - setups partition (x)
        - creates array for holding data and sets it to zeros
        NB: Reads setup_properties.h5
        ---------
        Parameters:
        ---------
        calc_id
        particle_name
        xp_partition

        -> can change XP grid 
        """
        tdc_FMCI_XP_Data_Base.__init__(self)
        # name and calc_id
        self.name    = particle_name
        self.calc_id = calc_id
        # setup XP_Data --------------------
        sample_dict = dict(name='regular', n_reduce=1, n_min=1)
        self.xp = tdc_XP_Data(calc_id, particle_name, sample_dict, get_weight=True)
        # interface to timetable -----------
        self.timetable = self.xp.timetable
        # setup properties -----------------
        setup_props = tdc_Setup_Props(calc_id)
        # normalization parameters
        self.W0 = setup_props.get_papam('FMPProps/W0')
        self.L  = setup_props.get_papam('/GridProps/L')
        # set xp_partition =================
        self.set_xp_partition(xp_partition)

    def get_pure_data_copy(self):
        """
        Returns copy containing only data necessary for producing a sinle plot,
        without HDF file specific info
        Used for saving data for subsequent restoring of plot without
        accesing original data files
        """
        import copy
        data=copy.copy(self)
        data.xp = data.xp.get_pure_data_copy()
        data.timetable = data.timetable.get_pure_data_copy() 
        return data

    def __repr__(self):
        s  = 'tdc_FMCI_XP_Data:\n'
        s += ' particle name : %s\n' % self.name
        s += '       calc_id : %s\n' % self.calc_id
        s += '          i_ts : %g\n' % self.i_ts
        # partition 
        s += 'Partition => %s\n' % str(self.xp_partition)
        return s

    def set_xp_partition(self,xp_partition):
        """
        set new data partition and created clear fmci_XP array
        """
        # setup partition: set x grid
        self.xp_partition = xp_partition
        self.xp_partition.setup_x_grid(xx=[0,self.L])
        # local copies of x and p grids
        self.x=self.xp_partition.x
        self.p=self.xp_partition.p
        # allocate fmci_XP array
        self.fmci_XP=np.zeros((self.xp_partition.nx,self.xp_partition.np))
        
    def read(self, i_ts, print_progress=True):
        """
        Read particle data for timeshot i_ts and fill fmci_XP array for
        current partition
        """
        if print_progress:
            print 'Reading data "%s" i_ts=%d ... ' % (self.xp.name,i_ts)
        self.xp.read(i_ts)
        self.fill_fmci_XP_array(print_progress)
        self.i_ts = i_ts
        self.time = self.xp.timetable.get_time()

    def fill_fmci_XP_array(self, print_progress=True):
        """
        Fill fmci_XP array for current timeshot and current partition:
        - iterates over all particles in self.xp and adds their statistical weights
          into corresponding cell of fmci_XP array
        - normalizes weights to GJ numger density
        """
        # iterate over particles ----------------------
        x_idx=self.xp_partition.x_idx
        p_idx=self.xp_partition.p_idx
        if print_progress:
            print 'Filling fmci_XP array for "%s" ... ' % self.xp.name
        for  x,p,w  in zip(self.xp.x,self.xp.p,self.xp.w):
            ix=x_idx(x)
            ip=p_idx(p)
            # add weight only if indexies are not None
            if (ix is not None) and (ip is not None):
                    self.fmci_XP[ix,ip] += w
        # ---------------------------------------------
        # normalize to n_GJ
        # works for non-uniform x partition as well
        dx = self.xp_partition.x_cell[1:]-self.xp_partition.x_cell[0:-1]
        self.fmci_XP = self.W0*self.fmci_XP/dx.reshape((dx.size,1))
