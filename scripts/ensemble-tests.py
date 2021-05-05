
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
import scorpy
import datetime




n = 4
s= 0


# for n in [1,2,4,8,16,32,64, 128]:
# #     print('Starting: ', n)
    # # print(datetime.datetime.now())
    # # geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')
    # # pk = scorpy.PeakData(f'../data/ensemble_peaks/n{n}/peaks_{n}_{s}.txt', geo, cxi_flag=False)

    # # pk.crop_scat(Imax = 150)


    # # corr = scorpy.CorrelationVol(200,360,1.4)

    # # corr.fill_from_peakdata(pk)
    # # corr.save(f'../data/dbins/ensemble_peaks/ensemble_n{n}_{s}_qcor')
    # # print('Done')

    # corr = scorpy.CorrelationVol(path=f'../data/dbins/ensemble_peaks/ensemble_n{n}_{s}_qcor')

    # corr.plot_q1q2(log=True)
    # plt.title(f'Ensemble n{n}_{s}')


# plt.show()






# geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')

# pk1 = scorpy.PeakData('../data/cxi/118/peaks.txt', geo)
# corr1 = scorpy.CorrelationVol(200,360,1.4)
# corr1.fill_from_peakdata(pk1)

# print('bink')

# pk2 = scorpy.PeakData('../data/ensemble_peaks/n16/peaks_16_0.txt', geo, cxi_flag=False)
# corr2 = scorpy.CorrelationVol(200,360,1.4)
# corr2.fill_from_peakdata(pk2)




geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')
pk1 = scorpy.PeakData('../data/ensemble_peaks/homebrew-peaks.txt', geo, cxi_flag=False)


plt.figure()
pk1.plot_peaks()
geo.plot_panels()

corr1 = scorpy.CorrelationVol(20,36,1.4)
corr1.fill_from_peakdata(pk1)


corr1.plot_sumax(cmap='afmhot')



plt.show()











