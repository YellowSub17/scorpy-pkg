#!/bin/bash




size=$1

npats=250
nchunks=80


printf "\n"
for geom in  19MPz12 agipdv2
do
    printf "Starting Geometry $geom:  $(date +'%l:%M')                                           \n\n"

    printf "    Starting Size: $size nm $(date +'%l:%M')                                           \n"
    
    for chunk in $(seq 0 1 $nchunks);
    do
        printf "Chunk $chunk/$nchunks: Generating $npats h5 patterns.                             \r"
        python ./gen-h5-patterns.py $chunk $npats $size $geom
        printf "Chunk $chunk/$nchunks: Converting $npats h5s to npz.                              \r"
        python ./h5_to_npz.py $chunk $npats $size $geom
        printf "Chunk $chunk/$nchunks: Removing $npats h5s.                                       \r"
        rm /media/pat/datadrive/ice/sim/patterns/$geom/*$size*$geom-$chunk*h5
    done

    printf "    Finished Size: $size nm $(date +'%l:%M')                                           \n\n"
    printf "Finished Geometry $geom:  $(date +'%l:%M')                                           \n\n\n"
done







#for i in $(seq 0 1 9);
#do
    #python ./gen-h5-patterns.py $i 1000 250 
    #python ./h5_to_npz.py $i 1000 250
    #rm /media/pat/datadrive/ice/sim/patterns/14MP/*h5
#done




#for i in $(seq 0 1 9);
#do
    #python ./gen-h5-patterns.py $i 1000 250 
    #python ./h5_to_npz.py $i 1000 250
    #rm /media/pat/datadrive/ice/sim/patterns/14MP/*h5
#done


