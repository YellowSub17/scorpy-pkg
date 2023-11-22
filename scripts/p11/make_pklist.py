import scorpy
import numpy as np
import matplotlib.pyplot as plt
import regex
import sys




# run = int(sys.argv[1][:-1])
# print(run)


runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
for run in runs:


    print(f'Starting run:\t{run}')
    datapath = f'/home/ec2-user/corr/data/crystfel_calc'
    runpath = f'{datapath}/{run}/pk8_thr5_snr5'


    ##### crystfel.total.edit is crystfel.total with s/panel0//g
    crystfeltotal_file = open(f'{runpath}/crystfel.total.edit', 'r')
    cont = crystfeltotal_file.read()

    chunks = cont.split('\n----- Begin chunk -----\n')[1:]


    print(f'Number of chunks:\t{len(chunks)}')


    for i_chunk, chunk in enumerate(chunks):
        print(i_chunk, end='\r')

        num_peaks = int(regex.findall('(?<=num_peaks = )\d.*', chunk)[0])
        # if num_peaks > 1:


        peak_list = chunk.split('Peaks from peak search\n')[1].split('End of peak list\n')[0]

        peak_list = peak_list.split('\n')[1:-1]
        peak_list = ' '.join(peak_list)



        loc = np.fromstring(peak_list, sep=' ',  dtype=float).reshape((num_peaks, 4))





        np.save(f'{runpath}/pklists/pklist-{i_chunk}', loc)


