Ecoli_RNAseq
============

* reference_seqs

	all sequence files that have been generated in the process or needed for the pipeline

* adaptors.fna
	
	Contains all adaptor sequences used for trimming by flexbar
	
* final_reference_seqs
	
	Contains final sequence files used to run the analysis. Most of the sequence in this directory have been 			modified from original versions
	
	Contains all generated reference sequences.
	
	* REL606.fa/.fai - original untampered fasta files with Ecoli DNA sequence
	* REL606_nc_tss_no_dupl.gtf - modified REL606.gtf file that contains non-coding RNAs and formatted tss column. There are also no duplicate entries present in this file (unlike REL606.gtf)
	* REL606_nc_tss_no_dupl_rRNAtRNA.gtf - REL606_nc_tss_no_dupl.gtf file with only tRNAs and rRNAs (needed by cuffdiff to weed out tRNAs and rRNAs)

* edited_reference_seqs
	
	Contains original and modified reference sequences made in the process for different functions.
	
* indexes
	
	Contains index files generated from REL606.fa and used by bowtie2. It also contains original untampered REL606.fa. Bowtie2 requires a fasta file within this folder for proper functioning

* job_submissions_files

	files used to submit a job on TACC
		
	* cuffdiff_launcher.sge - launcher file used to submit a job on TACC to carry out paramlist_cuffdiff
	
	* bowtie_launcher.sge - launcher file used to submit a job on TACC to carry out bowtie_commands.sh

* scripts

	all script files used to run the pipeline

	* write_paramlist_bowtie.sh - writes paramlist_bowtie by finding all the MURI_*_R1_*.fastq within the directory and creating MURI_*_R1_*.fastq for given R1 file. paramlist_bowtie file with bowtie_commands.sh to be ran on reads1 and reads2. bowtie_launcher.sge executes paramlist_bowtie 

	* bowtie_commands.sh - contains functions that carry out the analysis for reads1 and reads2 for a sample

	* paramlist_cuffdiff - runs cuffdiff on given samples. 

	* combine_reads.sh - combines all R1 and R2 fastq files in one R1 and R2 files
		
	* calculate_norm_fpkm.py - takes in htseq output and reference gtf file to write out a file with columns for gene id, gene length, raw counts for each gene, normalized counts, and fpkm. 
	
	* quality_control.py - calculates counts and percentages of reads mapping to genome for both reads, reads 1 and reads 2 separately; and calculates counts and percentages of mapped reads to mRNAS, tRNAs, rRNAs, and ncRNAs for reads 1.
		 
