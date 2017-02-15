#PBS -l walltime=720:00:00
#PBS -l nodes=1:ppn=1
#PBS -l pmem=128000MB
#PBS -l vmem=128000MB
#PBS -l mem=128000MB
#PBS -q cmb


################################## -> start after aligning 
bam_file_path=$ARGV_FILE_PATH


output_directory="/home/cmb-07/sn1/tkitapci/Oyster_OsHV/GBS/raw_data/variant_call/variant_by_GATK"

echo $bam_file_path


ref="/home/cmb-07/sn1/tkitapci/Oyster_Genome/Index_for_samtools/Crassostrea_gigas.GCA_000297895.1.27.dna.genome.fa"






#################################################################################################################
#Call SNPs and indels simultaneously via local de-novo assembly of haplotypes in an active region
#################################################################################################################

java -Xmx16g -jar /home/cmb-panasas2/tkitapci/software/GATK/GenomeAnalysisTK.jar \
	-T HaplotypeCaller \
	-R $ref \
	-I /staging/sn1/tkitapci/Oyster_OsHv/alignments_Run1_Run2_Merged/Parent_12-sorted-rmdupped.bam \
	
	-stand_call_conf 50.0 \
	-stand_emit_conf 10.0 \
	-o $output_directory/Oyster_OsHv.raw.snps.indels.vcf

#knows snps can be added using --dbsnp dbSNP.vcf
# the -L argument directs the GATK engine restricts processing to specific genomic intervals (this is an Engine capability and is therefore available to all GATK walkers)

