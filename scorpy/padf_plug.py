import os
import sys
from xfelcorrel import *
import imageio
import configparser as cfp


# HOME_DIR = '/Users/pat/'
HOME_DIR = '/home/pat/'

padfcorr_path = f'{HOME_DIR}Documents/cloudstor/phd/python_projects/padfcorr/'
padf_path = f'{HOME_DIR}Documents/cloudstor/phd/python_projects/padf/'



def save_im_to_dbin(path_in, path_out):
    '''
    open an RGB png file, save all B=255 positions as 1, and rest as 0
    save array to dbin

    '''
    #read image
    im = imageio.imread(f'{path_in}.png')
    #processing to mask
    im = np.array(im)
    im = im[...,0]

    if im.shape[0]!=im.shape[1]:
        print('WARNING: If saving image to dbin for padfcorr, image must be square')

    im[np.where(im==0)] = 1
    im[np.where(im !=1)] = 0
    #save as dbin
    flat_im = im.flatten().astype(np.float64)
    flat_im.tofile(f'{path_out}.dbin')












def run_corr(path_to_dbin, path_out, tag, nq, ntheta, qmax=-1, wavelength=1.3331611626494623e-10, res=5000, clen = 0.1697469375):
    '''
    open a dbin, run the qcorrel calculate
    dbin must be from single square array
    '''
    #write config file for padfcorr
    config = open(f'{padfcorr_path}config.txt', 'w')
    config.write(f'input = {path_to_dbin}.dbin\n')
    config.write(f'outpath = {path_out}\n')
    config.write(f'wavelength = {wavelength}\n')
    config.write(f'pixel_width = {1/res}\n')
    config.write(f'detector_z = {clen}\n')
    config.write(f'nq = {nq}\n')
    config.write(f'nth = {ntheta*2}\n') # padfcorr give theta from 0-360, so double ntheta so cut in half later 
    config.write(f'tag = {tag}\n')


    #if we give a qmax max, use it. else, use largest q on detector
    if qmax>0:
        config.write(f'qmax = {qmax*1e9}\n')
        # config.write(f'qmax = {qmax*1e10/(2*np.pi)**2}\n')
    config.close()

    #run the correlation
    os.system(f'{padfcorr_path}padfcorr {padfcorr_path}config.txt')

    #grab the qmax used inthe correlation (either maximum defualt or provided)
    f = open(f'{path_out}{tag}_log.txt', 'r')
    cont = f.read()
    f.close()
    cont = '[params]' + cont
    config = cfp.ConfigParser(interpolation=None, inline_comment_prefixes = (';'))
    config.read_string(cont)

    print(config['params'])
    print(float(config['params']['qmax']))
    #make a correlation volume object
    cor = CorrelationVol(nq, ntheta, float(config['params']['qmax'])*1e-9*2/np.pi) 
    # cor = CorrelationVol(nq, ntheta, float(config['params']['qmax'])*1e-10*4*np.pi**2) 
    
    #load in the dbin from the padfcorr
    cvol = np.fromfile(f'{path_out}{tag}_correlation.dbin').reshape((nq, nq, ntheta*2))

    #save the cvol to the correlation object
    cor.cvol = cvol[:, :, :ntheta]
    
    #save the correlation object
    cor.save_dbin(f'{path_out}{tag}')
    #delete junk
    os.system(f'rm {path_out}{tag}_correlation.dbin')
    os.system(f'rm {path_to_dbin}.dbin')








def run_padf(cor,rmax, res, nl, outpath, tag='tag'):


    nR = round(rmax/res) #A / (A/Pix) = Pix

    config_file = open(f'{padf_path}config.txt', 'w')

    config_file.write(f'correlationfile = {os.getcwd()}/{cor.fname}.dbin\n\n')
    config_file.write(f'outpath = {outpath}\n\n')
    config_file.write(f'wavelength = 1e-10\n\n')
    config_file.write(f'tag = {tag}\n\n')
    config_file.write(f'nthq = {cor.ntheta}\n\n')
    config_file.write(f'nq = {cor.nq}\n\n')
    config_file.write(f'nthr = {cor.ntheta}\n\n')
    config_file.write(f'nr = {nR}\n\n')
    config_file.write(f'nl = {nl}\n\n')
    config_file.write(f'qmax = {float(cor.qmax)/1e-10}\n\n')
    config_file.write(f'rmax = {rmax*1e-10}\n\n')


    config_file.close()

    cmd = f'{padf_path}padf {padf_path}config.txt'

    os.system(cmd)

    stream1 = os.popen(f'rm {outpath}/*r_vs_l*')
    stream2 = os.popen(f'rm {outpath}/*bl*')
    os.system(f'rm {outpath}/*r_vs_l*')
    os.system(f'rm {outpath}/*bl*')
    os.system(f'mv {outpath}/{cor.fname.split("/")[-1]}_padf_log.txt {outpath}/{cor.fname.split("/")[-1]}_AM_padf_log.txt') 
    os.system(f'mv {outpath}/{cor.fname.split("/")[-1]}_padf_padf.dbin {outpath}/{cor.fname.split("/")[-1]}_padf.dbin') 

    new_log = open(f'{outpath}/{cor.fname.split("/")[-1]}_padf_log.txt', 'w')
    new_log.write("## Correlation Log File\n\n")
    new_log.write("[params]\n")
    new_log.write(f"fname = {outpath}/{cor.fname.split('/')[-1]}_padf\n")
    new_log.write(f"qmax = {rmax}\n")
    new_log.write(f"nq = {nR}\n")
    new_log.write(f"ntheta = {cor.ntheta}\n")
    new_log.write("hflag = False\n")
    new_log.close()




if __name__ == '__main__':



#### MASK correlation

    geo = ExpGeom('data/agipd_2304_vj_opt_v3.geom')
    mask = MaskData('data/masks/radial_mask_iwr.h5', geo, mask_value=1)
    peaks = PeakData('data/cxi/108/peaks.txt', geo)


    npix = 500
    nq = 100
    ntheta = 180
    qmax=1.40
    im = np.zeros( (npix, npix) )
    xrange = (-0.055, 0.055)
    yrange = (-0.055, 0.055)

    xpix_lower = mask.qlist[:, 0] > xrange[0]
    xpix_higher = mask.qlist[:, 0] < xrange[1]
    xpix = xpix_lower & xpix_higher

    ypix_lower = mask.qlist[:, 1] > yrange[0]
    ypix_higher = mask.qlist[:, 1] < yrange[1]
    ypix = ypix_lower & ypix_higher

    pix = np.where(xpix & ypix)
    qlist = mask.qlist[pix[0]]

    for q in qlist:
        xind = index_x2(q[0],xrange[0], xrange[1], npix)
        yind = index_x2(q[1],yrange[0], yrange[1], npix)

        im[xind, yind] +=1
    im[np.where(im >= 1) ] = 1

    png_im = np.zeros((npix, npix, 3))
    png_im[np.where(im ==0)] = [255, 255, 255]
    imageio.imsave('data/masks/radial_mask_iwr.png', png_im.astype(np.uint8))

    save_im_to_dbin('data/masks/radial_mask_iwr', 'data/masks/radial_mask_iwr')

    mask_data_folder = f'{HOME_DIR}Documents/cloudstor/phd/python_projects/xfel_correl/data/masks/'

    print('bink')
    run_corr(f'{mask_data_folder}radial_mask_iwr', mask_data_folder, 'radial_mask_iwr_qcor_qmax',
             nq, ntheta,  wavelength=geo.wavelength, res= geo.res,
             clen=geo.clen, qmax=qmax)

#     print('bonk')
    # run_corr(f'{mask_data_folder}radial_mask_iwr', mask_data_folder, 'radial_mask_iwr_qcor_woqmax',
             # nq, ntheta,  wavelength=geo.wavelength, res= geo.res,
             # clen=geo.clen)


    c1 = CorrelationVol(fromfile=True, fname='data/masks/radial_mask_iwr_qcor_qmax')
    # c2 = CorrelationVol(fromfile=True, fname='data/masks/radial_mask_iwr_qcor_woqmax')
    c1.plot_q1q2()
    # c2.plot_q1q2()
    plt.show()







# ########### PADF with MASK
    # pass
    # runs = [108,109, 110]


    # for run in runs:
        # for seed in range(5):

            # print('\n\n\n')
            # print('#############')
            # print(f'{run} {seed}')
            # print('#############')
            # print('\n\n\n')

            # mask_cor = CorrelationVol(fromfile=True, fname='data/masks/radial_mask_iwr_qcor_qmax')
            # mask_cor.cvol = mask_cor.cvol[1:, 1:, :]
            # mask_cor.nq -= 1

            # cor = CorrelationVol(fromfile=True, fname=f'data/dbins/cosine_sim/{run}/qcor_a_seed{seed}')
            # cor.cvol = cor.cvol[1:, 1:, :]
            # cor.nq -=1

            # cor.cvol *= 1/mask_cor.cvol
            # cor.cvol[np.where(mask_cor.cvol <1e-1)] = 0

            # outpath = f'{HOME_DIR}Documents/cloudstor/phd/python_projects/xfel_correl/data/dbins/cosine_sim/{run}'
            # run_padf(cor, 30,0.25, 10, f'{outpath}', tag=f'seed{seed}_a')


            # cor = CorrelationVol(fromfile=True, fname=f'data/dbins/cosine_sim/{run}/qcor_b_seed{seed}')
            # cor.cvol = cor.cvol[1:, 1:, :]
            # cor.nq -=1

            # cor.cvol *= 1/mask_cor.cvol
            # cor.cvol[np.where(mask_cor.cvol <1e-1)] = 0

            # outpath = f'{HOME_DIR}Documents/cloudstor/phd/python_projects/xfel_correl/data/dbins/cosine_sim/{run}'
            # run_padf(cor, 30,0.25, 10, f'{outpath}', tag=f'seed{seed}_b')

















   ####### PADF CALC 

#     runs = [118, 110, 108]
    # numseeds = 20
    # for run in runs:
        # for seed in range(numseeds):
            # print('\n\n\n', f'{run} {seed}', '\n\n\n')

            # cor = CorrelationVol(fromfile=True, fname=f'data/dbins/cosine_sim/{run}/corra_seed{seed}')
            # outpath = f'/home/patrick/Documents/cloudstor/phd/python_projects/xfel_correl/data/dbins/cosine_sim/{run}'
            # run_padf(cor, 30,0.25, 30, f'{outpath}')

            # cor = CorrelationVol(fromfile=True, fname=f'data/dbins/cosine_sim/{run}/corrb_seed{seed}')
            # outpath = f'/home/patrick/Documents/cloudstor/phd/python_projects/xfel_correl/data/dbins/cosine_sim/{run}'
            # run_padf(cor, 30,0.25, 30, f'{outpath}')
