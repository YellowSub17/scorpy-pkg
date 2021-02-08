import matplotlib.pyplot as plt
import imageio
import h5py

from PIL import Image 
import CifFile as pycif
import matplotlib.patches as patches
import numpy as np
import scipy.signal as signal
import configparser as cfp
import symmetry as sym
from numba import jit
from scipy import special





class ExpGeom:

    def __init__(self, filename):
        '''
        Handler for .geom parameter files
        filename: str of the path to the .geom file
        '''

        self.filename = filename

        #dictionary of arguments from the .geom file
        #args is for general arguments, panel is for listed panels

        self.file_args, self.panel_args = self.parse_file()

        # a few arguments we might need from parsed_args
        self.res = float(self.file_args['res'])   #pixel resolution (~5000 Pix/m, 200 e-6 m/Pix)
        self.clen = float(self.file_args['clen']) #camera length
        self.photon_energy = float(self.file_args['photon_energy']) #eV
        self.wavelength = (4.135667e-15*2.99792e8)/self.photon_energy  #m

        self.panels = self.make_panels(self.panel_args)  #make the panels




    def translate_pixels(self, pix_sss, pix_fss):

        pix_posx = np.zeros((len(pix_sss)))
        pix_posy = np.zeros((len(pix_sss)))
        pix_posz = np.zeros((len(pix_sss)))

        pix_pos = np.zeros( (len(pix_sss), 3))

        panel_mods = np.floor(pix_sss/64)

        for i_p, panel in enumerate(self.panels):
            if np.floor(panel['min_ss']/64) not in panel_mods:
                continue
            else:
                loc = np.where(int(panel['min_ss']/64) == panel_mods)


                pix_posx[loc] = panel['fs_xy'][0]*(pix_fss[loc]%128) \
                                 + panel['ss_xy'][0]*(pix_sss[loc]%64)

                pix_posy[loc] = panel['fs_xy'][1]*(pix_fss[loc]%128) \
                                + panel['ss_xy'][1]*(pix_sss[loc]%64)

                pix_posz[loc] = panel['coffset']

                #translate according to corner of panel
                pix_posx[loc] += panel['corner_xy'][0]
                pix_posy[loc] += panel['corner_xy'][1]



        return np.array([pix_posx/self.res, pix_posy/self.res, pix_posz+self.clen]).T









    def parse_file(self):
        f = open(self.filename, 'r')
        cont = f.read()
        cont = '[params]' + cont
        config = cfp.ConfigParser(interpolation=None, inline_comment_prefixes = (';'))
        config.read_string(cont)

        parsed_args= {}
        parsed_panel ={}

        for line in config['params']:
            if '/' in line:  #check if thise argument is a panel eg. p0a4/fs
                                #if it is a panel, split by name/attribute, add to panel_dict
                panel_split = line.split('/')
                if panel_split[0] not in parsed_panel.keys(): #if the panel is no already in the dictionary
                    parsed_panel[panel_split[0]] = {} #add panel
                    parsed_panel[panel_split[0]]['name'] = panel_split[0] #set the name key

                #after adding the panel, add the panel attribute
                parsed_panel[panel_split[0]][panel_split[1]] = config['params'][line]

            else: #if the argument is not a panel argument, add to the arg dictionary instead
                parsed_args[line] = config['params'][line]


        return parsed_args, parsed_panel




    def plot_panels(self, sf=1):
        '''
        for every panel in the geom, plot the panel
        '''
        for panel in self.panels:
            #size of the panel
            #check if we implemented the fs_xy and ss_xy correctly
            #I think all they are doing atm is multiplying +-1 for
            #to flip the rectangle
            rect_width = sf*panel['fs_xy'][1]*(panel['max_fs']-panel['min_fs'])/self.res
            rect_height = sf*panel['ss_xy'][0]*(panel['max_ss']-panel['min_ss'])/self.res

            #rotation of the panel, trig from fs directions
            #should be close to 90 or 270 degrees
            rect_rot =(panel['fs_xy'][0]**2 +panel['fs_xy'][1]**2)**(1/2)/(panel['fs_xy'][0])
            rect_rot = np.degrees(np.arccos(np.clip(1/rect_rot, -1, 1)))

            #corner of the panel
            rect_x = sf*panel['corner_xy'][0]/self.res
            rect_y = sf*panel['corner_xy'][1]/self.res

            #rectangle object
            rect = patches.Rectangle((rect_x, rect_y), rect_width, -rect_height,rect_rot,
                                        fill=False,ec='red', alpha=1,lw=1 )

            #add the rectangle object to the plot
            plt.gca().add_patch(rect)

            #plot an X in the (0,0) corner, add a label here as well
            plt.plot( sf*panel['corner_xy'][0]/self.res, sf*panel['corner_xy'][1]/self.res, 'rx')
            plt.text( sf*panel['corner_xy'][0]/self.res, sf*panel['corner_xy'][1]/self.res, panel['name'], fontsize=6)



    def make_panels(self, file_panels):

        '''
        return a list of panel objects, for every panel in this experiment ExpGeom
        '''
        panels = []    #init a list of panels
        names = []
        min_fss = []
        min_sss = []
        max_sss = []
        max_fss = []
        coffsets = []

        for key in file_panels.keys(): # for every panel in the parsed panels
            this_panel = {}
            this_panel['name'] = key
            this_panel['min_fs'] = int(file_panels[key]['min_fs'])
            this_panel['min_ss'] = int(file_panels[key]['min_ss'])
            this_panel['max_ss'] = int(file_panels[key]['max_ss'])
            this_panel['max_fs'] = int(file_panels[key]['max_fs'])
            this_panel['coffset'] = float(file_panels[key]['coffset'])

            fs_xy = file_panels[key]['fs'].split()
            this_panel['fs_xy'] = [float(fs_xy[0][:-1]),
                                   float(fs_xy[1][:-1])]

            ss_xy = file_panels[key]['ss'].split()
            this_panel['ss_xy'] = [float(ss_xy[0][:-1]),
                                   float(ss_xy[1][:-1])]

            this_panel['corner_xy'] = [float(file_panels[key]['corner_x']),
                                       float(file_panels[key]['corner_y'])]
            panels.append(this_panel)
        return panels


class CifData:

    def __init__(self,fname, qmax=-1):

        self.fname = fname
        print(f'Reading CIF: {self.fname}')
        cif = pycif.ReadCif(self.fname)
        print('Done')

        vk = cif.visible_keys[0]
        self.cif = dict(cif[vk])

        if '_diffrn_radiation_wavelength.wavelength' in cif.keys():
            self.wavelength = float(self.cif['_diffrn_radiation_wavelength.wavelength'])
        else:
            print('WARNING: No wavelength found in cif')
            self.wavelength = None
        self.space_group = self.cif['_symmetry.space_group_name_h-m']

        self.dcell_angles = self.get_dcell_angles()

        self.dcell_vectors = self.get_dcell_vectors()

        self.qcell_vectors = self.get_qcell_vectors()

        self.miller_refl, self.scattering, self.spherical = self.get_refl()


        if qmax < 0:
            self.qmax = np.max(self.spherical[:,0])
        else:
            self.qmax = qmax
            self.spherical = self.spherical[np.where(self.spherical[:,0] <qmax)]
            self.scattering = self.scattering[np.where(self.spherical[:,0] <qmax)]
            self.miller_refl = self.miller_refl[np.where(self.spherical[:,0] <qmax)]






    def get_refl(self):

        h = np.array(self.cif['_refln.index_h']).astype(np.int32)
        k = np.array(self.cif['_refln.index_k']).astype(np.int32)
        l = np.array(self.cif['_refln.index_l']).astype(np.int32)


        if '_refln.intensity_meas' in self.cif.keys():
            I = np.array(self.cif['_refln.intensity_meas'])
            I = np.where(I == '?', '0', I)
            I = I.astype(np.float64)
        elif '_refln.f_meas_au' in self.cif.keys():
            I = np.array(self.cif['_refln.f_meas_au'])
            I = np.where(I == '?', '0', I)
            I = I.astype(np.float64)**2

        elif '_refln.f_squared_meas' in self.cif.keys():
            I = np.array(self.cif['_refln.f_squared_meas'])
            I = np.where(I == '?', '0', I)
            I = I.astype(np.float64)

        else:
            print('WARNING: No Intensity found when reading cif.')
            return None

        asym_refl = np.array([h, k, l, I]).T
        miller_refl = sym.apply_sym(asym_refl, self.space_group)

        scattering_pos = np.matmul(miller_refl[:,:-1], np.array(self.qcell_vectors))

        scattering = np.zeros(miller_refl.shape)
        scattering[:, :-1] = scattering_pos
        scattering[:, -1] = miller_refl[:, -1]


        q_mag = np.linalg.norm(scattering[:,:3], axis=1)
        phi = np.arctan2(scattering[:,1], scattering[:,0]) # -pi -> pi
        phi[np.where(phi<0)] = phi[np.where(phi<0)] + 2*np.pi  #0 -> 2pi
        theta = np.arctan2(np.linalg.norm(scattering[:,:2], axis=1),scattering[:,2]) #0 -> pi

        spherical  =np.array([q_mag, theta, phi, miller_refl[:,-1]]).T


        return miller_refl, scattering, spherical


    def get_qcell_vectors(self):
        ast = np.cross(self.dcell_vectors[1],self.dcell_vectors[2]) /np.dot(self.dcell_vectors[0],np.cross(self.dcell_vectors[1],self.dcell_vectors[2]))
        bst = np.cross(self.dcell_vectors[0],self.dcell_vectors[2]) /np.dot(self.dcell_vectors[0],np.cross(self.dcell_vectors[1],self.dcell_vectors[2]))
        cst = np.cross(self.dcell_vectors[0],self.dcell_vectors[1]) /np.dot(self.dcell_vectors[0],np.cross(self.dcell_vectors[1],self.dcell_vectors[2]))

        return [ast, bst, cst]

    def get_dcell_vectors(self):
        a_unit = np.array([1.0,0.0,0.0])
        b_unit = np.array([np.cos(self.dcell_angles[2]), np.sin(self.dcell_angles[2]), 0])
        c_unit = np.array([
                            np.cos(self.dcell_angles[1]),
                           (np.cos(self.dcell_angles[0]) - np.cos(self.dcell_angles[1])*np.cos(self.dcell_angles[2]))/np.sin(self.dcell_angles[2]),
                            np.sqrt( 1 - np.cos(self.dcell_angles[1])**2 - (( np.cos(self.dcell_angles[0]) -np.cos(self.dcell_angles[1])*np.cos(self.dcell_angles[2]))/np.sin(self.dcell_angles[2]))**2)
                        ])

        a = float(self.cif['_cell.length_a'])*a_unit
        b = float(self.cif['_cell.length_b'])*b_unit
        c = float(self.cif['_cell.length_c'])*c_unit

        return [a, b, c]

    def get_dcell_angles(self):

        alpha = np.radians(float(self.cif['_cell.angle_alpha']))
        beta = np.radians(float(self.cif['_cell.angle_beta']))
        gamma = np.radians(float(self.cif['_cell.angle_gamma']))
        return [alpha,beta, gamma]




class MaskData:

    def __init__(self, fname, geo, mask_value=0):
        self.fname = fname
        self.mask_value=mask_value
        self.geo = geo
        self.h5 = h5py.File(self.fname, 'r')
        self.data = np.array(h5py.File(self.fname, 'r')['data']['data'])
        self.qlist = self.gen_qlist()


    def gen_qlist(self):
        loc = np.where(self.data==self.mask_value)

        fss_df = loc[1]
        sss_df = loc[0]
        inten_df = np.ones(len(fss_df))

        pix_pos = self.geo.translate_pixels(sss_df, fss_df) #x,y,z position [m]

        # r_mag = np.sqrt( pix_pos[:,0]**2 + pix_pos[:,1]**2)
        r_mag = np.hypot( pix_pos[:,0], pix_pos[:,1])

        polar_t = np.degrees(np.arctan2(pix_pos[:,1], pix_pos[:,0]))
        polar_t[np.where(polar_t <0)] = polar_t[np.where(polar_t <0)] +360

        diffrat_t = np.degrees(np.arctan2(r_mag, pix_pos[:,2]))
        q_mag = (2*np.pi/self.geo.wavelength) * np.sin(np.radians(diffrat_t))/1e10 #1/A
        qlist = np.array([pix_pos[:,0], pix_pos[:,1], pix_pos[:,2], r_mag, diffrat_t, q_mag, polar_t, inten_df])

        return qlist.T

    def plot_peaks(self, cmap='viridis'):

        if type(cmap) != type('x'):
            plt.plot(self.qlist[:,0], self.qlist[:,1], '.')
        else:
            plt.scatter(self.qlist[:,0], self.qlist[:,1], s=20, c=self.qlist[:, -1],  cmap=cmap)
            plt.colorbar()








class PeakData:

    def __init__(self, df, geo, qlist_flag=True, rpf_flag=False):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        qlist_flag: flag to generate qvector correlation list
                    dont waste time generateing calculating a list if we need
                    to split the frames and calc again anyway
        '''

        self.geo = geo  #ExpGeom object
        self.rpf_flag = rpf_flag

        #if df is str, read dataframe from file, else, assume df is dataframe
        if type(df)==str:

            #use cols: frameNUmebr, photon energy (ev), wavelngth, GMD,
            #peak index, peak_x_raw, peak_y_raw, peak_r_assembled,_peak_q,
            #peak_resA, npix, total intens, max intens, sigmaBG, SNR

            # self.df = np.genfromtxt(df, delimiter=', ', skip_header=1, usecols=(0,2,3,4,5,6,7,8,9,10,11,12,13,14,15))

            if self.rpf_flag:
                self.df = np.genfromtxt(df, delimiter=' ')
            else:
                self.df = np.genfromtxt(df, delimiter=', ', skip_header=1, usecols=(0,6,7,12))
        else:
            self.df = df

        #multiple frames can be in a single peak file, so list the unique frames
        self.frameNumbers = np.unique(self.df[:,0])
        self.qlist_flag=qlist_flag
        if self.qlist_flag:
            self.qlist = self.gen_qlist()
            self.qmax = np.max(self.qlist[:,5])

    def split_frames(self):
        '''
        return a list of PeakData objects, where each PeakData object on has a
        single frame of data
        '''
        if len(self.frameNumbers)<=1:       #check if we can actually split this data frame
            print('This PeakData object contains one frame, cannot split frames')
            return None                 #should this just return itself?
        else:
            frames = []                                 #init list of frames
            for fn in self.frameNumbers:                    #for each frame number
                frame_df = self.df[np.where(self.df[:,0]==fn)]  #get the peaks from this frame number
                frames.append(PeakData(frame_df, self.geo))     #make the Peak data object and append
            return frames                           #return the list of appended peak datas



    def gen_qlist(self):
        '''
        generate a list of important values to calculate from
        it's easier to work with arrays the panda dataframes
        '''

        # fss_df = self.df[:,5]    #0-127, fs direction
        # sss_df = self.df[:,6]    #ss direction
        # inten_df = self.df[:,11] #intensity

        fss_df = self.df[:,1]    #0-127, fs direction
        sss_df = self.df[:,2]    #ss direction
        inten_df = self.df[:,3] #intensity

        pix_pos = self.geo.translate_pixels(sss_df, fss_df) #x,y,z position [m]

        # r_mag = np.sqrt( pix_pos[:,0]**2 + pix_pos[:,1]**2)
        r_mag = np.hypot(pix_pos[:,0], pix_pos[:,1])

        polar_t = np.degrees(np.arctan2(pix_pos[:,1], pix_pos[:,0]))
        polar_t[np.where(polar_t <0)] = polar_t[np.where(polar_t <0)] +360

        diffrat_t = np.degrees(np.arctan2(r_mag, pix_pos[:,2]))
        q_mag = (2*np.pi/self.geo.wavelength) * np.sin(np.radians(diffrat_t))/1e10 #1/A
        qlist = np.array([pix_pos[:,0], pix_pos[:,1], pix_pos[:,2], r_mag, diffrat_t, q_mag, polar_t, inten_df])

        return qlist.T





    def plot_peaks(self, cmap='viridis'):

        if type(cmap) != type('x'):
            plt.plot(self.qlist[:,0], self.qlist[:,1], '.')
        else:
            plt.scatter(self.qlist[:,0], self.qlist[:,1], s=20, c=self.qlist[:, -1],  cmap=cmap)
            plt.colorbar()




    def powder(self, nq = 500):
        '''
        supply magnitudes and intensitys to a specified resolution (nq bands)
        give Q and 2theta values for choice in plotting
        '''
        Q_band_lims = np.linspace(0, self.qmax, nq+1)
        I = np.zeros((nq))
        N = np.zeros((nq))
        for i, q in enumerate(Q_band_lims[:-1]):
            q_range_min = q
            q_range_max = Q_band_lims[i+1]

            q_range = self.qlist[np.where((self.qlist[:,3]>=q_range_min) & (self.qlist[:,3]<q_range_max))[0] ]

            I[i] = np.sum(q_range[:,5])
            N[i] = len(q_range[:,5])


        Q = np.linspace(0, self.qmax, nq)
        theta2 = np.degrees(np.arctan2(Q, self.geo.clen))

        return Q, theta2, I,N






class CorrelationVol:

    def __init__(self, nq=256, ntheta=360, qmax=1, fromfile=False, fname='test', hflag=False):
       '''
        representation of a correlation volume, 3D space with two q and q' axis
        and one theta axis
        nq: number of bins in the q space axes
        ntheta: number of bins in the theta axis
        qmax: maximum qvalue to which to correlate to

        note: this class could potentially double as an rspace correlation vol
        all varibles are to reference qspace for the moment, might generalise later
       '''
       if fromfile:
           self.fname=fname
           config = cfp.ConfigParser()
           config.read(f'{self.fname}_log.txt')

           self.qmax=float(config['params']['qmax'])
           self.nq= int(config['params']['nq'])
           self.ntheta = int(config['params']['ntheta'])
           self.hflag = bool(config['params']['hflag'])
           file_vol = np.fromfile(f'{self.fname}.dbin')
           self.cvol = file_vol.reshape(self.nq,self.nq, self.ntheta)

       else:
           self.qmax = qmax
           self.nq = nq
           self.ntheta = ntheta
           self.hflag = hflag
           self.fname = fname
           self.cvol = np.zeros((nq,nq,ntheta))     #init correlation volume space

    def save_dbin(self, fname, log=True):
        self.fname = fname
        vol= self.cvol.flatten()
        vol.tofile(f'{self.fname}.dbin')
        if log:
            self.save_log(f'{self.fname}_log.txt')

    def save_log(self,fname):
        f = open(fname, 'w')
        f.write('## Correlation Log File\n\n')
        f.write('[params]\n')

        f.write(f'fname = {self.fname}\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'ntheta = {self.ntheta}\n')
        f.write(f'hflag = {self.hflag}\n')
        f.close()


    def correlate(self, qti):
        '''
        correlate a list vectors qti = [ [q_mag,theta, inten.],...]
        double for loop implemented so  vectors are not correlated with self
        and uses C(q1,q2,t)=C(q2,q1,t)
        '''

        #correlating 2D diffraction patterns (|q|, theta, intensity)
        if qti.shape[1] == 3:
            # print('Correlating 2D diffraction pattern...')
            less_than_qmax = np.where(qti[:,0] < self.qmax)[0]      #only correlate less the qmax
            qti = qti[less_than_qmax]
            #for every vector
            for i, q in enumerate(qti):

                q_ind = index_x(q[0],self.qmax, self.nq)

                #start q_prime counting ahead of q (i+1)
                for q_prime in qti[i+1:]:
                    q_prime_ind = index_x(q_prime[0],self.qmax, self.nq)
                    theta = polar_angle_between(q[1], q_prime[1])
                    theta_ind = index_x(theta, 180, self.ntheta)

                    # add values to the corrlation and histograms
                    # in (q1,q2,t) and (q2,q1,t) positions
                    if self.hflag:
                        self.cvol[q_ind,q_prime_ind,theta_ind] +=1
                        self.cvol[q_prime_ind,q_ind,theta_ind] +=1
                    else:
                        self.cvol[q_ind,q_prime_ind,theta_ind] +=q[-1]*q_prime[-1]
                        self.cvol[q_prime_ind,q_ind,theta_ind] +=q[-1]*q_prime[-1]

        #correlating 3D vectors (qx,qy,qz, intensity)
        elif qti.shape[1] == 4:
            # print('Correlating 3D diffraction volume...')

            # get indices where q is less then qmax
            qmags = np.linalg.norm(qti[:,:3], axis=1) #q magnitudes
            correl_vec_indices = np.where(qmags < self.qmax)[0]

            # remove scattering vectors with magnitude less then qmax
            qti = qti[correl_vec_indices]
            qmags = qmags[correl_vec_indices]

            for i, q in enumerate(qti):
                q_mag =  qmags[i]  # np.linalg.norm(q[:3])
                q_ind = index_x(q_mag,self.qmax, self.nq)

                #start q_prime counting ahead of q (i+1)
                for j, q_prime in enumerate(qti[i+1:]):
                    q_prime_mag =  qmags[i+j+1] # np.linalg.norm(q[:3])
                    q_prime_ind = index_x(q_prime_mag,self.qmax, self.nq)

                    theta = angle_between(q[:3]/q_mag, q_prime[:3]/q_prime_mag)

                    theta_ind = index_x(theta, np.pi, self.ntheta)

                    # add values to the corrlation and histograms
                    # in (q1,q2,t) and (q2,q1,t) positions
                    if self.hflag:
                        self.cvol[q_ind,q_prime_ind,theta_ind] +=1
                        self.cvol[q_prime_ind,q_ind,theta_ind] +=1
                    else:
                        self.cvol[q_ind,q_prime_ind,theta_ind] +=q[-1]*q_prime[-1]
                        self.cvol[q_prime_ind,q_ind,theta_ind] +=q[-1]*q_prime[-1]





    def get_q1q2(self):
        im = np.zeros( (self.nq, self.ntheta))
        for qi in range(self.nq):
            im[qi,:] = self.cvol[qi,qi,:]
        return im

    def plot_q1q2(self, cmap='viridis', log=False):
        plt.figure()
        im = self.get_q1q2()
        if log:
            im = np.log10(im+1)
        plt.imshow(im, origin='lower', extent=[0,180,0,self.qmax],aspect='auto',
                  cmap=cmap)
        plt.xlabel('$\\Delta \\Psi$ [Degrees]')
        plt.ylabel('$q_1=q_2$ [\u212b$^{-1}$]')



    def convolve(self,  kern_L=2, kern_size =5, std_q = 1, std_t=1):

        q_space = np.linspace(-kern_L,kern_L, kern_size )
        t_space = np.linspace(-kern_L,kern_L, kern_size )

        kq1, kq2, kt = np.meshgrid(q_space,q_space, t_space)

        K = np.zeros( (kern_size, kern_size, kern_size))

        K = np.exp(- ( kq1**2/(2*std_q**2) + kq2**2/(2*std_q**2) + kt**2/(2*std_t**2)))
        blur = signal.fftconvolve(self.cvol, K)

        kern_size_half = int((kern_size-1)/2)
        blur = blur[kern_size_half:-kern_size_half, kern_size_half:-kern_size_half, kern_size_half:-kern_size_half ]

        return blur











@jit
def index_x(x_val, x_max, nx):
    return int(round((x_val/float(x_max))*(nx-1)))




@jit
def index_x2(x_val,x_min, x_max, nx):
    return int(round((float(x_val-x_min)/float(x_max-x_min))*(nx-1)))

@jit
def polar_angle_between(t1,t2):
    return np.abs((t1-t2+180)%360 -180)      #angle of theta

@jit
def angle_between(q1,q2):
    dot = np.dot(q1, q2)
    if dot > 1:
        dot=1.0
    elif dot < -1:
        dot = -1.0

    return np.arccos(dot)



def norm01(arr):

    arr = np.array(arr)
    arr -=np.min(arr)
    arr /=np.max(arr)
    return arr





if __name__=="__main__":
    plt.close('all')
    import time
    import os


    geo = ExpGeom('data/agipd_2304_vj_opt_v3.geom')
    run = 120



    peaks = PeakData(f'data/cxi/{run}/peaks.txt', geo)

    plt.figure()
    geo.plot_panels()
    peaks.plot_peaks()
    plt.title(f'All peaks in run {run}')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')

    frames = peaks.split_frames()

    plt.figure()
    geo.plot_panels()
    frames[0].plot_peaks()
    plt.title(f'Peaks in frame {frames[0].frameNumbers[0]} (within run {run})')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')

    plt.show()


    # mask_cor = CorrelationVol(fromfile=True, fname = 'data/masks/





#     mask1 = MaskData('data/masks/radial_mask_iwr.h5', geo, mask_value=1)
    # mask2 = MaskData('data/masks/agipd_m6_badpix.h5', geo)

    # run = 108
    # cmap='viridis'

    # geo = ExpGeom('data/agipd_2304_vj_opt_v3.geom')
    # peaks = PeakData(f'data/cxi/{run}/{run}_indxd_rpf_peaks_Nint.txt', geo, rpf_flag=True)
    # peaks.qlist = peaks.qlist[np.where(peaks.qlist[:,-3] <2.4)]

    # plt.figure()
    # plt.title(f'Radial Mask')
    # geo.plot_panels()
    # peaks.plot_peaks(cmap=1)

    # mask1.plot_peaks(cmap=1)



    # npix = 200
    # im = np.zeros( (npix, npix) )
    # xrange = (-0.055, 0.055)
    # yrange = (-0.055, 0.055)


    # xpix_lower = mask1.qlist[:, 0] > xrange[0]
    # xpix_higher = mask1.qlist[:, 0] < xrange[1]

    # xpix = xpix_lower & xpix_higher

    # ypix_lower = mask1.qlist[:, 1] > yrange[0]
    # ypix_higher = mask1.qlist[:, 1] < yrange[1]

    # ypix = ypix_lower & ypix_higher


    # pix = np.where(xpix & ypix)


    # qlist = mask1.qlist[pix[0]]


    # for q in qlist:
        # xind = index_x2(q[0],xrange[0], xrange[1], npix)
        # yind = index_x2(q[1],yrange[0], yrange[1], npix)

        # im[xind, yind] +=1



    # flat_im = im.flatten()



    # padfcorr_path = '/home/patrick/Documents/cloudstor/phd/python_projects/padfcorr/'

    # flat_im.tofile(f'{padfcorr_path}mask.dbin')


    # os.system(f'{padfcorr_path}padfcorr {padfcorr_path}config.txt')




    # mask_cor = CorrelationVol(nq=npix, ntheta=180,  
    






