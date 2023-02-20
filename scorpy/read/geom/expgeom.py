import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import configparser as cfp


from .expgeom_props import ExpGeomProps
from .expgeom_plot import ExpGeomPlot

class ExpGeom(ExpGeomProps, ExpGeomPlot):

    def __init__(self, path):
        '''
        Handler for .geom parameter files
        path: str of the path to the .geom file
        '''

        self.path = path
        self.file_args, self.panel_args = self.parse_file()
        # pixel resolution (~5000 Pix/m, 200 e-6 m/Pix)
        self.res = float(self.file_args['res'])
        self.clen = float(self.file_args['clen'])  # camera length
        self.photon_energy = float(self.file_args['photon_energy'])  # eV


        #props
        self.wavelength = (4.135667e-15 * 2.99792e8 *1e10) / self.photon_energy  # A
        self.k = (2 * np.pi) / self.wavelength # 1/A

        self.panels = self.make_panels(self.panel_args)  # make the panels

    def translate_pixels(self, pk_df):
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

        # pix_pos = np.zeros((len(pix_sss), 3))

        # panel_mods = np.floor(pix_sss / self.nss)

        print('pix_posx.shape')
        print(pix_posx.shape)

        print('pk_df.shape')
        print(pk_df.shape)


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







    def parse_file(self):
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

        parsed_args = {}
        parsed_panels = {}

        for line in config['params']:
            if '/' in line:  # check if thise argument is a panel eg. p0a4/fs
                # if it is a panel, split by name/attribute, add to panel_dict
                panel_split = line.split('/')
                # if the panel is no already in the dictionary
                if panel_split[0] not in parsed_panels.keys():
                    parsed_panels[panel_split[0]] = {}  # add panel
                    # set the name key
                    parsed_panels[panel_split[0]]['name'] = panel_split[0]

                # after adding the panel, add the panel attribute
                parsed_panels[panel_split[0]][panel_split[1]
                                              ] = config['params'][line]

            else:  # if the argument is not a panel argument, add to the arg dictionary instead
                parsed_args[line] = config['params'][line]

        return parsed_args, parsed_panels




    def make_panels(self, file_panels):
        '''
        Parse panel arguments and make each panel.

        Arguments:
            file_panels (dict): dictionary of panel arguments from geom file.

        Returns:
            panels (list): List of panel dictionaries.
        '''
        panels = []  # init a list of panels

        for key in file_panels.keys():  # for every panel in the parsed panels
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


    def convert_r2q(self, r):
        theta = np.arctan2(r, self.clen)
        return 2*self.k*np.sin(theta/2)

    def convert_q2r(self, q):
        arcs = np.arcsin(q/(2*self.k))
        return np.tan(2*arcs)*self.clen
