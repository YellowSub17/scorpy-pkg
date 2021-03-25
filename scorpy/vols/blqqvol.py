

from .vol import Vol
import numpy as np
from scipy import special
import matplotlib.pyplot as plt



class BlqqVol(Vol):
    '''
    Representation of the B_l(q1,q2) volume, an invertible correlation matrix.

    Arguments:
        nq (int): number of scattering magnitude bins.
        nl (int): number of spherical harmonics (inc. 0th harmonic, so 1+lmax).
        qmax (float): correlation magnitude limit [1/A].
        path (str): path to dbin (and log) if being created from memory.
    '''


    def __init__(self, nq=100, nl=37, qmax=1, path=None, comp=False):
        Vol.__init__(self, nq,nq,nl, qmax, qmax, nl, comp, path=path)

        self.plot_q1q2 = self.plot_xy


    @property
    def qmax(self):
        return self.xmax

    @property
    def nq(self):
        return self.nx

    @property
    def nl(self):
        return self.nz

    @property
    def blvol(self):
        return self.vol

    @blvol.setter
    def blvol(self, new_vol):
        self.vol = new_vol




    def fill_from_corr(self,cor):
        assert cor.qmax == self.qmax, 'CorrelationVol and BlqqVol have different qmax'
        assert cor.nq == self.nq, 'CorrelationVol and BlqqVol have different nq'

        print('Filling BlqqVol from CorrelationVol\n')

        q_range = np.linspace(0,self.qmax, self.nq)
        # create args of legendre eval

        #TODO add ewald sphere
        args = np.cos( np.linspace(0, np.pi, cor.ntheta))

        # initialze fmat matrix
        fmat = np.zeros( (cor.ntheta, self.nl) )

        #for every even spherical harmonic
        for l in range(0, self.nl, 2):
            leg_vals = (1/(4*np.pi))*special.eval_legendre(l, args)
            # leg_vals = ((2*l+1)/(4*np.pi))*special.eval_legendre(l, args)
            fmat[:,l] = leg_vals


        #TODO check svd
        fmat_inv = np.linalg.pinv(fmat, rcond=1e-2)


        ident = np.matmul(fmat_inv, fmat)
        # ident = np.matmul(fmat, fmat_inv)


        # plt.figure()
        # plt.imshow(fmat_inv)
        # plt.title('fmat_inv')
        plt.figure()
        plt.imshow(ident)
        plt.title('indent')

        for iq1 in range(self.nq):
            for iq2 in range(iq1, self.nq):
                dot =  np.dot(fmat_inv,cor.vol[iq1,iq2,:])
                self.vol[iq1,iq2,:] = dot
                self.vol[iq2,iq1,:] = dot

        # for l in range(1, self.nl, 2):
            # self.vol[...,l] *=0

        # times 4pi because we multi 2root(pi) in the ylm calc.
        self.vol *= 4*np.pi




    def fill_from_sph(self, sph):
        print(f'Calculating BlqqVol from SphHarmHandler\n')

        if self.comp:
            bl = np.zeros((self.nq, self.nq), dtype=np.complex128)
        else:
            bl = np.zeros((self.nq, self.nq))

        for l in range(0, self.nl, 2):
            for iq1 in range(self.nq):
                for iq2 in range(iq1, self.nq):
                    bl[iq1,iq2] = np.sum(np.conj(sph.vals_lnm[l][iq1])*sph.vals_lnm[l][iq2])
                    bl[iq2,iq1] = np.sum(np.conj(sph.vals_lnm[l][iq2])*sph.vals_lnm[l][iq1])

            self.vol[...,l] = bl






