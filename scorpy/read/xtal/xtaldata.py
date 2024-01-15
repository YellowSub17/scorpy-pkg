





class XtalData:



    def __init__(self, a_mag=1, b_mag=1, c_mag=1,
                 alpha=90, beta=90, gamma=90,
                 qmax=1, rotk=[1,0,0], rottheta=0):


        self.qmax = qmax



        ### get cell angles
        self.alpha = np.radians(alpha)
        self.beta = np.radians(beta)
        self.gamma = np.radians(gamma)

        ### get cell sides
        self.a_mag = a_mag
        self.b_mag = b_mag
        self.c_mag = c_mag

        self.rotk = rotk
        self.rottheta=rottheta

        # self.spg = spg

        ### calculate lattice vectors
        a_unit = np.array([1.0, 0.0, 0.0])
        b_unit = np.array([np.cos(self.gamma), np.sin(self.gamma), 0])
        c_unit = np.array([
            np.cos(self.beta),
            (np.cos(self.alpha) - np.cos(self.beta) * np.cos(self.gamma)) / np.sin(self.gamma),
            np.sqrt(1 - np.cos(self.beta)**2 - ( (np.cos(self.alpha) - np.cos(self.beta) * np.cos(self.gamma)) / np.sin(self.gamma))**2)
        ])


        units = [a_unit, b_unit, c_unit]
        mags = [self.a_mag, self.b_mag, self.c_mag]


        rotk = rotk/np.linalg.norm(rotk)
        c = np.cos(rottheta)
        s = np.sin(rottheta)


        abc = np.zeros((3,3))
        for i, (unit, mag) in enumerate(zip(units, mags)):
            #rodriguiz formula
            rot_unit =  c*unit + (1-c)*np.dot(unit, rotk)*rotk + s*(np.cross(rotk, unit))

            abc[i] = rot_unit*mag

        abc = np.round(abc, 14)

        self.a, self.b, self.c = abc


        ### calculate reciprocal lattice vectors

        cell_volume = np.dot(self.a, np.cross(self.b, self.c))

        self.ast = 2 * np.pi * np.cross(self.b, self.c) / cell_volume
        self.bst = 2 * np.pi * np.cross(self.c, self.a) / cell_volume
        self.cst = 2 * np.pi * np.cross(self.a, self.b) / cell_volume

        ### calculate reciprocal lattice vector magnitudes

        self.ast_mag = np.linalg.norm(self.ast)
        self.bst_mag = np.linalg.norm(self.bst)
        self.cst_mag = np.linalg.norm(self.cst)



    def calc_scat(self):

        ast_max_bragg_ind = int(self.qmax/self.ast_mag)+1
        bst_max_bragg_ind = int(self.qmax/self.bst_mag)+1
        cst_max_bragg_ind = int(self.qmax/self.cst_mag)+1

        ast_ite = np.arange(-ast_max_bragg_ind, ast_max_bragg_ind+1)
        bst_ite = np.arange(-bst_max_bragg_ind, bst_max_bragg_ind+1)
        cst_ite = np.arange(-cst_max_bragg_ind, cst_max_bragg_ind+1)

        bragg_xyz = np.array(list(itertools.product( ast_ite, bst_ite, cst_ite)))
        loc_000 = np.all(bragg_xyz == 0, axis=1)  # remove 000 reflection
        bragg_xyz = bragg_xyz[~loc_000]

        rect_xyz = np.matmul(
            bragg_xyz, np.array([self.ast, self.bst, self.cst]))

        sph_qtp = convert_rect2sph(rect_xyz)




        qloc = np.where(sph_qtp[:,0] <= self.qmax)

        bragg_xyz = bragg_xyz[qloc]
        rect_xyz = rect_xyz[qloc]
        sph_qtp = sph_qtp[qloc]



        q_inds = sphv.get_indices(sph_qtp[:,0], axis=0)
        theta_inds = sphv.get_indices(sph_qtp[:,1], axis=1)
        phi_inds = sphv.get_indices(sph_qtp[:,2], axis=2)

        I = np.zeros(sph_qtp.shape[0])
        for i, (q_ind, theta_ind, phi_ind ) in enumerate(zip(q_inds, theta_inds, phi_inds )):
            I[i] += sphv.vol[q_ind, theta_ind, phi_ind]







