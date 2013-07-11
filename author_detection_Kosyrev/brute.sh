#!/bin/bash


for dsize in {1250..1400..10}
	do
		python generate_global_dict.py $dsize
		python classifier.py
		echo -n $dsize >> log.txt
		echo -n '           ' >> log.txt
		python tester.py >> log.txt
		echo $dsize
	done
