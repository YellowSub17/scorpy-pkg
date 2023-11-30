#!/bin/bash





printf '######\n'
printf 'Starting: x.sh\n'

echo $(date)>> ~/log.txt
echo starting x>> ~/log.txt



for superchunk in 0 1
do
    for chunk in $(seq 0 255)
    do
        echo $(date)>> ~/log.txt
        echo x${superchunk} ${chunk} >> ~/log.txt

        echo $(date)
        echo x${superchunk} ${chunk} 
        for size in 60 70 80 90 100 125 150 200 500
        do
            python /home/ec2-user/corr/scorpy-pkg/scripts/lysosim/generate-qcor-2d.py "${size}nm" "x${superchunk}" "$chunk"
        done
    done
done


printf '######\n'
printf 'Finished: '
date
printf '######\n'

#sshpass -p uNix0987! ssh patricka@max-display3.desy.de -t 'echo donexsh184to255 | mail -s donexsh184to255 s3826109@student.rmit.edu.au'
