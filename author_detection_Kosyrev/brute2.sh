#!/bin/bash


for msglen in {40..900..20}
do
			echo $dsize
			python classifier.py 340 $msglen 0.2 >> log.txt
done
