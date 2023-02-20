import numpy as np
import configparser as cfp



class ExpGeom:



    def parse_geom_file(self):
        '''
        Parse the geom file for experiment details.

        Arguments:
            None.

        Returns:
            parsed_args (dict): experimental arguments
            parsed_panels (dict): description of panels
        '''

        f = open(self.geompath, 'r')
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
            this_panel['min_fs'] = int(geom_params['panels'][key]['min_fs'])
            this_panel['min_ss'] = int(geom_params['panels'][key]['min_ss'])
            this_panel['max_ss'] = int(geom_params['panels'][key]['max_ss'])
            this_panel['max_fs'] = int(geom_params['panels'][key]['max_fs'])
            this_panel['coffset'] = float(geom_params['panels'][key]['coffset'])

            fs_xy = geom_params['panels'][key]['fs'].split()
            this_panel['fs_xy'] = [float(fs_xy[0][:-1]),
                                   float(fs_xy[1][:-1])]

            ss_xy = geom_params['panels'][key]['ss'].split()
            this_panel['ss_xy'] = [float(ss_xy[0][:-1]),
                                   float(ss_xy[1][:-1])]

            this_panel['corner_xy'] = [float(geom_params['panels'][key]['corner_x']),
                                       float(geom_params['panels'][key]['corner_y'])]
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

