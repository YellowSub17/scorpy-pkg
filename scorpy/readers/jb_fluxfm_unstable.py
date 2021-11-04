import h5py
import numpy as np
import os
import matplotlib.pyplot as plt
import hdf5plugin
import glob
import struct
import array
from skimage.transform import warp_polar
import re
import random
import scipy



def tag_grab(group_root):
    tag_list = []
    raw_tag_list = glob.glob(group_root+"/*/")
    [tag_list.append(rt.split("/")[-2]) for rt in raw_tag_list]
    return sorted(tag_list)


def sorted_nicely(ls):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(ls, key=alphanum_key)


class RedPro:

    def __init__(self,array,pix_num):
        self.array = array
        self.avg = np.array([])
        self.qar = np.zeros(pix_num)
        self.tthar = np.zeros(pix_num)
        self.sar = np.zeros(pix_num)
        self.data = array
        self.rfac = 0.0
        self.xmin = 50
        self.xmax = 500
        self.prominence = 0.01

    def peak_hunt(self):
        peaks, properties = scipy.signal.find_peaks(self.data, prominence=self.prominence)
        peaks_in_s = []
        print(peaks)
        for i, datap in enumerate(self.data):
            if i in peaks:
                peaks_in_s.append(self.qar[i])
        peaks_in_s = np.array(peaks_in_s)
        print(peaks_in_s)
        return peaks_in_s


    def norm_pattern(self,patt):
        ymax = np.max(patt)
        ymin = np.min(patt)
        baseline = patt - ymin
        norm_baseline = baseline / ymax
        return norm_baseline


    def calc_rfac(self):
        delta = 0.0
        sum_yobs = 0.0

        norm_avg = self.norm_pattern(self.avg[:,1])        
        norm_data = self.norm_pattern(self.data)
        for x in range(len(norm_data)):
            if self.xmin < x < self.xmax:
                ddelta = (norm_data[x] - norm_avg[x])**2
                delta += ddelta
                sum_yobs += norm_avg[x]**2
        rfac = np.sqrt(delta / sum_yobs)
        #if rfac > 0.4:
        #    plt.plot(norm_data[self.xmin:self.xmax])
        #    plt.plot(norm_avg[self.xmin:self.xmax])
        #    plt.show()
        return rfac

    def proc2s(self,pix_size,cam_length,wavelength):
        for i,pix in enumerate(self.sar):
            a = np.arctan((i * pix_size) / cam_length)
            s = (2  / wavelength) * np.sin( a / 2 )
            self.sar[i] = s
        joint_array = np.column_stack((self.sar,self.data))
        return joint_array
    
    def proc2q(self,pix_size,cam_length,wavelength):
        for i,pix in enumerate(self.sar):
            a = np.arctan((i * pix_size) / cam_length)
            q = ((4 * np.pi) / wavelength) * np.sin( a / 2 )
            s = (2  / wavelength) * np.sin( a / 2 )
            self.qar[i] = q * 1E-10
        joint_array = np.column_stack((self.qar,self.data))
        return joint_array

    def proc2tth(self,pix_size,cam_length,wavelength):
        for i,pix in enumerate(self.sar):
            a = np.arctan((i * pix_size) / cam_length)
            self.tthar[i] = np.degrees(a)
        joint_array = np.column_stack((self.tthar,self.data))
        return joint_array


class XfmHfiveDataset:

    def __init__(self):
        self.root = ''
        self.group = ''
        self.tag = ''
        self.dpath = ''
        self.apath = ''
        self.scratch = ''
        self.mfpath = ''
        self.nx = 1062
        self.ny = 1028
        self.image_center = (0,0)
        self.h5ls = []
        self.dsum = []
        self.mask = []
        self.bboxes = []
        self.circs = []
        self.pix_size = 1.0
        self.cam_length = 1.0
        self.wavelength = 1.0
        self.average_profile = []
        self.rfactor_array = []


    def grab_dset_members(self):
        print('<grab_dset_members> Grabbing .h5 list...',self.dpath)
        full = sorted(os.listdir(self.dpath))
        self.h5ls = full[:-1]
        #print('h5 list: ',self.h5ls)
        return self.h5ls  # remove the _master and _11 



    def mk_scratch(self,folder):
        """
        Checks if the run has a scratch folder and makes it if needed
        :return: updates self.scratch to new locale
        """
        scr_path = self.apath + folder + '/'
        if not os.path.exists(scr_path):
            os.makedirs(scr_path)
        print(f'scratch folder: {scr_path}')
        self.scratch = scr_path



    def write_dbin(self, path, data):
        """
        Write a .dbin file to the specified path. Slower than using npy files
        :param path: str to file location
        :param data: array to be written
        :return: nothing returned 
        """
        foal = open(path, "wb")
        fmt = '<' + 'd' * data.size
        bin_in = struct.pack(fmt, *data.flatten()[:])
        foal.write(bin_in)
        foal.close()


    def read_dbin(self, path, swapbyteorder=0):
        size = os.path.getsize(path)
        print(size)
        b = array.array('d')
        fail = open(path, 'rb')
        # print(fail)
        b.fromfile(fail, size // 8)
        fail.close()
        lst = b.tolist()
        output = np.array(lst).reshape(self.nx, self.ny)
        if swapbyteorder == 1:
            output  = output.newbyteorder()
        return output
        


    def gen_mask(self,image,max_lim,bboxes=False,circs=False,dump=False):
        print('<gen_mask> Generating mask...')
        self.mask = np.ones(image.shape)
        print(f'<gen_mask>{self.mask.shape}')
        #print(f'<gen_mask>{self.dsum.shape}') 
        for index, pix in np.ndenumerate(image):
            if pix > max_lim:
                nx = index[0]
                ny = index[1]
                self.mask[nx,ny] = 0
            else:
                continue
        if bboxes:
            print("<gen_mask> masking from bboxes")
            print(self.bboxes)
            print(f'<gen_mask>  image shape  {image.shape}')
            print(f'<gen_mask>  mask shape  {self.mask.shape}') 
            self.mask = np.transpose(self.mask)
            image = np.transpose(image)
            print(f'<gen_mask>  image shape  {image.shape}') 
            print(f'<gen_mask>  mask shape  {self.mask.shape}')
            for idx, pixel in np.ndenumerate(image):
                excluded_flag = False
                #print(idx)
                for exbox in self.bboxes:
                    if exbox[0] < idx[0] < exbox[1] and exbox[2] < idx[1] < exbox[3]:
                        excluded_flag = True
                        #print(excluded_flag)
                        continue
                if excluded_flag:
                    self.mask[idx[0],idx[1]] = 0
            self.mask = np.transpose(self.mask)
        if circs:
            print("<gen_mask> masking from circs")
            print(self.circs)
            self.mask = np.transpose(self.mask)
            for idx, pixel in np.ndenumerate(image):
                excluded_flag = False
                for crc in self.circs:
                    if (idx[0] - crc[0]) * (idx[0] - crc[0]) + (idx[1] - crc[1]) * (idx[1] - crc[1]) <= crc[2]**2:
                        excluded_flag = True
                        continue
                if excluded_flag:
                    self.mask[idx[0],idx[1]] = 0
            self.mask = np.transpose(self.mask)
        if dump:
            print('<gen_mask> Writing sum to:',self.scratch+self.tag + '_sum.npy')
            np.save(self.scratch+self.tag + '_mask.npy', self.mask)
            print('<gen_mask> Writing sum to:',self.scratch+self.tag + '_sum.dbin')
            self.write_dbin(self.scratch+self.tag + '_mask.dbin', self.mask)
        return self.mask
        


    
    def inspect_mask(self,image,cmin=0,cmax=1):
        print('<inspect_mask> inspecting mask...')
        inspection_frame = self.mask * image
        plt.imshow(inspection_frame)
        plt.clim(cmin,cmax)
        plt.show()

        
    def inspect_unwarp(self,image,cmin=0,cmax=1):
        print('<inspect_unwarp> unwarping...')
        plt.figure()
        inspec = warp_polar(np.transpose(image), center = self.image_center, radius = 1028)
        plt.imshow(inspec)
        plt.clim(cmin,cmax)
        plt.figure()
        profile = self.frm_integration(image)
        plt.plot(np.log10(profile))
        tth_rpro = RedPro(profile,1024)
        proc_arr = tth_rpro.proc2tth(self.pix_size,self.cam_length,self.wavelength)
        plt.figure()
        plt.plot(proc_arr[:,0],proc_arr[:,1])
        target = f'{self.apath}{self.tag}_sum_reduced_tth.txt'
        np.savetxt(target, proc_arr)
        q_rpro = RedPro(profile,1024)
        plt.figure()
        plt.title('s')
        q_arr = tth_rpro.proc2s(self.pix_size,self.cam_length,self.wavelength)
        plt.plot(q_arr[:,0],q_arr[:,1])
        plt.show()
        
        #pzero = 97.5
        #plt.axvline(x=pzero)
        #plt.axvline(x=pzero*np.sqrt(3))
        #plt.axvline(x=pzero*np.sqrt(4))
        #plt.show()


    def sum_h5s(self, limit=10, dump=False):
        """
        Sums all h5 files in a run
        :param limit: set to index at which sum will stop
        :return: numpy array containing sum of all data in run
        """
        # First check to see if the sum file has been generated before:
        prior_sum_file = self.scratch+self.tag + '_sum.npy'
        if os.path.isfile(prior_sum_file):
            print('<sum_h5s> sum file already exists...continue?')
            input('Press enter to continue...')
        print('<sum_h5s> Summing all frames...')
        sum_data = np.zeros((1062, 1028))   
        print("length h5 list:", len(self.h5ls))     
        for h5 in self.h5ls[:limit]:
            print('<sum_h5s> h5:', h5)
            print('<sum_h5s> Reading:', self.dpath+h5)
            with h5py.File(self.dpath+h5) as f:
                d = np.array(f['entry/data/data'])
                sum_data += np.sum(d, 0)
            # print(f'dsum.size = {sum_data.size}')
        if dump:
            print('<sum_h5s> Writing sum to:',self.scratch+self.tag + '_sum.npy')
            np.save(self.scratch+self.tag + '_sum.npy', sum_data)
            print('<sum_h5s> Writing sum to:',self.scratch+self.tag + '_sum.dbin')
            self.write_dbin(self.scratch+self.tag + '_sum.dbin', sum_data)
        self.dsum = sum_data
        return sum_data

    def sum_half_h5s(self, limit=10, dump=False, correlate_flag=False):
        """
        Sums each half of the h5 files in a run
        :param limit: set to index at which sum will stop
        :return: numpy array containing sum of all data in run
        """
        # First check to see if the sum file has been generated before:
        prior_sum_file = self.scratch+self.tag + '_sum.npy'
        prior_sum_evens_file = self.scratch+self.tag + '_sum_evens.npy'
        prior_sum_odds_file = self.scratch+self.tag + '_sum_evens.npy'
        if os.path.isfile(prior_sum_file) and os.path.isfile(prior_sum_odds_file) and os.path.isfile(prior_sum_evens_file):
            print('<sum_half_h5s> sum file already exists...continue?')
            input('Press enter to continue...')
        print('<sum_half_h5s> Summing all frames...')
        sum_data = np.zeros((1062, 1028))   
        sum_data_odds = np.zeros((1062, 1028))   
        sum_data_evens = np.zeros((1062, 1028))  
        
        data_qcor = np.zeros( (500, 360) )
        evens_qcor = np.zeros( (500, 360) )
        odds_qcor = np.zeros( (500, 360) ) 
        
        print("length h5 list:", len(self.h5ls))  
        nomask = True   
        for h5 in self.h5ls[:limit]:
            print('<sum_half_h5s> h5:', h5)
            print('<sum_half_h5s> Reading:', self.dpath+h5)
            with h5py.File(self.dpath+h5) as f:
                d = np.array(f['entry/data/data'])
                d_evens = d[0::2,:,:]
                d_odds = d[1::2,:,:]
                sum_data += np.sum(d, 0)
                sum_data_evens += np.sum(d_evens, 0)
                sum_data_odds += np.sum(d_odds, 0)
                
                if nomask:
                    self.mask = self.gen_mask(sum_data,bboxes=True,circs=True,max_lim = 1e11,dump=True)
                    nomask = False
                
                if correlate_flag:
                    
                    for i, shot in enumerate(d):
                        shot_unwrapped = self.to_polar(shot*self.mask, 500,720,0,500,0,360,  self.image_center[0], self.image_center[1])                        
                        shot_qcor = self.polar_angular_correlation(shot_unwrapped)
                        
                        data_qcor += shot_qcor
                        if i%2==0:
                            evens_qcor += shot_qcor
                        else:
                            odds_qcor += shot_qcor
                        

        if dump:
            
            np.save(self.scratch+self.tag + '_sum.npy', sum_data)
            self.write_dbin(self.scratch+self.tag + '_sum.dbin', sum_data)
            
            np.save(self.scratch+self.tag + '_sum_evens.npy', sum_data_evens)
            self.write_dbin(self.scratch+self.tag + '_sum_evens.dbin', sum_data_evens)

            np.save(self.scratch+self.tag + '_sum_odds.npy', sum_data_odds)
            self.write_dbin(self.scratch+self.tag + '_sum_odds.dbin', sum_data_odds)
            
            if correlate_flag:
               np.save(self.scratch+self.tag + '_sum_odds_qcor.npy', odds_qcor)
               self.write_dbin(self.scratch+self.tag + '_sum_odds_qcor.dbin', odds_qcor)
            
               np.save(self.scratch+self.tag + '_sum_evens_qcor.npy', evens_qcor)
               self.write_dbin(self.scratch+self.tag + '_sum_evens_qcor.dbin',evens_qcor)
            
               np.save(self.scratch+self.tag + '_sum_total_qcor.npy', data_qcor)
               self.write_dbin(self.scratch+self.tag + '_sum_total_qcor.dbin', data_qcor)
            

        self.dsum = sum_data
        return sum_data


    def atomize_h5(self,folder,limit=10,masked=False,normalize=False, norm_range=[0,10]):
        """
        Each h5 file in self.h5ls is separated out into 1000 dbin files in 
        self.tag/h5_frames/
        A manifest .txt file is written out for reading by p3padf
        :param limit: int setting the number of member .h5 files in the self.tag to expand
        :
        """
        atom_path = self.scratch+folder+'/'
        if not os.path.exists(atom_path):
            os.makedirs(atom_path)
        print(f'<atomize_h5> Atomizing to {atom_path}')
        with open(atom_path+self.tag+'_manifest.txt', 'w') as f:
            for k,h5 in enumerate(sorted_nicely(self.h5ls[:limit])):
                print(f'<atomize_h5> Atomizing {h5}...')
                with h5py.File(self.dpath+h5) as h:
                    d = np.array(h['entry/data/data'])
                    print(h['entry/data/data'])
                    for shot in range(d.shape[0]):
                        target = f'{atom_path}{self.tag}_{k}_{shot}.dbin'
                        if shot % 10 == 0:
                            print(f'<atomize_h5> {shot}/{d.shape[0]} frames generated')
                        if masked:
                            frame = d[shot,:,:] * self.mask
                        else:
                            frame = d[shot,:,:]
                        if normalize:
                            frame = self.normalize_frame(frame, norm_range)
                        self.write_dbin(target,frame)
                        f.write(f'{atom_path}{self.tag}_{k}_{shot}.dbin'+'\n')
        print('<atomize_h5> ...complete')
        print(f'<atomize_h5> File manifest written to {atom_path}{self.tag}_manifest.txt')



    def frm_integration(self, frame):
        """
        integrate and reduce to 1d plots
        """
        frame_polar = warp_polar(np.transpose(frame), center = self.image_center, radius = 1024)
        #plt.figure()
        #plt.imshow(frame_polar)
        #plt.show()
        integrated_frame_polar = np.sum(frame_polar, axis=0)
        return integrated_frame_polar


    def normalize_frame(self, img, norm_range):
        uw_img = self.frm_integration(img)
        # plt.plot(uw_img)
        norm_base = np.sum(uw_img[norm_range[0]:norm_range[1]])
        print(f'<normalize_frame> {norm_base}')
        norm_img = img / norm_base
        uw_norm = self.frm_integration(norm_img)
        # plt.plot(uw_norm)
        # plt.show()
        return norm_img



    def reduce_h5(self,folder='1d_profiles',limit=10,masked=False,scatter_mode='q',units='m'):
        """

        """
        reduction_path = f'{self.scratch}{folder}/'
        if not os.path.exists(reduction_path):
            os.makedirs(reduction_path)
        print(f'<reduce_h5> Reducing data to 1D profiles. Output to {reduction_path}')
        print(f'<reduce_h5> Reduction mode :{scatter_mode}')
        for k,h5 in enumerate(self.h5ls[:limit]):
            print(f'<reduce_h5> Reducing {h5}...')
            with h5py.File(self.dpath+h5) as h:
                d = np.array(h['entry/data/data'])
                for shot in range(d.shape[0]):
                    frame = d[shot,:,:] * self.mask
                    profile = self.frm_integration(frame)
                    rpro = RedPro(profile,1024)
                    if scatter_mode == 'q':
                        proc_arr = rpro.proc2q(self.pix_size,self.cam_length,self.wavelength)
                        target = f'{reduction_path}{self.tag}_{k}_{shot}_reduced_q_{units}.dat'
                        #print(proc_arr[100])
                        np.savetxt(target, proc_arr)
                    elif scatter_mode == 's':
                        proc_arr = rpro.proc2s(self.pix_size,self.cam_length,self.wavelength)
                        target = f'{reduction_path}{self.tag}_{k}_{shot}_reduced_s'
                        np.save(target, proc_arr)
                    elif scatter_mode == 'tth':
                        proc_arr = rpro.proc2tth(self.pix_size,self.cam_length,self.wavelength)
                        target = f'{reduction_path}{self.tag}_{k}_{shot}_reduced_tth'
                        np.save(target, proc_arr)
                        #plt.plot(proc_arr[:,0],proc_arr[:,1])
                        #plt.show()


    def reduce_dbin(self,folder='1d_profiles', dbin_folder='norm_h5_frames',masked=True,scatter_mode='q'):
        """

        """
        reduction_path = f'{self.scratch}{folder}/'
        ensemble_peak = []
        ensemble_base = []
        ensemble_pob = []
        if not os.path.exists(reduction_path):
            os.makedirs(reduction_path)
        print(f'<reduce_dbin> Reducing data to 1D profiles. Output to {reduction_path}')
        print(f'<reduce_dbin> Reduction mode :{scatter_mode}')
        dbin_ls = sorted_nicely(glob.glob(f'{self.apath}{dbin_folder}/*.dbin'))
        for k,db in enumerate(dbin_ls):
            d = self.read_dbin(db)
            frame = d * self.mask
            profile = self.frm_integration(frame)
            rpro = RedPro(profile,1028)
            if scatter_mode == 'q':
                proc_arr = rpro.proc2q(self.pix_size,self.cam_length,self.wavelength)
                target = f'{reduction_path}{self.tag}_{k}_reduced_q'
                np.save(target, profile)
                peak = np.sum(proc_arr[105:130,1])
                base = np.sum(proc_arr[400:425,1])
                print(f'{k} peak {peak} base {base}')
                ensemble_peak.append(peak)
                ensemble_base.append(base)
                ensemble_pob.append(peak/base)
                #plt.plot(proc_arr[:,1])
                #plt.show()
            elif scatter_mode == 's':
                proc_arr = rpro.proc2s(self.pix_size,self.cam_length,self.wavelength)
                target = f'{reduction_path}{self.tag}_{k}_reduced_s'
                np.save(target, profile)
        np.save(f'{reduction_path}{self.tag}_peak.npy', np.array(ensemble_peak))
        np.save(f'{reduction_path}{self.tag}_base.npy', np.array(ensemble_base))
        np.save(f'{reduction_path}{self.tag}_pob.npy', np.array(ensemble_pob))
        plt.plot(ensemble_peak[:])
        plt.plot(ensemble_base[:])
        plt.plot(ensemble_pob[:])
        plt.show()


    

    def tau_heatmap(self,limit=1000,folder='1d_profiles',intensity_range=[0,1e11]):
        prf_list = glob.glob(f'{self.apath}{folder}/*_reduced_q.npy')
        parent_mf = f'/data/xfm/16777/analysis/eiger/SAXS/{self.group}/{self.tag}/h5_frames/{self.tag}_manifest.txt'
        mf_path = f'/data/xfm/16777/analysis/eiger/SAXS/{self.group}/{self.tag}/h5_frames/{self.tag}_intensity_fltr_manifest.txt'
        prf_list = sorted_nicely(prf_list)
        print(prf_list[0])
        print(prf_list[-1])
        print(len(prf_list))
        ensemble_peak = []
        ensemble_base = []
        ensemble_pob = []
        measure = np.load(prf_list[0])
        print(measure.shape)
        tau_array = np.zeros((measure.shape[0],limit))
        print(tau_array.shape)
        for k, arr in enumerate(prf_list[:limit]):
            prf = np.load(prf_list[k])
            tau_array[:,k] = prf[:]
            peak = np.sum(prf[60:69])
            base = np.sum(prf[400:425])
            print(f'{k} peak {peak} base {base}')
            ensemble_peak.append(peak)
            ensemble_base.append(base)
            ensemble_pob.append(peak/base)
        plt.imshow(tau_array, aspect=5)
        plt.ylabel('pixel')
        plt.title(f'{self.tag}')
        plt.xlabel('frame number')
        plt.show()
        np.save(f'{self.apath}{self.tag}_heatmap.npy', tau_array)
        np.save(f'{self.apath}{self.tag}_peak.npy', np.array(ensemble_peak))
        np.save(f'{self.apath}{self.tag}_base.npy', np.array(ensemble_base))
        np.save(f'{self.apath}{self.tag}_pob.npy', np.array(ensemble_pob))
        #plt.plot(ensemble_peak[:])
        #plt.plot(ensemble_base[:])
        plt.plot(ensemble_pob[:])
        plt.show()
        frame_index = list(range(len(prf_list)))
        peak_sum = []
        sorted_heatmap = np.zeros((len(prf_list),1028))
        sorted_peak_map = [] 
        working_map = np.transpose(tau_array)
        for idx, profile in enumerate(working_map):
            #profile_sum = np.sum(profile)
            profile_peak = np.sum(profile[60:69])
            peak_sum.append(profile_peak)
        index_peak_sum_zip = np.column_stack((np.array(frame_index), np.array(peak_sum)))
        sorted_index_peak_sum_zip = index_peak_sum_zip[index_peak_sum_zip[:, 1].argsort()]
        for k, idx in enumerate(sorted_index_peak_sum_zip):
            sorted_heatmap[k, :] = working_map[int(idx[0]), :]
            sorted_peak_map.append(peak_sum[int(idx[0])])
        sorted_heatmap = np.transpose(sorted_heatmap)
        sorted_index = sorted_index_peak_sum_zip[:, 0]
        np.save(f'{self.apath}{self.tag}_sorted_peak_intensity.npy', np.array(sorted_peak_map))
        plt.imshow(sorted_heatmap)
        plt.show()
        plt.figure()
        plt.ylabel('Peak Intensity')
        plt.xlabel('Intensity rank')
        plt.plot(sorted_peak_map[:],'o')
        plt.show()
        ####
        plt.figure()
        plt.xlabel('Peak Intensity')
        plt.ylabel('Counts')
        peak_intensity_hist = np.histogram(sorted_peak_map, bins = 1000)
        plt.hist(sorted_peak_map, bins='auto')
        plt.show()
        ####
        print(sorted_index)
        filter_min = intensity_range[0]
        filter_max = intensity_range[1]
        filtered_indices = []
        print(f'FILTERS : {filter_min}    {filter_max}')
        count = 0
        for lbl, peak in enumerate(ensemble_peak):
            if filter_min < peak < filter_max:
                filtered_indices.append(lbl)
        print(f'there are {len(filtered_indices)} frames passed through teh filter')
        print(f'FILTERS : {filter_min}    {filter_max}')
        with open(parent_mf, 'r') as f:
            lines = f.readlines()
            with open(mf_path, 'w') as out:
                for index in filtered_indices:
                    int_ind = int(index)
                    out.write(lines[int_ind])
                    count += 1
        print(f'I wrote {count} files to the manifest {mf_path}')


    def scatter_shot_inspect(self,dbin_folder='h5_frames',sample_size=10,dump=False, show_each=False):
        dbin_ls = sorted_nicely(glob.glob(f'{self.apath}{dbin_folder}/*.dbin'))
        for count in range(sample_size):
            rand_indx = random.randint(0,len(dbin_ls))
            print(rand_indx) 
            try:
                print(f'<scatter_shot_inspect> frame: {dbin_ls[rand_indx]}')
            except IndexError:
                print('<scatter_shot_inspec> ERROR: cannot inspect random shots. did you forgot to atomize frames?')
                return None
            d = self.read_dbin(dbin_ls[rand_indx])
            frame = d * self.mask
            plt.figure()
            
            plt.imshow(frame)
            #plt.clim(0,100)
            plt.colorbar()
            np.savetxt(f'{self.apath}{self.tag}_sshot_{count}.txt',frame)
            plt.title(f'{dbin_ls[rand_indx]}')
            
            # plt.figure()
            # profile = self.frm_integration(frame)
            # plt.plot(profile)

            # plt.figure()
            # frame_polar = warp_polar(np.transpose(frame), center = self.image_center, radius = 1024)
            # print(frame_polar.shape)
            # plt.imshow(frame_polar)
            
            # plt.figure()
            # plt.plot(np.sum(frame_polar[:,117:128],axis=1))
            # plt.show()


    def define_average_profile(self,folder='1d_profiles',limit=10000):
        prf_list = glob.glob(f'{self.apath}{folder}/*_reduced_tth.npy')
        parent_mf = f'/data/xfm/16777/analysis/eiger/SAXS/{self.group}/{self.tag}/h5_frames/{self.tag}_manifest.txt'
        #mf_path = f'/data/xfm/16777/analysis/eiger/SAXS/{self.group}/{self.tag}/h5_frames/{self.tag}_intensity_fltr_manifest.txt'
        prf_list = sorted_nicely(prf_list)
        print(prf_list[0])
        print(prf_list[-1])
        prf_num = len(prf_list) 
        print(f"number of profiles: {prf_num}")
        if limit != 10000:
            limit = prf_num
        measure = np.load(prf_list[0])
        print(measure.shape)
        tau_array = np.zeros((measure.shape[0],limit))
        print(tau_array.shape)
        for k, arr in enumerate(prf_list[:limit]):
            prf = np.load(prf_list[k])
            tau_array[:,k] = prf[:,1]
        average_tau = np.average(tau_array, axis=1)
        print(average_tau.shape)
        self.average_profile = np.column_stack((prf[:,0],average_tau[:]))
        return self.average_profile


    def calc_rfactor(self,profile):
        delta = 0.0
        yobs = 0.0        
        for i, dp in enumerate(profile):
            delta = delta + (profile[i,1] - self.average_profile[i,1])**2
            yobs = yobs + (profile[i,1])**2
        r_p = np.sqrt(delta / yobs)
        #print(f'R_p : {r_p}')
        return r_p

    
    def define_parent_manifest(self, pmf_path):
        frm_list = []
        line_list = []
        if pmf_path == '':
            pmf_path = f'/data/xfm/16777/analysis/eiger/SAXS/{self.group}/{self.tag}/h5_frames/{self.tag}_manifest.txt'
        with open(pmf_path, 'r') as f:
            lines = f.readlines()
            print(f'Total of {len(lines)} frames in parent manifest')
            for line in lines:
                line_list.append(line)
                sploot = line.split('/')
                splat = sploot[-1].split('.')[0]
                print(splat)
                frm_list.append(splat)
        print(f'Parent manifest has {len(frm_list)} frames')
        return frm_list, line_list


    def grab_parent_prfs(self, frm_list, folder):
        prf_list = []
        for frm in frm_list:
            prf_list.append(f'{self.apath}{folder}/{frm}_reduced_tth.npy')
        return prf_list

    
    def calc_subset_average(self, prf_list):
        limit = len(prf_list)
        measure = np.load(prf_list[0])
        print(measure.shape)
        tau_array = np.zeros((measure.shape[0],limit))
        print(tau_array.shape)
        for k, arr in enumerate(prf_list[:limit]):
            prf = np.load(prf_list[k])
            tau_array[:,k] = prf[:,1]
        average_tau = np.average(tau_array, axis=1)
        print(average_tau.shape)
        subset_ap = np.column_stack((prf[:,0],average_tau[:]))
        return subset_ap
                   

    def calc_subset_rfactor(self,profile,average):
        delta = 0.0
        yobs = 0.0   
        # print(profile.shape)
        # print(average.shape)     
        for i, dp in enumerate(profile):
            delta = delta + (profile[i, 1] - average[i, 1])**2
            yobs = yobs + (profile[i,1 ])**2
        r_p = np.sqrt(delta / yobs)
        # print(f'R_p : {r_p}')
        return r_p

    
    def make_filtered_manifest(self, filtered_indices, frm_list, line_list, mf_path):
        count = 0
        with open(mf_path, 'w') as out:
            for index in filtered_indices:
                int_ind = int(index)
                out.write(line_list[int_ind])
                count += 1
        print(f'I wrote {count} files to the manifest {mf_path}')
        return line_list


    def filter_against_average(self,folder='1d_profiles',limit=10000,rfac_threshold=1.0, itera=0, parent_mf=''):
        frm_list, line_list = self.define_parent_manifest(parent_mf)
        prf_list = self.grab_parent_prfs(frm_list, folder)
        filtered_indices = []
        mf_path = f'/data/xfm/16777/analysis/eiger/SAXS/{self.group}/{self.tag}/h5_frames/{self.tag}_average_filter_manifest_{itera}.txt'
        prf_list = sorted_nicely(prf_list)
        print(prf_list[0])
        print(prf_list[-1])
        prf_num = len(prf_list)
        subset_ap = self.calc_subset_average(prf_list)
        for k, arr in enumerate(prf_list[:limit]):
            prf = np.load(prf_list[k])
            self.rfactor_array.append(self.calc_subset_rfactor(prf,subset_ap))
            #plt.plot(prf[:,0],prf[:,1])
            #plt.plot(subset_ap[:,0],subset_ap[:,1])
            #plt.show()
        plt.plot(self.rfactor_array[:])
        plt.show()
        plt.figure()
        plt.ylabel('Counts')
        plt.xlabel('R factor')
        plt.hist(self.rfactor_array, bins=20)
        plt.show()
        print(f'<filter_against_average> filtering with limit <= {rfac_threshold}')
        for k, rfac in enumerate(self.rfactor_array):
                if rfac <= rfac_threshold:
                   filtered_indices.append(k)
        print(f'<filter_against_average> a total of {len(filtered_indices)} profles < {rfac_threshold}')
        self.make_filtered_manifest(filtered_indices, frm_list, line_list, mf_path)

        
        




    def comp_dsets(self,tags=[]):
        plt.figure()
        for d in tags:
            d1 = np.loadtxt(f'/data/xfm/17635/analysis/eiger/SAXS/{self.group}/{d}/{d}_sum_msk_1d.txt')
            plt.plot(d1, label=d)
        plt.legend()
        plt.show()



    def to_polar(self, data, nr, nth, rmin, rmax, thmin, thmax, cenx, ceny):
        x = warp_polar( data, center=(cenx,ceny), radius=rmax)
        return np.rot90(x, k=3)


    def polar_angular_correlation(self, polar, polar2=None):
        fpolar = np.fft.fft( polar, axis=1 )

        if polar2 != None:
            fpolar2 = np.fft.fft( polar2, axis=1)
            out = np.fft.ifft( fpolar2.conjugate() * fpolar, axis=1 )
        else:
            out = np.fft.ifft( fpolar.conjugate() * fpolar, axis=1 )
        return np.real(out)



        
