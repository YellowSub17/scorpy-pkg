#!/bin/bash




datadir='/home/ec2-user/corr/data/crystfel_calc/11/pk8_thr5_snr5/'

echo 'copying crystfel.total'
cp ${datadir}/crystfel.total ${datadir}/pklist.total

echo 'deleting preamble lines'
sed -i '1, 79d' ${datadir}/pklist.total


sed -i '/^indexed_by/d' ${datadir}/pklist.total
sed -i '/^photon_energy/d' ${datadir}/pklist.total
sed -i '/^beam_diver/d' ${datadir}/pklist.total
sed -i '/^beam_band/d' ${datadir}/pklist.total
sed -i '/^average_camera/d' ${datadir}/pklist.total
sed -i '/^peak_resolution/d' ${datadir}/pklist.total
