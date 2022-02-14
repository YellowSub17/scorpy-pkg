import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import configparser as cfp


class ExpGeom:

    def __init__(self, filename, nfs = 128, nss = 64):
        '''
        Handler for .geom parameter files
        filename: str of the path to the .geom file
        '''

        self.filename = filename
        self.file_args, self.panel_args = self.parse_file()
        # pixel resolution (~5000 Pix/m, 200 e-6 m/Pix)
        self.res = float(self.file_args['res'])
        self.clen = float(self.file_args['clen'])  # camera length
        self.photon_energy = float(self.file_args['photon_energy'])  # eV

        self.nfs = nfs
        self.nss = nss
        
        #props
        self.wavelength = (4.135667e-15 * 2.99792e8 *1e10) / self.photon_energy  # A
        self.k = (2 * np.pi) / self.wavelength # 1/A

        self.panels = self.make_panels(self.panel_args)  # make the panels

    def translate_pixels(self, pix_sss, pix_fss):
        '''
        Translate pixel indices of fast and slow scan directions into position.

        Arguments:
            pix_sss: list of pixels indices in slow scan direction.
            pix_fss: list of pixels indices in fast scan direction.

        Returns:
            pos: list of pixels positions in real space coordinates, (x,y,z).
        '''

        pix_posx = np.zeros((len(pix_sss)))
        pix_posy = np.zeros((len(pix_sss)))
        pix_posz = np.zeros((len(pix_sss)))

        pix_pos = np.zeros((len(pix_sss), 3))

        panel_mods = np.floor(pix_sss / self.nss)

        for i_p, panel in enumerate(self.panels):
            if np.floor(panel['min_ss'] / self.nss) not in panel_mods:
                continue
            else:
                loc = np.where(int(panel['min_ss'] / self.nss) == panel_mods)

                pix_posx[loc] = panel['fs_xy'][0] * (pix_fss[loc] % self.nfs) \
                    + panel['ss_xy'][0] * (pix_sss[loc] % self.nss)

                pix_posy[loc] = panel['fs_xy'][1] * (pix_fss[loc] % self.nfs) \
                    + panel['ss_xy'][1] * (pix_sss[loc] % self.nss)

                pix_posz[loc] = panel['coffset']

                # translate according to corner of panel
                pix_posx[loc] += panel['corner_xy'][0]
                pix_posy[loc] += panel['corner_xy'][1]

        return np.array([pix_posx / self.res, pix_posy / self.res, pix_posz + self.clen]).T

    def parse_file(self):
        '''
        Parse the geom file for experiment details.

        Arguments:
            None.

        Returns:
            parsed_args (dict): experimental arguments
            parsed_panels (dict): description of panels
        '''

        f = open(self.filename, 'r')
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

    def plot_panels(self):
        '''
        Plot the panels in the experiment geometry.

        Arguments:
            None.

        Returns:
            None.
        '''
        plt.axis('equal')
        plt.vlines(0, -0.005, 0.005)
        plt.hlines(0, -0.005, 0.005)
    
        for panel in self.panels:
            # size of the panel
            # check if we implemented the fs_xy and ss_xy correctly
            # I think all they are doing atm is multiplying +-1 for
            # to flip the rectangle
            rect_width = panel['fs_xy'][1] * \
                (panel['max_fs'] - panel['min_fs']) / self.res
            rect_height = panel['ss_xy'][0] * \
                (panel['max_ss'] - panel['min_ss']) / self.res
            
            # print(rect_width, rect_height)


            # rotation of the panel, trig from fs directions
            # should be close to 90 or 270 degrees
            # print('WARNING: PANEL ROTATION NOT CALCULATED (expgeom.py)')
            # print('assuming 0 rotation')
            # rect_rot = 90

          #   rect_rot = (panel['fs_xy'][0]**2 + panel['fs_xy']
                        # [1]**2)**(1 / 2) / (panel['fs_xy'][0])
            # rect_rot = np.degrees(np.arccos(np.clip(1 / rect_rot, -1, 1)))


            rect_rot = np.degrees(np.arctan2( np.abs(panel['fs_xy'][1]), panel['fs_xy'][0]))

            # corner of the panel
            rect_x = panel['corner_xy'][0] / self.res
            rect_y = panel['corner_xy'][1] / self.res

            # rectangle object
            rect = patches.Rectangle((rect_x, rect_y), rect_width, -rect_height, rect_rot,
                                     fill=False, ec='red', alpha=1, lw=1)

            # add the rectangle object to the plot
            plt.gca().add_patch(rect)

            # plot an X in the (0,0) corner, add a label here as well
            plt.plot(panel['corner_xy'][0] / self.res,
                     panel['corner_xy'][1] / self.res, 'rx')
            plt.text(panel['corner_xy'][0] / self.res, panel['corner_xy']
                     [1] / self.res, panel['name'], fontsize=6)
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')

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
