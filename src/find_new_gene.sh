##Sort bowtie output file for cufflinks


##calculate FPKMs using sorted bowtie output
echo "cufflinks -p 3 -o ${BASE_NAME}_nc_cufflinks_out -G $HOME/Ecoli_RNAseq/reference_seqs/final_reference_seqs/REL606_nc_tss_no_dupl.gtf ${BASE_NAME}_bowtie_out_sorted.sam"
if [[ ! $TEST = "true" ]]; then 
   cufflinks -p 3 -o ${BASE_NAME}_nc_cufflinks_out -G $HOME/Ecoli_RNAseq/reference_seqs/final_reference_seqs/REL606_nc_tss_no_dupl.gtf ${BASE_NAME}_bowtie_out_sorted.sam
fi

##look for novel transcripts
#make novel reference GTF file from reads mapped
echo "cufflinks -p 3 -o ${BASE_NAME}_novel_trans_cufflinks_out ${BASE_NAME}_bowtie_out_sorted.sam"
if [[ ! $TEST = "true" ]]; then 
   cufflinks -p 3 -o ${BASE_NAME}_novel_trans_cufflinks_out ${BASE_NAME}_bowtie_out_sorted.sam          
fi

#compare novel reference GTF to the original GTF file
echo "cuffcompare -o ${BASE_NAME}_nc_cuffcompare_out -r $HOME/Ecoli_RNAseq/reference_seqs/final_reference_seqs/REL606_nc_tss_no_dupl.gtf ${BASE_NAME}_novel_trans_cufflinks_out/transcripts.gtf" 
if [[ ! $TEST = "true" ]]; then 
   cuffcompare -o ${BASE_NAME}_nc_cuffcompare_out -r $HOME/Ecoli_RNAseq/reference_seqs/final_reference_seqs/REL606_nc_tss_no_dupl.gtf ${BASE_NAME}_novel_trans_cufflinks_out/transcripts.gtf
fi

##sort .bam file
echo "samtools sort ${BASE_NAME}_bowtie_out_r1.bam ${BASE_NAME}_bowtie_out_r1_sorted"
if [[ ! $TEST = "true" ]]; then 
   samtools sort ${BASE_NAME}_bowtie_out_r1.bam ${BASE_NAME}_bowtie_out_r1_sorted
fi