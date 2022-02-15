




import os
import scorpy


corr_total = scorpy.CorrelationVol(nq=100, npsi=180, cos_sample=False, inc_self_corr=False)
corr_total.save(f'{scorpy.DATADIR}/dbins/1vds-2d-total-qcor.dbin')


for file in os.listdir('/tmp/'):
    if '1vds' in file:
        os.remove(f'/tmp/{file}')




for i in range(10):
    os.system('python3 ./make-frames.py | bash')
    os.system('python3 ./2d-corr.py')

    for file in os.listdir('/tmp/'):
        if '1vds' in file:
            os.remove(f'/tmp/{file}')
    






