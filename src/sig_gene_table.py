##This script converts regular sig_gene_table output with XLOC names to a more conventional naming scheme. 
import sys,re, os

def make_ref_seq_dic(inFile):
	ref_seq = open(inFile,"r")
	ref_seq_lst = ref_seq.readlines()
	
	ref_seq_name_dic = {}
	for line in ref_seq_lst:
		m = re.match(r'.*gene_id\s+\"(XLOC_\w+)\";(.*);\s+class_code',line)
		if m:
			ref_seq_name_dic[m.group(1)] = m.group(2)
				
	return(ref_seq_name_dic)

def make_new_sig_gene_table(inFile, ref_seq_name_dic, new_sig_gene_table):
	sig_gene_table = open(inFile,"r")
	sig_gene_table_lst = sig_gene_table.readlines()
				
	for line in sig_gene_table_lst:
		m = re.match(r'(XLOC_\d+)\s+.*', line)
		if (m and m.group(1) in ref_seq_name_dic): 
			new_sig_gene_table.write(line.replace(m.group(1),(m.group(1)+";"+ref_seq_name_dic[m.group(1)]))) 
		
def main():
	ref_seq = sys.argv[1]
	sig_mRNA = sys.argv[2]
	new_sig_gene_data_file = sys.argv[3]
	
	new_sig_gene_table = open(new_sig_gene_data_file,"w")
	new_sig_gene_table.write("gene_id\tsample_1\tsample_2\tstatus\tvalue_1\tvalue_2\tlog2_fold_change\ttest_stat\tp_value\tq_value\tsignificant\n")

	ref_seq_name_dic = make_ref_seq_dic(ref_seq)
	new_sig_gene_table = make_new_sig_gene_table(sig_mRNA, ref_seq_name_dic, new_sig_gene_table)
		
main()