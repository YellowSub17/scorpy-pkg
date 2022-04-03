import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import configparser as cfp


class ExpGeomPlot:




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

            rect_width = panel['fs_xy'][1] * \
                (panel['max_fs'] - panel['min_fs']) / self.res
            rect_height = panel['ss_xy'][0] * \
                (panel['max_ss'] - panel['min_ss']) / self.res

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


    def plot_qring(self, q=1, ec='purple', ls=":"):
        r = self.convert_q2r(q)
        circ = patches.Circle( (0,0), radius=r, fill=False, ec=ec, alpha=1, lw=1, ls=ls)
        plt.gca().add_patch(circ)





