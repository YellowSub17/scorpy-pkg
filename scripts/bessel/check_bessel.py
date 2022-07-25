### recursive method: computes zeros ranges of Jn(r,n) from zeros of Jn(r,n-1)
### (also for zeros of (rJn(r,n))')
### pros : you are certain to find the right zeros values;
### cons : all zeros of the n-1 previous Jn have to be computed;
### note : Jn(r,0) = sin(r)/r

import numpy as np
from scipy import arange, pi, sqrt, zeros
from scipy.special import jv, jvp, yv
from scipy.optimize import brentq
from sys import argv
import os
import sys

def Jn(r,n):
    return (np.sqrt(pi/(2*r))*jv(n+0.5,r))

def Jn_zeros(n,nt):
    zerosj = np.zeros((n+1, nt), dtype=float)
    zerosj[0] = np.arange(1,nt+1)*pi
    points = np.arange(1,nt+n+1)*pi
    racines = np.zeros(nt+n, dtype=float)
    for i in range(1,n+1):
        for j in range(nt+n-i):
            foo, r = brentq(Jn, points[j], points[j+1], (i,), full_output=True)
            racines[j] = foo
        points = racines
        zerosj[i][:nt] = racines[:nt]
    return (zerosj)


def sphB_samp_nmax(lmax, rmax, qmax, nt=1000):

    qlim = 2 * np.pi * qmax * rmax
    out=0

    print(f'Calculating {nt} times...')
    for i in np.arange(nt):
        print(f'{i}', end='\r')

        jnuzeros = Jn_zeros(lmax, nt)

        qln = jnuzeros[lmax, i]
        if qln > qlim:
            out = i - 1
            break
    print()
    if out < 0:
        out = 0
    return out





if __name__ == "__main__":

    lmax = int(sys.argv[1])
    rmax = float(sys.argv[2])
    qmax = float(sys.argv[3])

    print(f'{lmax=} {rmax=} {qmax=}')

    x = sphB_samp_nmax(lmax, rmax, qmax)

    print(f'ANS: {x}')






