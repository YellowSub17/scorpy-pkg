import numpy as np







class KlnmHandler:




    def __init__(self, nl, nq):
        self.nq = nq
        self.nl = nl

        self.vals = []

        for l in range(nl):
            self.vals.append( np.zeros((nq, 2*l+1)))


    def fill_ilm(self, sphv):
        coeffs = sphv.get_all_q_coeffs()

        for l in range(self.nl):

            klnm_vals = np.zeros( (self.nq, 2*l+1))
            for q_ind in range(self.nq):
                q_coeffs = coeffs[q_ind]

                for im, m in zip( range(0, 2*l+1), range(-l, l+1)):
                    if m <0:
                        klnm_vals[q_ind, im] = q_coeffs[1, l, abs(m)]
                    else:
                        klnm_vals[q_ind, im] = q_coeffs[0, l, abs(m)]


            self.vals[l] = np.round(klnm_vals,15)






    def fill_klnm(self, bl_u):
        pass

    def fill_kprime(self, bl_l):
        pass

        
