#!/bin/bash

SRC_DIR=$HOME/Ecoli_RNAseq/src

all_raw_rna_files=($SCRATCH/data/glycerol_time_course/sample*/RNA/*.processed/*_raw_rna_count.txt)
all_work_dir=($SCRATCH/data/glycerol_time_course/sample*/RNA/*.processed/)
##look into processed directory 

rm -f $SCRATCH/data/paramlist_tRNA_count

for ((i=0;i<${#all_raw_rna_files[@]};i++)); do
	echo $i
	READS_1=`echo ${all_raw_rna_files[$i]} | grep -o "MURI_[0-9]\+_[a-zA-Z0-9_+]*_R1"`
	echo "READS_1: $READS_1"
	read_file=${all_raw_rna_files[$i]}  
	echo "cd ${all_work_dir[$i]}" >> $SCRATCH/data/paramlist_tRNA_count  
	echo "python $HOME/Ecoli_RNAseq/src/trna_fraction.py $HOME/Ecoli_RNAseq/reference_seqs/final_reference_seqs/REL606_nc_tss_no_dupl.gtf ${READS_1}_raw_rna_count.txt ${READS_1}_trna_norm_counts.txt" >> $SCRATCH/data/paramlist_tRNA_count
done

