# map_grch38_unplaced

mapping unplaced/unlocalized contigs in GRCh38# map_grch38_unplaced

## Work plan

```mermaid
flowchart LR
A[Parse sequence file to pull unplaced contigs] --> B[Align to T2T-CHM13]
B --> C[Parse alignments to get locations]
C --> D[Convert to cytogenetic coordinates]
D --> E[Create graphic and Data Table]
```

## Scripts/Workflow

Pull seq-ids for unmapped sequences

In scripts directory
```python parse_seq_report.py```

In main directory 

```seqtk subseq ../genome_data/GRCh38/GCF_000001405.40/GCF_000001405.40_GRCh38.p14_genomic.fna Unmap_seqids.txt > data/Unmap_primary.fa```

Align Unmap_primary.fa to T2T-CHM13 with minimap2
Note: some parameters suggested by Heng Li

Creating a PAF and a SAM just to look at different uses of output files.

```minimap2 -sm10 --MD ../genome_data/T2T-CHM13/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna data/Unmap_primary.fa -o results/GRCh38_unmap2T2T-CHM13.paf```

Note: you can add the --MD flag to the .paf output, but you don't get the flag (though maybe if you also output cigar into the paf)

```
[M::mm_idx_gen::30.101*1.32] collected minimizers
[M::mm_idx_gen::42.778*1.79] sorted minimizers
[M::main::42.778*1.79] loaded/built the index for 24 target sequence(s)
[M::mm_mapopt_update::43.488*1.77] mid_occ = 892
[M::mm_idx_stat] kmer size: 15; skip: 10; is_hpc: 0; #seq: 24
[M::mm_idx_stat::44.074*1.76] distinct minimizers: 100276788 (38.70% are singletons); average occurrences: 5.856; average spacing: 5.308; total length: 3117275501
[M::worker_pipeline::78.096*2.27] mapped 166 sequences
[M::main] Version: 2.24-r1122
[M::main] CMD: minimap2 -sm10 --MD -o results/GRCh38_unmap2T2T-CHM13.paf ../genome_data/T2T-CHM13/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna data/Unmap_primary.fa
[M::main] Real time: 78.403 sec; CPU: 177.309 sec; Peak RSS: 12.787 GB
```
```minimap2 -asm10 --MD ../genome_data/T2T-CHM13/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna data/Unmap_primary.fa -o results/GRCh38_unmap2T2T-CHM13.sam```

``` 
[M::mm_idx_gen::30.629*1.49] collected minimizers
[M::mm_idx_gen::43.785*1.90] sorted minimizers
[M::main::43.785*1.90] loaded/built the index for 24 target sequence(s)
[M::mm_mapopt_update::44.600*1.88] mid_occ = 892
[M::mm_idx_stat] kmer size: 15; skip: 10; is_hpc: 0; #seq: 24
[M::mm_idx_stat::45.187*1.87] distinct minimizers: 100276788 (38.70% are singletons); average occurrences: 5.856; average spacing: 5.308; total length: 3117275501
[M::worker_pipeline::80.625*2.35] mapped 166 sequences
[M::main] Version: 2.24-r1122
[M::main] CMD: minimap2 -asm10 --MD -o results/GRCh38_unmap2T2T-CHM13.sam ../genome_data/T2T-CHM13/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna data/Unmap_primary.fa
[M::main] Real time: 81.016 sec; CPU: 189.971 sec; Peak RSS: 14.379 GB
```

Add header to SAM and convert to BAM
```samtools view -b -T ../genome_data/T2T-CHM13/GCF_009914755.1/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna results/GRCh38_unmap2T2T-CHM13.sam >results/GRCh38_unmap2T2T-CHM13.bam```

Sort and index for viewing in IGV and BED file conversion

```samtools sort GRCh38_unmap2T2T-CHM13.bam -o GRCh38_unmap2T2T-CHM13_sorted.bam```
```samtools index GRCh38_unmap2T2T-CHM13_sorted.bam```

Convert to BED
```bedtools bamtobed -i GRCh38_unmap2T2T-CHM13_sorted.bam > GRCh38_unmap2T2T-CHM13_sorted.bed```

Note: BED file and PAF file have different number of lines

PAF: 583 lines
BED: 511 lines

Note: When processing file, I found a bug in the NCBI data files (downloaded using the datasets cli). The chrY sequence (NC_060948.1) which is imported from the NA24385 assembly is missing from the sequence_report.jsonl file, so I had to hard code this sequence-chromosome relationship in the notebook. 
