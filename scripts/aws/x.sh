#!/bin/bash





printf '######\n'
printf 'Starting: '
date
printf '######\n'


for superchunk in 0
do
    for chunk in $(seq 184 255)
    do
        for size in 60 70 80 90 100 125 150 200 500
        do
            python generate-qcor-2d.py "${size}nm" "x${superchunk}" "$chunk"
        done
    done
done


printf '######\n'
printf 'Finished: '
date
printf '######\n'

sshpass -p uNix0987! ssh patricka@max-display3.desy.de -t 'echo donexsh184to255 | mail -s donexsh184to255 s3826109@student.rmit.edu.au'
