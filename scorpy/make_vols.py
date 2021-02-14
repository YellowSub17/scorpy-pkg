from xfelcorrel import *
# from blqq import * 
import os
import time







if __name__ == '__main__':
    np.random.seed(0)





# # # MAKE CORREL FROM RANDOM (UNIQUE) RUNS

    runs150 = [112,123,113,125,102,103,104,105]
    runs144 = [118,108,119,109,120,110,121]
    runs = runs150+runs144

    # runs = [108, 109, 110]
    qmax = 1.4 #water ring, max across all runs in old data is 1.409066
    nq=100 #this is "should" be set to match detector pixel width
    ntheta=180

    nseeds = 20
    peak_max=150

    geo = ExpGeom('data/agipd_2304_vj_opt_v3.geom')

    for run in runs:
        print(f'Run: {run}')
        #make directory to save in if it doesn't exist
        ls = os.listdir('data/dbins/cosine_sim')
        if str(run) not in ls:
            os.mkdir(f'data/dbins/cosine_sim/{run}')


        #peaks from the current run
        peaks = PeakData(f'data/cxi/{run}/peaks.txt', geo)

        #Split peaks by frame, crop frames with more than peak_max peaks
        all_frames = peaks.split_frames()
        cropped_frames = []
        for frame in all_frames:
            if frame.qlist.shape[0]<peak_max:
                cropped_frames.append(frame)



        print(f'Correlating {len(cropped_frames)} frames with less than {peak_max} peaks.')
        cropped_frame_cor = CorrelationVol(nq, ntheta, qmax)
        for frame in cropped_frames:
            cropped_frame_cor.correlate(frame.qlist[:, -3:])
        cropped_frame_cor.save_dbin(f'data/dbins/cosine_sim/{run}/qcor_all_peakmax{peak_max}')



        nframes_to_cor = int(len(cropped_frames)/2)
        print(f'Correlating {nframes_to_cor} frames in each half of the run {run}.')


        for i in range(nseeds):
            print(f'Seed: {i}')

            frames =  list(cropped_frames)

            np.random.shuffle(frames)
            cora = CorrelationVol(nq,ntheta, qmax)
            cora_num_peaks = 0

            for frame in frames[:nframes_to_cor]:
                cora_num_peaks += frame.qlist.shape[0]


                cora.correlate(frame.qlist[:, -3:])
            cora.save_dbin(f'data/dbins/cosine_sim/{run}/qcor_a_seed{i}')

            corb = CorrelationVol(nq,ntheta, qmax)
            corb_num_peaks = 0
            for frame in frames[nframes_to_cor:2*nframes_to_cor]:
                corb_num_peaks += frame.qlist.shape[0]
                corb.correlate(frame.qlist[:, -3:])
            corb.save_dbin(f'data/dbins/cosine_sim/{run}/qcor_b_seed{i}')
            print(f'Peaks in A: {cora_num_peaks}, Peaks in B: {corb_num_peaks}')






# # # MAKE CORREL FROM CIF
    # names= [ 'diamond','1al1','CuCN', '1vds', '5lf5', 'adamsite']
    # qmaxs = [ -1, -1, -1, 0.3, 0.1, -1]

    # for name, qmax in zip(names, qmaxs):

        # cif = CifData(f'data/xtal/{name}-sf.cif')
        # print(cif.qmax)

        # if qmax < 0:
            # correl = CorrelationVol(256,180, cif.qmax)
        # else:
            # correl = CorrelationVol(256,180, qmax)

        # correl.correlate(cif.scattering)

        # correl.save_dbin(f'data/dbins/{name}_qcor')

        # print('\n\n')




# # # MAKE BLQQ FROM CORREL + CIF
    # names = ['1al1', '1vds', '5lf5', 'CuCN', 'diamond', 'adamsite']

    # nl = 61

    # for name in names:

        # correl = CorrelationVol(fromfile=True, fname=f'data/dbins/{name}_qcor')
        # cif = CifData(f'data/xtal/{name}-sf.cif', qmax=correl.qmax)
        # iv = SphericalIntenVol(nq=correl.nq,nside=2**6, cifdata=cif)

        # print(f'{name} sph1')
        # sph1 = SphericalHandler(correl.nq, nl, correl.qmax)
        # sph1.calc_spherical_scattering(cif.spherical)
        # print(f'{name} bl1')
        # bl1 = BlqqVol(correl.nq, nl, correl.qmax)
        # bl1.fill_from_sph(sph1)
        # bl1.save_dbin(f'data/dbins/blqq/{name}_bl_Ilm')


        # print(f'{name} bl4')
        # bl4 = BlqqVol(correl.nq, nl, correl.qmax, comp=False)
        # bl4.fill_from_cvol(correl.cvol)
        # bl4.save_dbin(f'data/dbins/blqq/{name}_bl_pin')


