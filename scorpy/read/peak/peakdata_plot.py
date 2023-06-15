



import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np







class PeakDataPlot:



    def plot_peaks(self, intenthresh=0, scatter=False, cmap=None, sizes=None,  peakr=None, fig=None, ax=None):

        
        if fig is None:
            fig, ax = plt.subplots(1,1)

        self.plot_panels(fig=fig, ax=ax)



        x = self.scat_rect[:,0]
        y = self.scat_rect[:,1]
        colors = self.scat_rect[:,-1]
        marker = 'o'



        loc = np.where(colors>intenthresh)

        x = x[loc]
        y = y[loc]

        colors = colors[loc]


        if sizes is not None:
            sizes = (np.max(sizes)-np.min(sizes))*(colors-colors.min())/(colors.max()-colors.min()) + np.min(sizes)
        else:
            sizes = 15

        ax.scatter(x, y, c=colors, s=sizes, cmap=cmap, marker=marker)


        # plt.colorbar()


    def label_qphi(self,dx, dy):

        x = self.scat_rect[:,0]
        y = self.scat_rect[:,1]

        qs = self.scat_qpol[:,0]
        phis = self.scat_qpol[:,1]
        for peakx, peaky, q, phi in zip(x, y, qs, phis):
            plt.text(peakx+dx, peaky+dy, f'({round(q, 2)}, {round(phi,2)})', fontsize=6)





    def plot_peakr(self, peakr, ec='red', ls=':', fig=None, ax=None):

        if fig is None:
            plt.figure()
        if ax is None:
            ax = plt.gca()

        x = self.scat_rect[:,0]
        y = self.scat_rect[:,1]
        for peakx, peaky in zip(x, y):

            circ = patches.Circle( (peakx,peaky), radius=peakr, fill=False, ec=ec, alpha=1, lw=1, ls=ls)
            ax.add_patch(circ)

    def plot_panels(self, panel_label=True, fs_arrow=False, ss_arrow=True, units='m', fig=None, ax=None):
        '''
        Plot the panels in the experiment geometry.

        Arguments:
            None.

        Returns:
            None.
            '''
        if fig is None:
            plt.figure()
        if ax is None:
            ax = plt.gca()
        ax.set_aspect('equal')


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
            ax.add_patch(rect)

            # plot an X in the (0,0) corner, add a label here as well
            ax.plot(panel['corner_xy'][0] / (self.res*sf),
                     panel['corner_xy'][1] / (self.res*sf), 'rx')

            if panel_label:
                ax.text(panel['corner_xy'][0] / (self.res*sf), panel['corner_xy']
                         [1] / (self.res*sf), panel['name'], fontsize=6)

            if fs_arrow:
                ax.arrow(panel['corner_xy'][0] / (self.res*sf),panel['corner_xy'][1] / (self.res*sf),
                          30*panel['fs_xy'][0]/(self.res*sf), 30*panel['fs_xy'][1]/(self.res*sf),
                         color='blue')
#             if ss_arrow:
                # plt.arrow(panel['corner_xy'][0] / (self.res*sf),panel['corner_xy'][1] / (self.res*sf),
                          # 30*panel['ss_xy'][0]/(self.res*sf), 30*panel['ss_xy'][1]/(self.res*sf),
                         # color='red')
        # plt.vlines(0, -0.005, 0.005)
        # plt.hlines(0, -0.005, 0.005)
        cross_hair = 30/(self.res*sf)
        

        ax.vlines(0, -cross_hair, cross_hair)
        ax.hlines(0, -cross_hair, cross_hair)


        ax.set_xlabel(f'x [{units}]')
        ax.set_ylabel(f'y [{units}]')


    def plot_qring(self, q=1, ec='purple', ls=":"):
        r = self.convert_q2r(q)
        circ = patches.Circle( (0,0), radius=r, fill=False, ec=ec, alpha=1, lw=1, ls=ls)
        plt.gca().add_patch(circ)











