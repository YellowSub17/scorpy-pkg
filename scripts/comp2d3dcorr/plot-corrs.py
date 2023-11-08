import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.close('all')

plt.rc('font', size=8)



corr2d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/intenr/intenr-qmax0264-2d-qcor.dbin')
corr2d_qpsi = corr2d.copy()
corr2d_qpsi.qpsi_correction()
corr3d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/intenr/intenr-qmax0264-3d-qcor.dbin')

fig, axes = plt.subplots(1,2, sharey=True, figsize=(16/2.54, 8/2.54), dpi=300)
corr2d.plot_q1q2(xlabel='$\\Delta\\psi$ [rad]',  fig=fig, axes=axes[0])
corr3d.plot_q1q2(xlabel='$\\Delta\\psi$ [rad]', ylabel='$q_1=q_2$ [$\u212b^{-1}$]', fig=fig, axes=axes[1])

axes[0].text(0.05, 0.05, '$2D (corrected)$', transform=axes[0].transAxes, fontsize=12, color=(1,1,1),
verticalalignment='top')
axes[1].text(0.05, 0.05, '$3D$', transform=axes[1].transAxes, fontsize=12, color=(1,1,1),
verticalalignment='top')
fig.tight_layout()
fig.savefig('/home/pat/Documents/phd/figs/py/comp_2d3d_slice_bare.png')





corr2d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/intenr/intenr-qmax0264-2d-qcor.dbin')
corr2d_qpsi = corr2d.copy()
corr2d_qpsi.qpsi_correction()
corr3d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/intenr/intenr-qmax0264-3d-qcor.dbin')




fig, axes = plt.subplots(1,2, sharey=True, figsize=(16/2.54, 8/2.54), dpi=300)
corr2d_qpsi.plot_q1q2(xlabel='$\\Delta\\psi$ [rad]',  fig=fig, axes=axes[0])
corr3d.plot_q1q2(xlabel='$\\Delta\\psi$ [rad]', ylabel='$q_1=q_2$ [$\u212b^{-1}$]', fig=fig, axes=axes[1])

axes[0].text(0.05, 0.15, '$2D$', transform=axes[0].transAxes, fontsize=12, color=(1,1,1),
verticalalignment='top')
axes[1].text(0.05, 0.15, '$3D$', transform=axes[1].transAxes, fontsize=12, color=(1,1,1),
verticalalignment='top')
fig.tight_layout()
fig.savefig('/home/pat/Documents/phd/figs/py/comp_2d3d_integrated_w_alaising_slice.png')
















corr2d_inte_qpsi = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/intenr/intenr-qmax0264-2d-inte-qcor.dbin')
corr2d_inte_qpsi.qpsi_correction()

fig, axes = plt.subplots(1,1, sharey=True, figsize=(8/2.54, 8/2.54), dpi=300)
corr2d_inte_qpsi.plot_q1q2(xlabel='$\\Delta\\psi$ [rad]',  fig=fig, axes=axes, ylabel='$q_1=q_2$ [$\u212b^{-1}$]')
axes.text(0.05, 0.15, '$2D (corrected)$', transform=axes.transAxes, fontsize=12, color=(1,1,1),
verticalalignment='top')

fig.tight_layout()
fig.savefig('/home/pat/Documents/phd/figs/py/comp_2d3d_2dcorrect.png')


























corr2d_inte_qpsi = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/intenr/intenr-qmax0264-2d-inte-qcor.dbin')
corr2d_inte_qpsi.qpsi_correction()
corr3d_inte = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/intenr/intenr-qmax0264-3d-inte-qcor.dbin')
###### corr(psi)
fig, axes = plt.subplots(4,1, sharex=True, figsize=(16/2.54, 16/2.54), dpi=150)

# plt.subplots_adjust(hspace=0.4)


qqs = [96, -17, 76, 58]

for i, qq in enumerate(qqs):
    axes[i].plot(corr3d_inte.psipts, corr3d_inte.vol[qq, qq,:]/np.max(corr3d_inte.vol[qq,qq,:]), label='3D')
    # axes[i].plot(corr2d_inte.psipts, corr2d_inte.vol[qq, qq,:]/np.max(corr2d_inte.vol[qq,qq,:]), label='2D')
    axes[i].plot(corr2d_inte_qpsi.psipts, corr2d_inte_qpsi.vol[qq, qq,:]/np.max(corr2d_inte_qpsi.vol[qq,qq,:]), label='2D (corrected)')
    axes[i].set_title(f'q={np.round(corr2d_inte_qpsi.qpts[qq], 3)} [$\u212b^{{-1}}$]')
    axes[i].legend()

axes[-2].set_ylabel('Correlation Intensity [Normalized AU]')


axes[-1].set_xlabel('$\\psi$ [rad]')




fig.tight_layout()

fig.savefig('/home/pat/Documents/phd/figs/py/comp_2d3d_lines.png')
plt.show()









