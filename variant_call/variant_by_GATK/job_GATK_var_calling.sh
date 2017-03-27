#PBS -l walltime=200:00:00
#PBS -l nodes=1:ppn=1
#PBS -l pmem=128000MB
#PBS -l vmem=128000MB
#PBS -l mem=128000MB
#PBS -q cegs


################################## -> start after aligning and pre-processing


output_directory="/home/cmb-07/sn1/tkitapci/Oyster_OsHV/GBS/raw_data/variant_call/variant_by_GATK"



ref="/home/cmb-07/sn1/tkitapci/Oyster_Genome/Index_for_samtools/Crassostrea_gigas.GCA_000297895.1.27.dna.genome.fa"
###
#Make sure .dict is generated

#java -Xmx4g -jar /home/cmb-panasas2/tkitapci/software/picard/picard-tools-1.110/CreateSequenceDictionary.jar R=Crassostrea_gigas.GCA_000297895.1.27.dna.genome.fa O=Crassostrea_gigas.GCA_000297895.1.27.dna.genome.dict
#Make sure .fai is generated
#samtools faidx /home/cmb-07/sn1/tkitapci/Oyster_Genome/Index_for_samtools/Crassostrea_gigas.GCA_000297895.1.27.dna.genome.fa




#################################################################################################################
#Call SNPs and indels simultaneously via local de-novo assembly of haplotypes in an active region
#################################################################################################################


java -Xmx90g -jar /home/cmb-panasas2/tkitapci/software/GATK/GenomeAnalysisTK.jar \
	-T HaplotypeCaller \
	-R $ref \
	-I /home/cmb-07/sn1/tkitapci/Oyster_OsHV/GBS/raw_data/variant_call/variant_by_GATK/all_bam_files_read_group_added_exclude_not_used_wells.list \
	-stand_call_conf 50.0 \
	-stand_emit_conf 10.0 \
	-o $output_directory/Oyster_OsHv.raw.snps.indels.vcf



#knows snps can be added using --dbsnp dbSNP.vcf
# the -L argument directs the GATK engine restricts processing to specific genomic intervals (this is an Engine capability and is therefore available to all GATK walkers)

