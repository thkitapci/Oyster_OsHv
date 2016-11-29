#PBS -l walltime=24:00:00
#PBS -l nodes=1:ppn=1
#PBS -l pmem=8000MB
#PBS -l vmem=8000MB
#PBS -l mem=8000MB
#PBS -q cegs

ref="/home/cmb-07/sn1/tkitapci/Oyster_Genome/Index_for_bwa/Crassostrea_gigas.GCA_000297895.1.27.dna.genome.fa"
#ref=$arg_ref
path_to_read1=$ARGV_path_to_read1

#output_directory="/staging/sn1/tkitapci/Barnacle/alignment/ref_with_contigs_bigger_than_1kb/"
#output_directory="/home/cmb-07/sn1/tkitapci/Barnacle/alignment_100bp_250bp"
output_directory="/staging/sn1/tkitapci/Oyster_OsHv/alignments_Run1_Run2_Merged"

echo $ref
echo $path_to_read1


read1=$(echo $path_to_read1 |awk 'BEGIN{FS="/"}{print $NF}')
sam_file_name=$(echo $path_to_read1 |awk 'BEGIN{FS="/"}{print $NF}'|awk 'BEGIN{FS="."}{print $1}')

ref_name=$(echo $ref |awk 'BEGIN{FS="/"}{print $NF}')

#mkdir $output_directory/ #create a dir
echo "Reference file used: $ref" >$output_directory/LOG.TXT

echo "read1 is:$read1"
echo "sam_file_name_is $sam_file_name"


#bwa index $ref #DON'T DO THIS HERE!! MAKE SURE THE INDEX FILE IS AVAILABLE!!!
#################################
#### bwa mem

bwa mem $ref $path_to_read1 >$output_directory/$sam_file_name.sam

################################################################################################
echo "Samfile is generated"

samtools view -bS $output_directory/$sam_file_name.sam -o $output_directory/$sam_file_name.bam  
samtools sort -o $output_directory/$sam_file_name-sorted.bam $output_directory/$sam_file_name.bam
samtools rmdup $output_directory/$sam_file_name-sorted.bam $output_directory/$sam_file_name-sorted-rmdupped.bam


#take only the mapped reads
#use this if the expected number of mapping is low so it is easier for downstream analysis
#samtools view -bS -F 4 $output_directory/$sam_file_name.sam -o $output_directory/$sam_file_name.mapped.bam 

##take only the unmapped reads
#samtools view -bS -f 4 $output_directory/$sam_file_name.sam -o $output_directory/$sam_file_name.unmapped.bam

samtools flagstat $output_directory/$sam_file_name-sorted.bam >$output_directory/$sam_file_name-sorted.bam.stats
samtools flagstat $output_directory/$sam_file_name-sorted-rmdupped.bam >$output_directory/$sam_file_name-sorted-rmdupped.bam.stats


#clean-up
rm $output_directory/$sam_file_name.sam
rm $output_directory/$sam_file_name.bam

echo "Sorted Bam file is generated"
