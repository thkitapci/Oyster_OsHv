import os
import sys

genome_size=637000000
genome_fraction=0.04

fastq_file=sys.argv[1]

f=open(fastq_file,"r")

#lines=f.readlines() #read the whole file into the memory


num_of_nucleotides=0

while True:
	seq_identifier=f.readline().rstrip("\n")
	raw_seq_letters=f.readline().rstrip("\n")
	plus_sign=f.readline().rstrip("\n")
	quality_scores=f.readline().rstrip("\n")
	if not quality_scores:
		break
	
	num_of_nucleotides+=len(raw_seq_letters)

coverage=num_of_nucleotides/(genome_size*genome_fraction)

f.close()

print "%s,%s" %(fastq_file,coverage)
