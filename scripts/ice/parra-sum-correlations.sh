#!/bin/bash






for i in $(seq 1 160);
do
    if [ $(expr $i % 6) != 0 ];then
        python correlate-patterns.py $i &
    else
        python correlate-patterns.py $i
    fi

    sleep 10



done
echo "finished."

