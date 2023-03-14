#!/bin/bash

printf '\n'

while [ 1 -ge 0 ]
do
    geom1=$(ls /media/pat/datadrive/ice/sim/patterns/agipdv2| wc -l)
    geom2=$(ls /media/pat/datadrive/ice/sim/patterns/19MPz12| wc -l)
    geom3=$(ls /media/pat/datadrive/ice/sim/patterns/19MPz18| wc -l)

    total=$(echo $geom1+$geom2+$geom3 | bc)

    printf '%s files                                     \r' $total
    sleep 1
#    if [ $total -le 20000 ]; then
        #sleep 1
    #else
        #play -q /usr/share/mint-artwork/sounds/notification.oga 2> /dev/null
        #sleep 10

    #fi



done



