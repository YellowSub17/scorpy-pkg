#!/usr/bin/env python3
'''
time-to-correlate.py

Calculates the time to correlate a set of random vectors.
Also reads previous correlation times to determine approximation for future 
correlations.

'''
import numpy as np
import matplotlib.pyplot as plt
import timeit





## Write to CSV
# num_vectors = [25,50,100,150,300,600,1200,2400, 4800]
# num_calcs = [100,100,100,100,100,25,25,5,5]
# print('##number_of_vectors,n_times, average_correlation_time, std_correlation_time')
# for num_vec, num_calc in zip(num_vectors, num_calcs):
    # times = []
    # for i in range(num_calc):
        # setup = f'import numpy as np; import scorpy; vecs = np.random.randn({num_vec},4);cor=scorpy.CorrelationVol(100,180,1.8);'
        # t = timeit.timeit('cor.correlate(vecs)', setup=setup,number=1)
        # times.append(t)

    # print(f'{num_vec},{num_calc},{np.average(times)},{np.std(times)}')



# Get saved data
random_cor_data = np.genfromtxt('../data/random_correlation_times.csv', delimiter=',')
random_corr_x = random_cor_data[:,0]
random_corr_y = random_cor_data[:,2]/60
corr_data = np.genfromtxt('../data/correlation_times.csv', delimiter=',')
corr_x = corr_data[:,0]
corr_y = corr_data[:,2]/60


# Create fit
fit_x = np.linspace(0,np.max(random_corr_x), int(np.max(random_corr_x)))
fit_x_ex = np.linspace(0, np.max(corr_x), int(np.max(corr_x)))
fit_poly = np.polyfit(random_corr_x,random_corr_y, 4, full=True)
fit_y = np.polyval(fit_poly[0], fit_x)
fit_y_ex = np.polyval(fit_poly[0], fit_x_ex)


# Calculate R^2
SSE = fit_poly[1][0]
diff = random_corr_y- random_corr_y.mean()
square_diff = diff**2
SST = square_diff.sum()
R2 = 1- SSE/SST


# Plot correlation times
plt.figure()
plt.plot(fit_x, fit_y, color='orange', label='Fit')
plt.plot(fit_x_ex, fit_y_ex, '--', color='orange', label='Fit (extrapolated)')
plt.plot(random_corr_x,random_corr_y,'.', label='Random Vectors')
plt.plot(corr_x,corr_y,'rx', label='Real Correlation')


plt.legend()
plt.xlabel('Number of correlating vectors')
plt.ylabel('Time to correlate [min]')

plt.show()


testnum = 20200
minutes = np.polyval(fit_poly[0], testnum)
print(f'\nTo correlate {testnum} vectors,')
print(f'it will take approximately {np.round(minutes)} minutes.')

