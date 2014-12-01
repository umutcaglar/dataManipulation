#!/bin/bash

SRC_DIR=$HOME/Ecoli_RNAseq/src

all_read_files=($SCRATCH/data/glucose_time_course/sample*/RNA/*.raw/)
##look into processed directory 

rm -f $SCRATCH/data/paramlist_concatenate

for ((i=0;i<${#all_read_files[@]};i++)); do
	echo $i
	read_file=${all_read_files[$i]}    
	echo "python $SRC_DIR/concatenate_reads.py $read_file" >> $SCRATCH/data/paramlist_concatenate
done
