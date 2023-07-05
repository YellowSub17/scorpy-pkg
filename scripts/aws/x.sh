#!/bin/bash





printf '######\n'
printf 'Starting: '
date
printf '######\n'



for superchunk in 0 1
do
    for chunk in $(seq 0 255)
    do

        for size in 60 70 80 90 125 150
        do
            python generate-qcor-2d.py "${size}nm" "x${superchunk}" "$chunk"
        done
    done
done


for chunk in $(seq 0 255)
do
    python generate-qcor-2d.py 100nm x2 "${chunk}"
    python generate-qcor-2d.py 100nm x3 "${chunk}"
done

printf '######\n'
printf 'Finished: '
date
printf '######\n'
