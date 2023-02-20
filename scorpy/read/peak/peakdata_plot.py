



import matplotlib.pyplot as plt
import numpy as np







class PeakDataPlot:



    def plot_peaks(self, intenthresh=50, scatter=False, cmap=None, sizes=None,  newfig=True):

        if newfig:
            plt.figure()
        self.geom.plot_panels()


        x = self.scat_rect[:,1]
        y = self.scat_rect[:,2]
        colors = self.scat_rect[:,-1]
        marker = 'o'

        # x = x[::skippeaks]
        # y = y[::skippeaks]
        # colors = colors[::skippeaks]


        loc = np.where(colors>intenthresh)

        x = x[loc]
        y = y[loc]

        colors = colors[loc]


        if sizes is not None:
            sizes = (np.max(sizes)-np.min(sizes))*(colors-colors.min())/(colors.max()-colors.min()) + np.min(sizes)
        else:
            sizes = 15

        plt.scatter(x, y, c=colors, s=sizes, cmap=cmap, marker=marker)
        plt.colorbar()

    def plot_panels(self, panel_label=True, fs_arrow=True, ss_arrow=True, units='m'):
        '''
        Plot the panels in the experiment geometry.

        Arguments:
            None.

        Returns:
            None.
        '''
        plt.axis('equal')


        if units=='m':
            sf=1

        elif units=='pix':
            sf = 1/self.res

        for panel in self.panels:

            rect_width = panel['fs_xy'][1] * \
                (panel['max_fs'] - panel['min_fs']) / (self.res*sf)
            rect_height = panel['ss_xy'][0] * \
                (panel['max_ss'] - panel['min_ss']) / (self.res*sf)

            rect_rot = np.degrees(np.arctan2( np.abs(panel['fs_xy'][1]), panel['fs_xy'][0]))

            # corner of the panel
            rect_x = panel['corner_xy'][0] / (self.res*sf)
            rect_y = panel['corner_xy'][1] / (self.res*sf)

            # rectangle object
            rect = patches.Rectangle((rect_x, rect_y), rect_width, -rect_height, rect_rot,
                                     fill=False, ec='red', alpha=1, lw=1)

            # add the rectangle object to the plot
            plt.gca().add_patch(rect)

            # plot an X in the (0,0) corner, add a label here as well
            plt.plot(panel['corner_xy'][0] / (self.res*sf),
                     panel['corner_xy'][1] / (self.res*sf), 'rx')

            if panel_label:
                plt.text(panel['corner_xy'][0] / (self.res*sf), panel['corner_xy']
                         [1] / (self.res*sf), panel['name'], fontsize=6)

            if fs_arrow:
                plt.arrow(panel['corner_xy'][0] / (self.res*sf),panel['corner_xy'][1] / (self.res*sf),
                          30*panel['fs_xy'][0]/(self.res*sf), 30*panel['fs_xy'][1]/(self.res*sf),
                         color='blue')
#             if ss_arrow:
                # plt.arrow(panel['corner_xy'][0] / (self.res*sf),panel['corner_xy'][1] / (self.res*sf),
                          # 30*panel['ss_xy'][0]/(self.res*sf), 30*panel['ss_xy'][1]/(self.res*sf),
                         # color='red')
        # plt.vlines(0, -0.005, 0.005)
        # plt.hlines(0, -0.005, 0.005)
        cross_hair = 30/(self.res*sf)
        

        plt.vlines(0, -cross_hair, cross_hair)
        plt.hlines(0, -cross_hair, cross_hair)


        plt.xlabel(f'x [{units}]')
        plt.ylabel(f'y [{units}]')


    def plot_qring(self, q=1, ec='purple', ls=":"):
        r = self.convert_q2r(q)
        circ = patches.Circle( (0,0), radius=r, fill=False, ec=ec, alpha=1, lw=1, ls=ls)
        plt.gca().add_patch(circ)











