#!/bin/bash


for dsize in {80..1480..100}
do
	echo 'Size: ' $dsize
	for msgLen in {40..440..100}
	do
		echo 'Len: ' $msgLen
		for fC in `seq 0.2 0.4 4.2`
		do	
			echo 'C: ' $fC
			python classifier.py $dsize $msgLen $fC >> log.txt
		done
	done	
done
