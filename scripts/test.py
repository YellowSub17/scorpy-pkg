



if __name__ == '__main__':



    from scorpy.vols import Vol
    from scorpy.vols import CorrelationVol
    from scorpy.readers import ExpGeom
    from scorpy.readers import PeakData
    from scorpy.readers import CifData



    import matplotlib.pyplot as plt


    DATA_DIR  = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/'


    cif1 = CifData(DATA_DIR+'xtal/1al1-sf.cif')

    qti = cif1.scattering[::100, :]

    c = CorrelationVol(100, 180, cif1.qmax)
    c.correlate(qti)

    c.plot_q1q2()
    plt.title('1al1 correl')

    plt.figure()




    e = ExpGeom(DATA_DIR+'agipd_2304_vj_opt_v3.geom')

    p = PeakData(DATA_DIR+'cxi/108/peaks.txt', e)
    frames = p.split_frames()

    p = frames[120]
    e.plot_panels()
    p.plot_peaks()
    plt.title('panels')

    c1 = CorrelationVol(100, 180, 1.4)
    c1.correlate(p.qlist[:,-3:])

    c1.plot_q1q2()
    plt.title('xfel correl')
    plt.show()
    





