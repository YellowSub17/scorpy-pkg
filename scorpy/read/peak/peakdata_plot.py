



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






