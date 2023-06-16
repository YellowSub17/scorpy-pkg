#!/bin/bash



for i in 2 4 8 16 32 64 128 256; do

    rm ~/corr/data/frames/*
    echo $i
    /usr/bin/time -f %E python generate-npz-patterns.py $i

done
