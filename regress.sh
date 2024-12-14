#!/bin/bash
MATCHES=$(grep $1 aoc*/*.py -l)
for m in $MATCHES
do
	OPTS=$(echo $m | sed -E "s/aoc_([0-9]{4})\/aoc_\1_([0-9]{2}).py/-y\1 -d\2/")
	./run.py $OPTS $2
done
