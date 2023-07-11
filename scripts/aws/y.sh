#!/bin/bash


superchunk=0

for flag in 0 1
do
    for exp in $(seq 0 7)
    do
        for size in 60 70 80 90 100 125 150 200 500
        do
            python sum-2d-qcor-nframes.py "${size}nm" "x${superchunk}" $exp $flag
        done
    done
done

