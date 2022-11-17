import csv
import pandas as pd

if __name__ == '__main__':

    #for now, hard code path to file you want. Could take this as an argument later if we need to generalize
    #note: used the dataformats tool to convert the jsonl format to a tsv.
    #last note: this file is incomplete- it only contains information for the primary assembly, which is fine for this exercise, but not others
    seq_report="/Users/deannachurch/Documents/projects/genome_data/GRCh38/GCF_000001405.40/sequence_report.tsv"
    unmap_seq="../Unmap_seqids.txt"

    assm_df=pd.read_csv(seq_report, sep="\t", header=0)
    unmap_df=assm_df.loc[assm_df['Role'] != 'assembled-molecule']
    unmap_df[['RefSeq seq accession']].to_csv(unmap_seq, index=False, header=False)
   


