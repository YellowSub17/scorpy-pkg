#!/bin/bash




printf '######\n'
printf 'Starting: y.sh\n'

echo $(date)>> ~/log.txt
echo starting y>> ~/log.txt





for flag in 0 1
do
    for maxexp in $(seq 0 7)
    do
        for exp in $(seq 0 $maxexp)
        do
            #date >> y.log
            #echo $flag $maxexp $exp >> y.log

            echo $(date)>> ~/log.txt
            echo ${flag} ${maxexp} ${exp} >> ~/log.txt

            echo $(date)
            echo ${flag} ${maxexp} ${exp}
            
            for size in 60 70 80 90 100 125 150 200 500
            do
                python /home/ec2-user/corr/scorpy-pkg/scripts/lysosim/sum-2d-qcor-nframes.py ${size}nm x1 $exp $maxexp $flag
                #echo y
            done
        done
    done
done

#sshpass -p uNix0987! ssh patricka@max-display3.desy.de -t echo doneyshxx1 | mail -s doneryshxx1 s3826109@student.rmit.edu.au


##date >> y.log
#echo $flag $maxexp $exp >> y.log
#for size in 60 70 80 90 100 125 150 200 500
#do
    #python sum-2d-qcor-nframes.py ${size}nm x1 7 7 0
#done

##sshpass -p uNix0987! ssh patricka@max-display3.desy.de -t echo doneysh770 | mail -s donerysh770 s3826109@student.rmit.edu.au


#date >> y.log
#echo $flag $maxexp $exp >> y.log
#for size in 60 70 80 90 100 125 150 200 500
#do
    #python sum-2d-qcor-nframes.py ${size}nm x1 7 7 1
#done

##sshpass -p uNix0987! ssh patricka@max-display3.desy.de -t 'echo doneysh771 | mail -s donerysh771 s3826109@student.rmit.edu.au'







