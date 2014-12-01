import sys,re

def match_gene_name(inFile):
	ref_seq = open(inFile,"r")
	ref_seq_lst = ref_seq.readlines()
	
	ref_gene_info = {}
	for line in ref_seq_lst:
		m = re.match(r'.*gene_id\s+\"(\w+)\";.*gene_name\s+\"(\w+)\s+oId\s+"(ECB\_t\d+)".*',line)
		if m:
			ref_gene_info[m.group(2)]=[m.group(1)
			
	return(tRNA_gene_name)
	
	
def main():
	ref_seq = sys.argv[1]
	