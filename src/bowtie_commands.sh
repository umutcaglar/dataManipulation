#!/bin/sh
## $1 = input directory *depleted.processed

##this script runs in sample*/RNA/*depleted.processed
TEST="false"
TEST="true"

READS_1=`echo ${1}*R1.fastq | grep -o "MURI_[0-9]\+_[a-zA-Z0-9_+]*_R1"`
READS_2=`echo ${1}*R2.fastq | grep -o "MURI_[0-9]\+_[a-zA-Z0-9_+]*_R2"`
SAMPLE_DIR=$1
LOGFILE="bowtie_commands.log"

cd $SAMPLE_DIR

echo "READS_1: ${READS_1}"  > ${LOGFILE}
echo "READS_2: ${READS_2}"	>> ${LOGFILE}
echo "SAMPLE_DIR: ${SAMPLE_DIR}"

##unzip processed reads if zipped
if [[ -a "${READS_1}*.fastq.gz" ]]; then
	gunzip ${READS_1}*.fastq.gz
	gunzip ${READS_2}*.fastq.gz
fi 

##trim adaptors on raw reads and moved trimmed reads to trimmed_reads
echo "flexbar -n 3 -t ${READS_1}_trimmed -r ${READS_1}.fastq -p ${READS_2}.fastq -f fastq -a $HOME/Ecoli_RNAseq/reference_seqs/adaptors.fna > ${READS_1}_R2_flexbar.out" >> ${LOGFILE}
if [[ ! $TEST = "true" ]]; then 
	flexbar -n 3 -t ${READS_1}_trimmed -r ${READS_1}.fastq -p ${READS_2}.fastq -f fastq -a $HOME/Ecoli_RNAseq/reference_seqs/adaptors.fna > ${READS_1}_R2_flexbar.out 2>> ${LOGFILE}
fi

if [[ -a "${READS_1}_trimmed_1.fastq" ]]; then
	mv ${READS_1}_trimmed_1.fastq ${READS_1}_trimmed.fastq 2>> ${LOGFILE}
	mv ${READS_1}_trimmed_2.fastq ${READS_2}_trimmed.fastq 2>> ${LOGFILE}
fi

##map trimmed reads to reference sequence in indexes file. 
##Index files were made with:
##bowtie2-build final_reference_seqs/REL606.fa indexes/REL606 
#align both reads together 2
echo "bowtie2 -k 1 -q -x $HOME/Ecoli_RNAseq/reference_seqs/indexes/REL606 -1 ${READS_1}_trimmed.fastq -2 ${READS_2}_trimmed.fastq -S ${READS_1}_R2_aligned.sam 2> ${READS_1}_R2_bowtie.out"  >> ${LOGFILE}
if [[ ! $TEST = "true" ]]; then 
   bowtie2 -k 1 -q -x $HOME/Ecoli_RNAseq/reference_seqs/indexes/REL606 -1 ${READS_1}_trimmed.fastq -2 ${READS_2}_trimmed.fastq -S ${READS_1}_R2_aligned.sam 2> ${READS_1}_R2_bowtie.out >> ${LOGFILE}
fi

#if [[ ! -a "${READS_1}_R2_aligned.sam.gz" ]]; then
#	gzip ${READS_1}_R2_aligned.sam
#fi

#align reads 1 separately
echo "bowtie2 -k 1 -q -x $HOME/Ecoli_RNAseq/reference_seqs/indexes/REL606 -U ${READS_1}_trimmed.fastq -S ${READS_1}_aligned.sam 2> ${READS_1}_bowtie.out"  >> ${LOGFILE}
if [[ ! $TEST = "true" ]]; then 
   bowtie2 -k 1 -q -x $HOME/Ecoli_RNAseq/reference_seqs/indexes/REL606 -U ${READS_1}_trimmed.fastq -S ${READS_1}_aligned.sam 2> ${READS_1}_bowtie.out >> ${LOGFILE}
fi

#if [[ ! -a "${READS_1}_aligned.sam.gz" ]]; then
#	gzip ${READS_1}_aligned.sam
#fi

#align reads 2 separately
echo "bowtie2 -k 1 -q -x $HOME/Ecoli_RNAseq/reference_seqs/indexes/REL606 -U ${READS_2}_trimmed.fastq -S ${READS_2}_aligned.sam 2> ${READS_2}_bowtie.out"  >> ${LOGFILE}
if [[ ! $TEST = "true" ]]; then 
   bowtie2 -k 1 -q -x $HOME/Ecoli_RNAseq/reference_seqs/indexes/REL606 -U ${READS_2}_trimmed.fastq -S ${READS_2}_aligned.sam 2> ${READS_2}_bowtie.out >> ${LOGFILE}
fi

#if [[ ! -a "${READS_2}_aligned.sam.gz" ]]; then
#	gzip ${READS_2}_aligned.sam
#fi

##convert bowtie output .sam to .bam
echo "samtools view -bS ${READS_1}_aligned.sam > ${READS_1}_aligned.bam" >> ${LOGFILE}
if [[ ! $TEST = "true" ]]; then 
   samtools view -bS ${READS_1}_aligned.sam > ${READS_1}_aligned.bam 2>> ${LOGFILE}
fi

##sort .bam file
echo "samtools sort ${READS_1}_aligned.bam ${READS_1}_aligned_sorted" >> ${LOGFILE}
if [[ ! $TEST = "true" ]]; then 
   samtools sort ${READS_1}_aligned.bam ${READS_1}_aligned_sorted 2>> ${LOGFILE}
fi

##convert back to sorted.sam
echo "samtools view -h -o ${READS_1}_aligned_sorted.sam ${READS_1}_aligned_sorted.bam" >> ${LOGFILE}
if [[ ! $TEST = "true" ]]; then 
   samtools view -h -o ${READS_1}_aligned_sorted.sam ${READS_1}_aligned_sorted.bam 2>> ${LOGFILE}
fi

TEST="false"
##get raw counts for reads mapped
echo "htseq-count -m union -t exon -i transcript_id ${READS_1}_aligned_sorted.sam $HOME/Ecoli_RNAseq/reference_seqs/edited_reference_seqs/REL606_nc.gtf  > ${READS_1}_raw_rna_count.txt" ##>> ${LOGFILE}
if [[ ! $TEST = "true" ]]; then
	htseq-count -m union -t exon -i transcript_id ${READS_1}_aligned_sorted.sam $HOME/Ecoli_RNAseq/reference_seqs/edited_reference_seqs/REL606_nc.gtf  > ${READS_1}_raw_rna_count.txt ##2>> ${LOGFILE}
fi
TEST="true"

##quality control 
echo "python $HOME/Ecoli_RNAseq/src/quality_control.py ${READS_1}.fastq ${READS_1}_trimmed.fastq ${READS_1}_R2_bowtie.out ${READS_1}_bowtie.out ${READS_2}_bowtie.out ${READS_1}_raw_rna_count.txt" 
if [[ ! $TEST = "true" ]]; then
	python $HOME/Ecoli_RNAseq/src/quality_control.py ${READS_1}.fastq ${READS_1}_trimmed.fastq ${READS_1}_R2_bowtie.out ${READS_1}_bowtie.out ${READS_2}_bowtie.out ${READS_1}_raw_rna_count.txt 
fi 

#python $HOME/Ecoli_RNAseq/scripts/trna_fraction.py $HOME/Ecoli_RNAseq/reference_seqs/final_reference_seqs/REL606_nc_tss_no_dupl.gtf ${READ_1}_raw_rna_count.txt glu_tRNA_norm_count.txt
##normalization 
#echo "python $HOME/Ecoli_RNAseq/scripts/calculate_norm_fpkm.py $HOME/Ecoli_RNAseq/reference_seqs/final_reference_seqs/REL606_nc_tss_no_dupl.gtf ${BASE_NAME}_htseq_count_r1.txt"
#if [[ ! $TEST = "true" ]]; then
#	python $HOME/Ecoli_RNAseq/scripts/calculate_norm_fpkm.py $HOME/Ecoli_RNAseq/reference_seqs/final_reference_seqs/REL606_nc_tss_no_dupl.gtf ${BASE_NAME}_htseq_count_r1.txt
#fi	

