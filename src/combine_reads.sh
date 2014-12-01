#!/bin/bash



for samp in `ls | grep -o "MURI_[0-9]\{2,3\}_[A-Z]\{6\}" | sort | uniq`
do
	echo $samp
	cat `echo ${samp}*R1*` > ${samp}_R1.fastq
	cat `echo ${samp}*R2*` > ${samp}_R2.fastq
done
