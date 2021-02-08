from xfelcorrel import *
import json



runs150 = [112,123,113,125,102,103,104,105]#1.5 buffer
runs144 = [118,108,119,109,120,110,121] #1.44 buffer
runs = runs150+runs144

runs = [108,109,110]
geo = ExpGeom('data/agipd_2304_vj_opt_v3.geom')
stats = {}
max_q = 0
for run in runs:
    print(f'Run: {run}')

    stats[run] = {}

    peaks = PeakData(f'data/cxi/{run}/peaks.txt', geo)
    try:
        peaks = PeakData(f'data/cxi/{run}/{run}_indxd_rpf_peaks_Nint.txt', geo, rpf_flag=True)
    except:
        continue



    stats[run]['num_peaks'] = peaks.qlist.shape[0]
    stats[run]['intens'] = list(peaks.qlist[:,-1])


    frames = peaks.split_frames()
    stats[run]['num_frames'] = len(frames)

    frames_dict = {}
    for frame in frames:
        frames_dict[frame.frameNumbers[0]] = {}
        frames_dict[frame.frameNumbers[0]]['num_peaks'] = frame.qlist.shape[0]
        frames_dict[frame.frameNumbers[0]]['intens'] = list(frame.qlist[:,-1])


    stats[run]['frames'] = frames_dict

with open('data/cxi/run_statistics.json', 'w') as outfile:
    json.dump(stats, outfile)


















infile = open('data/cxi/run_statistics.json', 'r')
stats = json.load(infile)
infile.close()




# ### Plot histogram of Intensitys of peaks in a run 
# for run in ['110','118', '123', '113']:
    # intens_in_run = stats[run]['intens']
    # plt.figure()
    # plt.title(f'Run: {run}, Number of frames: {stats[run]["num_frames"]}, Number of Peaks: {len(stats[run]["intens"])}')
    # plt.hist(intens_in_run, bins=200, log=True)
    # plt.xlabel('Intensity in Run')
    # plt.ylabel('Occourrence')


runs150 = [123,113,125]# 1.5 buffer
runs144 = [118,108,109,110] #1.44 buffer
runs = runs150+runs144

runs = [108, 109, 110]

# ###plot the histogram of number of peaks in a frame for every run
for run in runs:
    peaks_in_frames = []
    max_peaks = 0
    for frame in stats[str(run)]['frames'].keys():
        # if stats[str(run)]['frames'][frame]['num_peaks'] <150:
            # peaks_in_frames.append(stats[str(run)]['frames'][frame]['num_peaks'])
        peaks_in_frames.append(stats[str(run)]['frames'][frame]['num_peaks'])
        if stats[str(run)]['frames'][frame]['num_peaks'] > max_peaks:
            max_peaks = stats[str(run)]['frames'][frame]['num_peaks']
    plt.figure()
    plt.title(f'Run: {run}, Number of frames: {stats[str(run)]["num_frames"]}, Number of Peaks: {len(stats[str(run)]["intens"])}')
    plt.hist(peaks_in_frames, bins=int(max_peaks/7))
    plt.xlabel('Number of Peaks in Frames')
    plt.ylabel('Occourrence')

for run in runs:
    peaks_in_frames = []
    frame_count=0
    peak_count = 0
    for frame in stats[str(run)]['frames'].keys():
        if stats[str(run)]['frames'][frame]['num_peaks'] <150:
            peaks_in_frames.append(stats[str(run)]['frames'][frame]['num_peaks'])
            frame_count +=1
            peak_count += stats[str(run)]['frames'][frame]['num_peaks']


        if stats[str(run)]['frames'][frame]['num_peaks'] > max_peaks:
            max_peaks = stats[str(run)]['frames'][frame]['num_peaks']
    plt.figure()
    plt.title(f'Run: {run}, Number of frames: {frame_count}, Number of Peaks: {peak_count}')
    plt.hist(peaks_in_frames, bins=int(max_peaks/7))
    plt.xlabel('Number of Peaks in Frames')
    plt.ylabel('Occourrence')

plt.show()





