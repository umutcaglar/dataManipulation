import sys,re

def gene_length(file):
	ref_seq_gene_length = {}
	ref_seq = open(file,"r")
	
	ref_seq_lst = ref_seq.readlines()
	
	for line in ref_seq_lst:
		m = re.match(r'^REL606\s+\.\s+exon\s+(\d+)\s+(\d+).+oId\s+\"(ECB\_[\drt]\d+).+',line)
		if m:
			gene_start = m.group(1)
			gene_end = m.group(2)
			gene_id = m.group(3)
			gene_length = int(gene_end)-int(gene_start)+1
			ref_seq_gene_length[gene_id]=gene_length
		
	return(ref_seq_gene_length)	

def normalize_mRNA_counts(file, ref_seq_gene_length, outFile):
	raw_counts = open(file,"r")
	raw_counts_lst = raw_counts.readlines()
	
	##get all mRNA read count
	total_mRNA_reads = 0
	for line in raw_counts_lst:
		m = re.match(r'^ECB\_\d+\s+(\d+)$',line)
		if m:
			total_mRNA_reads += int(m.group(1))
			
	##normalize mRNA counts 
	for line in raw_counts_lst:
		m = re.match(r'^(ECB\_\d+)\s+(\d+)$',line)
		if m:
			gene_raw_count = int(m.group(2))
			
			##normalize by total mRNA value
			gene_norm_count = gene_raw_count/float(total_mRNA_reads)
			
			gene_id = m.group(1)
			if gene_id in ref_seq_gene_length:
				gene_length = int(ref_seq_gene_length.get(gene_id))
			
			##FPKM=(# of fragments)/(length of transcript/1000)/(total reads/10^6)
			fpkm = gene_raw_count/(float(gene_length)/1000)/(float(total_mRNA_reads)/1000000) 
			
			outFile.write("%s\t%i\t%i\t%f\t%f\n" %(gene_id,gene_length,gene_raw_count,gene_norm_count,fpkm))
				
	return()

def normalize_all_RNA_counts(file, ref_seq_gene_length, outFile):
	raw_counts = open(file,"r")
	raw_counts_lst = raw_counts.readlines()
	
	##get all mRNA read count
	total_mRNA_reads = 0
	for line in raw_counts_lst:
		m = re.match(r'^ECB\_\d+\s+(\d+)$',line)
		if m:
			total_mRNA_reads += int(m.group(1))
			
	##normalize mRNA counts 
	for line in raw_counts_lst:
		m = re.match(r'^(ECB\_\d+)\s+(\d+)$',line)
		if m:
			gene_raw_count = int(m.group(2))
			
			##normalize by total mRNA value
			gene_norm_count = gene_raw_count/float(total_mRNA_reads)
			
			gene_id = m.group(1)
			if gene_id in ref_seq_gene_length:
				gene_length = int(ref_seq_gene_length.get(gene_id))
			
			##FPKM=(# of fragments)/(length of transcript/1000)/(total reads/10^6)
			fpkm = gene_raw_count/(float(gene_length)/1000)/(float(total_mRNA_reads)/1000000) 
			
			outFile.write("%s\t%i\t%i\t%f\t%f\n" %(gene_id,gene_length,gene_raw_count,gene_norm_count,fpkm))
				
	return()
		
def main():
	ref_seq_gene_length = gene_length(sys.argv[1])
	
	m = re.match(r'^(MURI_\d+_SA\d+_[AGCT]+_L\d+)_\w+',sys.argv[2])	
	if m:
		sample = m.group(1)
		
	outFile = open(sample+"_normlized_mRNA_counts.txt","w")
	outFile.write("gene_id\tgene_length\tgene_raw_count\tgene_norm_count\tfpkm\n")
		
	normalize_mRNA_counts(sys.argv[2], ref_seq_gene_length, outFile)

main()