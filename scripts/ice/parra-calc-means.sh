#!/bin/bash






for i in '1000nm' '500nm' '250nm' '125nm';
do
    python calc-corr-means.py $i &
    sleep 10

done


