#!/usr/bin/bash



DATA_PATH='/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data'

## Experiment Params
GEOM="${DATA_PATH}/geoms/agipd_2304_vj_opt_v3.geom"
BEAM_RADIUS="1e-6"
NUM_PHOTONS="1e12"
PHOTON_E="9300"
#PHOTON_E="19300"
BEAM_BANDWIDTH="0.01"
SPECTRUM_SHAPE="tophat"
NUM_SAMPLE_SPEC="5"


## Crystal Params
PDB="${DATA_PATH}/xtal/1al1.pdb"
NUM_CRYSTALS="32"
SIZE="100"


## Calc Params
GRAD='mosaic'
TAG="test/test"




if [ ${NUM_CRYSTALS} == "1" ]; then
    TAG="${TAG}.h5"
fi




    #--background=${BACKGROUND} \

pattern_sim \
    --gpu \
    --random-orientation \
    --really-random \
    --no-noise \
    --flat \
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
    --gradients=${GRAD} \
    -g ${GEOM} \
    -p ${PDB} \
    -o ${DATA_PATH}/${TAG} 





for f in $(ls ${DATA_PATH}/${TAG}*); do
    h5ls -d ${f}/entry_1/instrument_1/detector_1/data | grep -m 1 -q -e '\.'
    if  [ $? -eq 0 ]
    then
        echo "${f} has Intensity"
    else
        echo "${f} has no Intensity"
        rm ${f}
    fi
done



#python3 ./crystfel/h5totxt.py ${DATA_PATH}/test ${DATA_PATH}/out














