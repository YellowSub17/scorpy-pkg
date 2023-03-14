#!/bin/bash


while [ 1 -ge 0 ]
do
    if [ $(ls /media/pat/datadrive/ice/sim/patterns/$1| wc -l) -le 75000 ]; then
        printf '%s\r' $(ls /media/pat/datadrive/ice/sim/patterns/$1 | wc -l)
        sleep 1
    else
        play /usr/share/mint-artwork/sounds/notification.oga
        sleep 20

    fi


done



