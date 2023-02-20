import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
from ..geom.expgeom import ExpGeom
from ...utils.env import DATADIR
from ...utils.utils import index_x, convert_rect2pol

from .peakdata_props import PeakDataProperties
from .peakdata_plot import PeakDataPlot




class PeakData(PeakDataProperties, PeakDataPlot):

    def __init__(self, h5path, geompath):
        '''
        handler for a peaks.txt file
        df: dataframe of the peak data, or str file path to txt
        geo: ExpGeom object associated to experiement geomtery
        '''

        self._geompath = geompath

        self._geom_params = self.parse_geom_file()


        self._h5path = h5path

        with h5py.File(self.path) as h5file:
            h5data = h5file['/entry_1/instrument_1/detector_1/data'][:]



        ss_pixel, fs_pixels =  np.where(h5data>0) # fs is the cols
        intens = h5data[ss_pixels, fs_pixels]

        self._scat_fs_ss = np.array([ fs_pixels, ss_pixels, intens]).T


        xyz_pixel = self.fsss2xyz(self._scat_fs_ss)



        rphi = convert_rect2pol(xyz_pixel[:,0:2])

        diff_cone_angle = np.arctan2(rphi[:,0], xyz_pixel[:, 2])

        q_mag = 2*self.k*np.sin(0.5*diff_cone_angle)

        saldin_sph_theta = np.pi/2 - np.arcsin((q_mag)/(2*self.k))



        self._scat_rect = np.array([ xyz_pixel[:,0], xyz_pixel[:,1], xyz_pixel[:,2], intens]).T

        self._scat_rpol = np.array([ rphi[:,0], rphi[:,1], intens ]).T

        self._scat_tpol = np.array([np.arctan2(pol_r_mag, xyz_pixel[:, 2]), rphi[:,1], intens ]).T

        self._scat_qpol = np.array(q_mag , rphi[:,1], intens ]).T

        self._scat_sph = np.array(q_mag, saldin_sph_theta, rphi[:,1], intens ]).T






    def make_im(self, npix, r, bool_inten=False, fname=None):

        im = np.zeros( (npix,npix) )

        loc = np.where(np.linalg.norm(self.scat_rect[:,0:2], axis=1)<r)[0]

        ite = np.ones( len(loc))

        xinds = map(index_x, self.scat_rect[loc,0], -r*ite, r*ite, ite*npix)
        yinds = map(index_x, self.scat_rect[loc,1], -r*ite, r*ite, ite*npix)

     

        for xind, yind, inten in zip(xinds, yinds, self.scat_rect[loc,-1]):
            im[xind, yind] += inten

        if bool_inten:
            im[im>0] = 1
            im[im<0] = 0

        if fname is not None:
            flat_im = im.flatten()
            flat_im.tofile(fname)

        return im.T





    def integrate_peaks(self, r):

        pixels = self.scat_rect[self.scat_rect[:, -1].argsort()]

        pixel_averaged_bool = np.zeros(pixels.shape[0])

        pixels = pixels[::-1]

        integrated_peaks_list = []

        for i, pixel in enumerate(pixels):

            if pixel_averaged_bool[i] ==1:
                continue

            dxypixels = pixels - pixel

            dr = np.linalg.norm(dxypixels[:,0:2], axis=1)
            loc = np.where(dr<r)
            pixel_averaged_bool[loc] = 1

            if loc[0].shape[0] ==1:
                integrated_peaks_list.append(pixel)
                continue
            else:
                peak = np.average(pixels[loc], axis=0, weights=pixels[loc,-1].flatten())
                peak[-1] = np.sum(pixels[loc], axis=0)[-1]
                integrated_peaks_list.append(peak)



        return np.array(integrated_peaks_list)












    def parse_geom_file(self):
        '''
        Parse the geom file for experiment details.

        Arguments:
            None.

        Returns:
            parsed_args (dict): experimental arguments
            parsed_panels (dict): description of panels
        '''

        f = open(self.path, 'r')
        cont = f.read()
        cont = '[params]' + cont
        config = cfp.ConfigParser(
            interpolation=None, inline_comment_prefixes=(';'))
        config.read_string(cont)

        geom_params = {'panels':{}}

        for line in config['params']:
            if '/' in line:  # check if thise argument is a panel eg. p0a4/fs
                # if it is a panel, split by name/attribute, add to panel_dict
                panel_split = line.split('/')
                # if the panel is no already in the dictionary
                if panel_split[0] not in geom_params['panels'].keys():
                    geom_params['panels'][panel_split[0]] = {}  # add panel
                    # set the name key
                    geom_params['panels'][panel_split[0]]['name'] = panel_split[0]

                # after adding the panel, add the panel attribute
                geom_params['panels'][panel_split[0]][panel_split[1]
                                              ] = config['params'][line]

            else:  # if the argument is not a panel argument, add to the arg dictionary instead
                geom_params[line] = config['params'][line]

        panels = []

        for key in geom_params['panels'].keys():
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

        geom_params['panels'] = panels


        return geom_params


    def fsss2xyz(self, pk_df):
        '''
        Translate pixel indices of fast and slow scan directions into position.

        Arguments:
            pix_sss: list of pixels indices in slow scan direction.
            pix_fss: list of pixels indices in fast scan direction.

        Returns:
            pos: list of pixels positions in real space coordinates, (x,y,z).
        '''

        pix_posx = np.zeros(pk_df.shape[0])
        pix_posy = np.zeros(pk_df.shape[0])
        pix_posz = np.zeros(pk_df.shape[0])




        for i_p, panel in enumerate(self.panels):

            pix_fs_in_panel_cond = np.logical_and( pk_df[:,0] >= panel['min_fs'], pk_df[:,0] <= panel['max_fs'] )
            pix_ss_in_panel_cond = np.logical_and( pk_df[:,1] >= panel['min_ss'], pk_df[:,1] <= panel['max_ss'] )

            loc = np.where(np.logical_and(pix_fs_in_panel_cond, pix_ss_in_panel_cond))

   

            nfs = panel['max_fs'] -panel['min_fs']
            nss = panel['max_ss'] -panel['min_ss']

            pix_posx[loc] = panel['fs_xy'][0] * (pk_df[loc,0] % nfs) \
                + panel['ss_xy'][0] * (pk_df[loc,1] % nss)

            pix_posy[loc] = panel['fs_xy'][1] * (pk_df[loc,0] % nfs) \
                + panel['ss_xy'][1] * (pk_df[loc,1] % nss)

            pix_posz[loc] = panel['coffset']

            # translate according to corner of panel
            pix_posx[loc] += panel['corner_xy'][0]
            pix_posy[loc] += panel['corner_xy'][1]

        rect_pos = np.array([pix_posx / self.res, pix_posy / self.res, pix_posz + self.clen]).T

        return rect_pos

