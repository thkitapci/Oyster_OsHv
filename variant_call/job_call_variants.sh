#PBS -l walltime=300:00:00
#PBS -l nodes=1:ppn=1
#PBS -l pmem=120000MB
#PBS -l vmem=120000MB
#PBS -l mem=120000MB
#PBS -q cegs


cd /home/cmb-07/sn1/tkitapci/Oyster_OsHV/GBS/raw_data/variant_call 

ref="/home/cmb-07/sn1/tkitapci/Oyster_Genome/Index_for_bwa/Crassostrea_gigas.GCA_000297895.1.27.dna.genome.fa"

bam_file_list="/home/cmb-07/sn1/tkitapci/Oyster_OsHV/GBS/raw_data/variant_call/bam_file_list.txt"

output_name="/staging/sn1/tkitapci/Oyster_OsHv/variant_call_results/OsHv_variant_call_Run_1"

samtools mpileup -f $ref -b $bam_file_list -o $output_name.vcf.gz --VCF
bcftools index $output_name.vcf.gz
bcftools call -o $output_name-SNPs.vcf -O "v" -v -c $output_name.vcf.gz
