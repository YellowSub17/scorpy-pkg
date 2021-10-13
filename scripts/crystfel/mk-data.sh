#!/bin/bash
DATA_PATH='/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data'

## Experiment Params
GEOM="${DATA_PATH}/geoms/agipd_2304_vj_opt_v3.geom"
OUT="${DATA_PATH}/out.h5"
BEAM_RADIUS="1e-6"
NUM_PHOTONS="1e22"
PHOTON_E="9300"
BEAM_BANDWIDTH="0.1"
SPECTRUM_SHAPE="tophat"
NUM_SAMPLE_SPEC="19"


## Crystal Params
PDB="${DATA_PATH}/pdb/5wuc.pdb"
NUM_CRYSTALS="1"
SIZE="900"
#SIZE="1000"







pattern_sim \
    --gpu \
    --random-orientation \
    --really-random \
    --no-fringes \
    -n ${NUM_CRYSTALS} \
    --max-size=${SIZE} \
    --min-size=${SIZE} \
    --beam-radius=${BEAM_RADIUS} \
    --nphotons=${NUM_PHOTONS} \
    --beam-bandwidth=${BEAM_BANDWIDTH} \
    --photon-energy=${PHOTON_E} \
    --spectrum=${SPECTRUM_SHAPE} \
    --sample-spectrum ${NUM_SAMPLE_SPEC} \
    -g ${GEOM} \
    -p ${PDB} \
    -o ${DATA_PATH}/h5/out.h5
