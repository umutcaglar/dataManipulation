import sys, re, os

def match_gene_name(inFile):
	ref_seq = open(inFile,"r")
	ref_seq_lst = ref_seq.readlines()
	
	tRNA_gene_name = {}
	for line in ref_seq_lst:
		m = re.match(r'.*gene\_name\s+\"(\w+)\";\s+oId\s+"(ECB\_t\d+)".*',line)
		if m:
			tRNA_gene_name[m.group(2)]=m.group(1)
			
	return(tRNA_gene_name)

def get_norm_tRNA(inFile,tRNA_gene_name):
	norm_counts = open(inFile,"r")
	norm_counts_lst = norm_counts.readlines()
	
	total_tRNA_reads = 0
	for line in norm_counts_lst:
		m = re.match(r'^ECB_t\d+\s+(\d+).*$',line)
		if m:
			total_tRNA_reads += int(m.group(1))
	
	tRNA_norm_counts = {}
	for line in norm_counts_lst:
		m = re.match(r'^(ECB_t\d+)\s+(\d+).*$',line)
		if m:
			aa_gene_name = tRNA_gene_name[m.group(1)]
			tRNA_norm_counts[aa_gene_name]=float(m.group(2))/total_tRNA_reads
	
	return(tRNA_norm_counts)
	
def main():
	ref_seq = sys.argv[1]
	raw_counts = sys.argv[2]
	tRNA_norm_counts_table = sys.argv[3]
	
	tRNA_gene_name = match_gene_name(ref_seq)
	tRNA_norm_counts = get_norm_tRNA(raw_counts,tRNA_gene_name)
	
	m = re.match(r'.*(MURI_\d+.*)_raw_rna_count\.txt',raw_counts)	
	if m:
		sample = m.group(1)
		
		m2 = re.match(r'^(MURI_\d+).*', sample)
		if m2:
			sample_name = m2.group(1)
	
	##glucose time course dictionary = {'sample_name': ['time', 'replicate'] }
	glucose_experiment = {'MURI_34': [3,1] , 'MURI_35': [4,1], 'MURI_36': [5,1], 'MURI_37': [6,1], 'MURI_38': [8,1], 'MURI_39': [24,1], 'MURI_40': [48,1], 'MURI_41': [168,1], 'MURI_42': [336,1] } 
	
	outFile = open(	tRNA_norm_counts_table, "w" )
	outFile.write('tRNA_norm_count\tgene_name\taa_name\ttime\tsample\treplicate\n')	
	
	if (sample_name in glucose_experiment):
		for tRNA_gene_name in tRNA_norm_counts:
			aa_name = tRNA_gene_name[:3]
			(time, replicate) = glucose_experiment[sample_name]
			row = '%f\t%s\t%s\t%i\t%s\t%i\n' %(tRNA_norm_counts[tRNA_gene_name], tRNA_gene_name, aa_name, time, sample_name, replicate )
			outFile.write(row)	

	return(0)
	
	
main()
