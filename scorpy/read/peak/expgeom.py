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

        self.geom_args, self.panel_args = self.parse_geom_file()

        # pixel resolution (~5000 Pix/m, 200 e-6 m/Pix)
        self.res = float(self.file_args['res'])
        self.clen = float(self.file_args['clen'])  # camera length
        self.photon_energy = float(self.file_args['photon_energy'])  # eV


        #props
        self.wavelength = (4.135667e-15 * 2.99792e8 *1e10) / self.photon_energy  # A
        self.k = (2 * np.pi) / self.wavelength # 1/A

        self.panels = self.make_panels(self.panel_args)  # make the panels









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




    def make_panels(self):
        '''
        Parse panel arguments and make each panel.

        Arguments:
            file_panels (dict): dictionary of panel arguments from geom file.

        Returns:
            panels (list): List of panel dictionaries.
        '''
        panels = []  # init a list of panels

        for key in self.geom_args['panels'].keys():  # for every panel in the parsed panels
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
