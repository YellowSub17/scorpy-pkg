#! /usr/bin/bash

DATA_PATH='/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data'

GEOM="${DATA_PATH}/geoms/agipd_2304_vj_opt_v3.geom"
PDB="${DATA_PATH}/xtal/fcc.pdb"
OUT="${DATA_PATH}/out.h5"


pattern_sim -r -g ${GEOM} -p ${PDB} -o ${OUT}
