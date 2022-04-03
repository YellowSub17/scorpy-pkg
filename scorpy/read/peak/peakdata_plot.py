



import matplotlib.pyplot as plt







class PeakDataPlot:



    def plot_peaks(self, scatter=False, cmap=None, sizes=None,  newfig=True):

        if newfig:
            plt.figure()
        self.geom.plot_panels()


        x = self.scat_rect[:,1]
        y = self.scat_rect[:,2]
        colors = self.scat_rect[:,-1]
        marker = 'o'

        if sizes is not None:
            sizes = (np.max(sizes)-np.min(sizes))*(colors-colors.min())/(colors.max()-colors.min()) + np.min(sizes)
        else:
            sizes = 15

        plt.scatter(x, y, c=colors, s=sizes, cmap=cmap, marker=marker)
        plt.colorbar()






