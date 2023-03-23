#!/bin/bash






for i in $(seq 45 160);
do
    if [ $(expr $i % 4) != 0 ];then
        python correlate-patterns.py $i &
    else
        python correlate-patterns.py $i
    fi

    sleep 2



done
echo "finished."

