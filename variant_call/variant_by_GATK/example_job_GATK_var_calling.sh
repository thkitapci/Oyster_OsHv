#PBS -l walltime=200:00:00
#PBS -l nodes=1:ppn=1
#PBS -l pmem=20000MB
#PBS -l vmem=20000MB
#PBS -l mem=20000MB
#PBS -q cmb


################################## -> start after aligning 
bam_file_path=$ARGV_FILE_PATH

#bam_file_path="/staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/LP_HT_ATCACG_L007.bam"
output_directory="/staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/"

echo $bam_file_path

#ref="/home/cmb-panasas2/tkitapci/Barnacle_Daniel/Barnacle_graph.scafSeq"
ref=/home/cmb-panasas2/tkitapci/Barnacle_Daniel/Barnacle_graph.scafSeq.fasta



bam_file_name=$(echo $bam_file_path |awk 'BEGIN{FS="/"}{print $NF}'|awk 'BEGIN{FS="."}{print $1}')

bam_file_dir=$(echo $bam_file_path |awk -v bam_file_name=$bam_file_name 'BEGIN{FS='bam_file_name'}{print $1}')
#bam_file_dir=$(echo $bam_file_path |awk 'BEGIN{FS="SMALL_SIZE_AATTCG_L001"}{print $1}')




#read1=$(echo $path_to_read1 |awk 'BEGIN{FS="/"}{print $NF}'|awk 'BEGIN{FS="."}{print $1}')
#read2=$(echo $path_to_read2 |awk 'BEGIN{FS="/"}{print $NF}'|awk 'BEGIN{FS="."}{print $1}')
#sam_file_name=$(echo $path_to_read1 |awk 'BEGIN{FS="/"}{print $NF}'|awk 'BEGIN{FS="_R[1-2]_"}{print $1}')
#################################################################################################################
#Call SNPs and indels simultaneously via local de-novo assembly of haplotypes in an active region
#################################################################################################################

java -Xmx16g -jar /home/cmb-panasas2/tkitapci/software/GATK/GenomeAnalysisTK.jar \
	-T HaplotypeCaller \
	-R $ref \
	-I /staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/LP_HT_ATCACG_L007-read_group_added_sorted_dupped_realigned.bam \
	-I /staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/LP_LT_CGATGT_L007-read_group_added_sorted_dupped_realigned.bam \
	-I /staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/PB_HT_ACAGTG_L007-read_group_added_sorted_dupped_realigned.bam \
	-I /staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/PB_HT_ACAGTG_L008-read_group_added_sorted_dupped_realigned.bam \
	-I /staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/PB_LT_GCCAAT_L007-read_group_added_sorted_dupped_realigned.bam \
	-I /staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/PB_LT_GCCAAT_L008-read_group_added_sorted_dupped_realigned.bam \
	-I /staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/SD_LT_TGACCA_L008-read_group_added_sorted_dupped_realigned.bam \
	-I /staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/SH_HT_CAGATC_L007-read_group_added_sorted_dupped_realigned.bam \
	-I /staging/sn1/tkitapci/Barnacle/alignment/bad_assembly/SH_LT_ACTTGA_L008-read_group_added_sorted_dupped_realigned.bam \
	-stand_call_conf 50.0 \
	-stand_emit_conf 10.0 \
	-o $output_directory/Barnacles.raw.snps.indels.vcf

#knows snps can be added using --dbsnp dbSNP.vcf
# the -L argument directs the GATK engine restricts processing to specific genomic intervals (this is an Engine capability and is therefore available to all GATK walkers)

