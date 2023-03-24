#!/bin/bash






#for i in $(seq 49 160);
#do
    #if [ $(expr $i % 6) != 0 ];then
        #python correlate-patterns.py $i &
    #else
        #python correlate-patterns.py $i
    #fi

    #sleep 10



#done
#echo "finished."

for i in $(seq 45 48);
do
    python correlate-patterns.py $i &

    sleep 10



done
echo "finished."


