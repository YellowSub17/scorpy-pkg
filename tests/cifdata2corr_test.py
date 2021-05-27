import scorpy
from scorpy.utils import index_x
import numpy as np

import matplotlib.pyplot as plt





data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data/'



def test_main():

    cif = scorpy.CifData(f'{data_dir}cifdata/cifdata2corr_test-sf.cif')

    # cif
    #### h, k ,l, I
    #   0,0,1, 1
    #   1,1,0, 2
    #   1,1,1, 3

    corr = scorpy.CorrelationVol(10, 36,cif.qmax)


    corr.fill_from_cif(cif)

    loc1 = (np.array([5, 5, 5, 5, 5, 5, 5, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9]),
            np.array([5, 5, 5, 5, 8, 9, 9, 5, 8, 8, 8, 8, 9, 9, 5, 5, 8, 8, 9, 9, 9, 9, 9]),
            np.array([ 0, 11, 18, 25, 18, 11, 25, 18,  0,  7, 18, 29,  7, 29, 11, 25,  7, 29,  0,  7, 11, 25, 29]))

    loc2 = np.where(corr.vol !=0)

    for i in range(3):
        np.testing.assert_array_equal(loc1[i], loc2[i])

    corrI = np.array([ 4.,  3.,  4.,  3.,  4.,  3.,  3.,  4., 16.,  6.,  4.,  6.,  6., 6.,  3.,  3.,  6.,  6., 36.,  6.,  3.,  3.,  6.])

    np.testing.assert_array_equal(corr.vol[loc1], corrI)






if __name__ == "__main__":


    cif = scorpy.CifData(f'{data_dir}cifdata/cifdata2corr_test-sf.cif')

    corr = scorpy.CorrelationVol(10, 36,cif.qmax)


    corr.fill_from_cif(cif)

    loc1 = (np.array([5, 5, 5, 5, 5, 5, 5, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9]),
            np.array([5, 5, 5, 5, 8, 9, 9, 5, 8, 8, 8, 8, 9, 9, 5, 5, 8, 8, 9, 9, 9, 9, 9]),
            np.array([ 0, 11, 18, 25, 18, 11, 25, 18,  0,  7, 18, 29,  7, 29, 11, 25,  7, 29,  0,  7, 11, 25, 29]))

    loc2 = np.where(corr.vol !=0)

    for i in range(3):
        np.testing.assert_array_equal(loc1[i], loc2[i])

    corrI = np.array([ 4.,  3.,  4.,  3.,  4.,  3.,  3.,  4., 16.,  6.,  4.,  6.,  6., 6.,  3.,  3.,  6.,  6., 36.,  6.,  3.,  3.,  6.])

    np.testing.assert_array_equal(corr.vol[loc1], corrI)



