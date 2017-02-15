#PBS -q cegs -l nodes=1:ppn=1,mem=128000mb,pmem=128000mb,vmem=128000mb,walltime=720:00:00

working_dir="/home/cmb-07/sn1/tkitapci/Oyster_OsHV/GBS/raw_data/variant_call/variant_by_discoSNP"

cd $working_dir


#### IT IS NOT WORKING AT THE MOMENT THERE IS NO OPTION TO GIVE BAM FILE AS INPUT!!!
/home/cmb-panasas2/tkitapci/software/DiscoSNP++-2.2.0-Source/run_discoSnp++.sh -r input_bam_files.txt -p /home/cmb-panasas2/tkitapci/Dugesia/variant_call_rmdupped_all/Dugesia_rmdupped_all
