from scorpy.utils import index_x, angle_between, polar_angle_between
import numpy as np


def test_polar_angle_between():
    '''
    testing the polar_angle_between function
    '''

    #t1=t2
    assert np.allclose(polar_angle_between(10,10), 0)

    # t1>t2
    assert np.allclose(polar_angle_between(90, 30), 60)

    # t2>t1
    assert np.allclose(polar_angle_between(15.4, 60), 44.6)

    # t2>360
    assert np.allclose(polar_angle_between(0, 4345),  4345%360 )

    # -t2
    assert np.allclose(polar_angle_between(0, -45),  45)

    #t1,t2 = t2,t1
    assert np.allclose(polar_angle_between(4351,6773), polar_angle_between(6773, 4351))





def test_angle_between():
    '''
    testing the angle_between function
    '''
    q1 = np.array([1,0,0])
    q2 = np.array([0,1,0])
    q3 = np.array([0,0,1])

    assert angle_between(q1,q2) == np.radians(90)
    assert angle_between(q1,q3) == np.radians(90)

    q4 = np.array([5,-2,3])
    q4 = q4/np.linalg.norm(q4)
    q5 = np.array([-4,5,7])
    q5 = q5/np.linalg.norm(q5)

    np.testing.assert_allclose(angle_between(q4,q5), 1.72530713409797)
    assert angle_between(q4,q5) ==angle_between(q5,q4)




def test_index_x():
    '''
    testing the index_x function
    '''

    xmax=180
    nx =400
    lin = np.linspace(0, xmax, nx)

    dx = lin[1]-lin[0]

    #value of 0 should point to first index
    assert index_x(0, xmax, nx) ==0

    #value of xmax should point to last index
    #remember, if len(x) ==nx, than the last index is nx-1
    assert index_x(xmax, xmax, nx) ==nx-1


    assert index_x(xmax/2, xmax, nx) ==int((nx-1)/2)
    assert index_x(xmax/2+dx, xmax, nx) ==int((nx-1)/2)+1
    assert index_x(xmax/2-dx, xmax, nx) ==int((nx-1)/2)-1


    #only 25% of the distance between values, rounds down
    assert index_x(0.25*dx, xmax, nx) ==0

    #round down
    assert index_x(0.499999999999999*dx, xmax, nx) ==0
    #round up
    assert index_x(0.500000000000001*dx, xmax, nx) ==1


    #75% of the distance between values, rounds up to next value
    assert index_x(0.75*dx, xmax, nx) ==1

    #distance between values points to the second index
    assert index_x(dx, xmax, nx) ==1


    assert index_x(1.25*dx, xmax, nx) ==1
    assert index_x(1.499999999999999*dx, xmax, nx) ==1
    assert index_x(1.500000000000001*dx, xmax, nx) ==2
    assert index_x(1.75*dx, xmax, nx) ==2
    assert index_x(2*dx, xmax, nx) ==2


















