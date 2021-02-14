


from .vol import Vol


class Padfvol(Vol):

    def __init__(self, nr=256, ntheta=360, rmax=1,  path=None):
        Vol.__init__(self, nr,nr,ntheta, rmax, rmax, 180, path=path)

        self.plot_r1r2 = self.plot_xy
        self.ymax = self.xmax
        self.rmax = self.xmax

        self.ny = self.nx
        self.nr = self.nx

        self.ntheta = self.nz


