
import scorpy
import numpy as np

from scorpy.utils import angle_between_sph









def test_angle_between_sph():

    melbourne = (127.8, 144)

    np.testing.assert_almost_equal(angle_between_sph(0, np.pi/2, 0, 0), np.pi/2)
    np.testing.assert_almost_equal(angle_between_sph(np.pi/4, 3*np.pi/4, 0, 0), np.pi/2)
    np.testing.assert_almost_equal(angle_between_sph(3*np.pi/4, np.pi/4, 0, 0), np.pi/2)
    np.testing.assert_almost_equal(angle_between_sph(np.pi/2, np.pi/2, 0, np.pi/2), np.pi/2)
    np.testing.assert_almost_equal(angle_between_sph(np.pi/2, np.pi/2, 0, np.pi/6), np.pi/6)


    np.testing.assert_almost_equal(angle_between_sph(np.pi, 0, np.pi, np.pi/2), np.pi)
    np.testing.assert_almost_equal(angle_between_sph(np.pi, np.pi, np.pi, np.pi/2), 0)
    np.testing.assert_almost_equal(angle_between_sph(0, np.pi, np.pi, np.pi/2), np.pi)

    np.testing.assert_almost_equal(angle_between_sph(0, 0, np.pi, np.pi/2), 0)

    melbourne = (127.816599, 144.962957)
    jakata = (96.215718, 106.850080)
    r_earth = 6371


    theta_m2j = angle_between_sph(np.radians(melbourne[0]), np.radians(jakata[0]), np.radians(melbourne[1]), np.radians(jakata[1]))
    arc = theta_m2j*r_earth

    np.testing.assert_almost_equal(np.round(arc), 5206)


