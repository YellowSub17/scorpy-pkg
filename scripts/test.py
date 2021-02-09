



if __name__ == '__main__':



    from scorpy.vols import Vol
    from scorpy.vols import CorrelationVol
    from scorpy.readers import ExpGeom
    from scorpy.readers import PeakData
    from scorpy.readers import CifData



    import matplotlib.pyplot as plt




    cif1 = CifData('../data/xtal/1al1-sf.cif')

    qti = cif1.scattering[::10, :]

    c = CorrelationVol(100, 180, cif1.qmax)
    c.correlate(qti)

    c.plot_q1q2()
    plt.show()





    # e = ExpGeom('../data/agipd_2304_vj_opt_v3.geom')

    # p = PeakData('../data/cxi/108/peaks.txt', e)
    # frames = p.split_frames()

    # p = frames[120]
    # e.plot_panels()
    # p.plot_peaks()

    # c = CorrelationVol(100, 180, 1.4)
    # c.correlate(p.qlist[:,-3:])

    # c.plot_q1q2()
    # plt.show()
    





