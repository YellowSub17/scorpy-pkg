

import numpy as np
import scorpy


def test_main():
    sphv = scorpy.SphericalVol(5, 18, 36)

    blqq = scorpy.BlqqVol(5, sphv.nl)

    blqq.fill_from_sphv(sphv)
    assert True


if __name__ == '__main__':
    test_main()
