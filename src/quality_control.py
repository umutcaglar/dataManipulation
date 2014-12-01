import sys, re 

def read_flexbar(file):	
	flexbar_file = open(file,"r")

	flexbar_file_lst = flexbar_file.readlines()

	for line in flexbar_file_lst:
		m = re.match( r'Discarded short reads:\s+(\d+)', line )
		if m:
			reads_discarded = int( m.group(1) )
			break # just record the first one

	for line in flexbar_file_lst:        
			m = re.match( r'Reads written to file:\s+(\d+)', line )
			if m:
					reads_trimmed = int( m.group(1) )
					break # just record the first one

	total_reads = reads_trimmed+reads_discarded
	percent_reads_remaining = reads_trimmed/float(total_reads)*100.0
	flexbar_file.close()

	return(total_reads, percent_reads_remaining, reads_trimmed)

def read_bowtie_both_reads(file,reads_trimmed):
	bowtie_file = open(file,"r")

	##get number of mapped and unmapped reads
	bowtie_file_lst = bowtie_file.readlines()

	for line in bowtie_file_lst:
		m = re.match( r'(\d+)\s+reads; of these:', line)
		if m: 
			print line
			print m.group(1)
			total_reads_for_mapping = int( m.group(1) )
			break 

	for line in bowtie_file_lst:
		m = re.match( r'^.+\((\d+\.\d+)\%\)\s+aligned concordantly exactly 1 time\s$', line)
		if m:
			percent_mapped_reads = float( m.group(1) )
			break

	if (reads_trimmed != total_reads_for_mapping):
		print("Warning: reads trimmed and written by flexbar does not equal the total number of reads processed by bowtie")

	reads_mapped = percent_mapped_reads/100*total_reads_for_mapping
	bowtie_file.close()

	return(reads_mapped, percent_mapped_reads)

def read_bowtie_one_read(file,reads_trimmed):
	bowtie_file = open(file,"r")

	##get number of mapped and unmapped reads
	bowtie_file_lst = bowtie_file.readlines()

	for line in bowtie_file_lst:
		m = re.match( r'(\d+)\s+reads; of these:', line)
		if m: 
			total_reads_for_mapping = int( m.group(1) )
			break 

	for line in bowtie_file_lst:
		m = re.match( r'^.+\((\d+\.\d+)\%\)\s+aligned exactly 1 time\s$', line)
		if m:
			percent_mapped_reads = float( m.group(1) )
			break

	#if (reads_trimmed != total_reads_for_mapping):
		#print("Warning: reads trimmed and written by flexbar does not equal the total number of reads processed by bowtie")

	reads_mapped = percent_mapped_reads/100*float(total_reads_for_mapping)
	bowtie_file.close()

	return(reads_mapped, percent_mapped_reads)

def count_bases(file):
	reads_file = open(file,"r")
	count_bases = 0
	i = 0
	
	
	for line in reads_file:	
		m = re.match( r'^([AGCTN]+)$', line.strip())
		if m: 
			count_bases += len(m.group(1))
			i += 1

	mean_read_length = float(count_bases)/i
	return(i,count_bases,mean_read_length)
	
def count_rna_type(file,reads_mapped):
	count_rna_file = open(file,"r")
	
	count_mRNA = 0
	count_tRNA = 0
	count_rRNA = 0

	for line in count_rna_file.readlines():
		m = re.match(r'ECB\_([\drt])\d+',line)
		if m:
			m2 = re.match(r'.*\s+(\d+)',line)
			if re.match(r'\d',m.group(1)):
				count_mRNA += int(m2.group(1))
			elif m.group(1) == "t":
				count_tRNA += int(m2.group(1))
			elif m.group(1) == "r": 
				count_rRNA += int(m2.group(1))
					
	percent_mRNA = count_mRNA/float(reads_mapped)*100
	percent_tRNA = count_tRNA/float(reads_mapped)*100
	percent_rRNA = count_rRNA/float(reads_mapped)*100				
	return (count_mRNA, percent_mRNA, percent_tRNA, percent_rRNA)	
	
def count_nc_rna(file,reads_mapped):
	count_rna_file = open(file,"r")
	
	count_ncRNA = 0
	
	for line in count_rna_file.readlines():
		m = re.match(r'RF.+\s+(\d+)',line)
		if m:
			count_ncRNA += int(m.group(1))
			
	percent_ncRNA = count_ncRNA/float(reads_mapped)*100
	return (percent_ncRNA)
		
def main():
	##python $HOME/Ecoli_RNAseq/scripts/quality_control.py ${BASE_NAME}_R1_001.fastq ${READS_1}_trimmed.fastq ${READS_1}_R2_bowtie.out ${READS_1}_bowtie.out ${READS_2}_bowtie.out ${READS_1}_raw_rna_count.txt
	##process flexbar output: 
	(total_reads_raw_fastq, base_count_raw, mean_raw_read_length) = count_bases(sys.argv[1])
	(total_reads_trimmed_fastq, base_count_trimmed, mean_trimmed_read_length) = count_bases(sys.argv[2])
	
	percent_reads_remaining = float(total_reads_trimmed_fastq)/total_reads_raw_fastq*100
	percent_base_remaining = float(base_count_trimmed)/base_count_raw*100
	
	print total_reads_trimmed_fastq
	
	(both_reads_mapped, percent_mapped_both_reads) = read_bowtie_both_reads(sys.argv[3],total_reads_trimmed_fastq)
	(read1_mapped, percent_mapped_read1) = read_bowtie_one_read(sys.argv[4],total_reads_trimmed_fastq)
	(read2_mapped, percent_mapped_read2) = read_bowtie_one_read(sys.argv[5],total_reads_trimmed_fastq)
	
	(count_mRNA, percent_mRNA, percent_tRNA, percent_rRNA) = count_rna_type(sys.argv[6],read1_mapped)	 
	(percent_ncRNA) = count_nc_rna(sys.argv[6], read1_mapped)
	##make output file

	m = re.match(r'^(MURI_\d+.*SA\d+_.*).fastq',sys.argv[1])	
	if m:
		sample = m.group(1)
	m2 = re.match(r'^(MURI_.*)SA\d+\w+', sample)
	if m2:
		sample_name = m2.group(1)
		
	outFile = open(sample+"_quality_control.txt","w")
		
	##write number of reads trimmed and discarded from flexbar
	outFile.write("sample\ttime\traw_read_count\traw_base_count\tmean_raw_read_length\ttrimmed_read_count\tpercent_reads_remaining\ttrimmed_base_count\tpercent_base_remaining\tmean_trimmed_read_length\tmapped_both_read_count\tpercent_trimmed_both_reads_mapped\tmapped_read_1_count\tpercent_read_1_mapped\tmapped_read_2_count\tpercent_read_2_mapped\tcount_read_1_mapping_mRNA\tpercent_read_1_mapping_mRNA\tpercent_read_1_mapping_tRNA\tpercent_read_1_mapping_to_rRNA\tpercent_read_1_mapping_to_ncRNA\n")
	row = "%s\ttime\t%i\t%i\t%i\t%i\t%.4g\t%i\t%.4g\t%i\t%i\t%.4g\t%i\t%.4g\t%i\t%.4g\t%i\t%.4g\t%.4g\t%.4g\t%.4g\n" % (sample_name, total_reads_raw_fastq, base_count_raw, mean_raw_read_length, total_reads_trimmed_fastq, percent_reads_remaining, base_count_trimmed, percent_base_remaining, mean_trimmed_read_length, both_reads_mapped, percent_mapped_both_reads, read1_mapped, percent_mapped_read1, read2_mapped, percent_mapped_read2, count_mRNA, percent_mRNA, percent_tRNA, percent_rRNA, percent_ncRNA )
	outFile.write(row)
	outFile.close()

main()

