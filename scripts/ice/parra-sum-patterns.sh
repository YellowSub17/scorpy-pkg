#!/bin/bash






for size in 1000nm 500nm 250nm 125nm;
do

    for stdl in $(seq 0 0.25 3.75);
    do
        stdu=$( echo "$stdl+0.25" |bc )
        python sum-patterns.py $size $1 $stdl $stdu 

    done

    python sum-correlations.py $size $1 -999 0 

done

echo "finished."

