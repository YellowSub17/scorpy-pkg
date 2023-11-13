#!/bin/bash





#for flag in 1
#do
    #for maxexp in $(seq 0 6)
    #do
        #for exp in $(seq 0 $maxexp)
        #do
            #date >> y.log
            #echo $flag $maxexp $exp >> y.log
            #for size in 60 70 80 90 100 125 150 200 500
            #do
                #python sum-2d-qcor-nframes.py ${size}nm x1 $exp $maxexp $flag
            #done
        #done
    #done
#done

#sshpass -p uNix0987! ssh patricka@max-display3.desy.de -t echo doneyshxx1 | mail -s doneryshxx1 s3826109@student.rmit.edu.au


date >> y.log
echo $flag $maxexp $exp >> y.log
for size in 60 70 80 90 100 125 150 200 500
do
    python sum-2d-qcor-nframes.py ${size}nm x1 7 7 0
done

#sshpass -p uNix0987! ssh patricka@max-display3.desy.de -t echo doneysh770 | mail -s donerysh770 s3826109@student.rmit.edu.au


date >> y.log
echo $flag $maxexp $exp >> y.log
for size in 60 70 80 90 100 125 150 200 500
do
    python sum-2d-qcor-nframes.py ${size}nm x1 7 7 1
done

#sshpass -p uNix0987! ssh patricka@max-display3.desy.de -t 'echo doneysh771 | mail -s donerysh771 s3826109@student.rmit.edu.au'







