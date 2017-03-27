import numpy as np



#PBS -l walltime=720:00:00
#PBS -l nodes=1:ppn=1
#PBS -l pmem=128000MB
#PBS -l vmem=128000MB
#PBS -l mem=128000MB
#PBS -q cegs


#java -jar /home/cmb-panasas2/tkitapci/software/picard/picard-tools-1.110/AddOrReplaceReadGroups.jar \
#        I=$bam_file_path \
#        O=$bam_file_dir/$bam_file_name-read_group_added_sorted.bam \
#        SO=coordinate \
#        ID=$bam_file_name \
#        LB=$bam_file_name \
#        PL=illumina \
#        PU=$PU \
#        SM=$SM \
#        VALIDATION_STRINGENCY=SILENT



bam_files=np.loadtxt("all_bam_files_excluding_not_used_wells_from_plate_4.txt",dtype="str")
#print bam_files

#/staging/sn1/tkitapci/Oyster_OsHv/alignments_Run1_Run2_Merged/Parent_12-sorted-rmdupped.bam

working_dir="/staging/sn1/tkitapci/Oyster_OsHv/alignments_Run1_Run2_Merged/"

for bam_file in bam_files:
	vec=bam_file.split("/")
	file_name=vec[-1].split("-sorted-rmdupped")[0]
	#print file_name
	ID=file_name
	LB=file_name
	PL="illumina"
	PU=file_name
	SM=file_name
	f=open("job_%s.sh" %(file_name),"w")
	f.write("#PBS -l walltime=5:00:00\n")
	f.write("#PBS -l nodes=1:ppn=1\n")
	f.write("#PBS -l pmem=5000MB\n")
	f.write("#PBS -l vmem=5000MB\n")
	f.write("#PBS -l mem=5000MB\n")
	f.write("#PBS -q cegs\n")
	
	f.write("cd %s\n" %(working_dir))

	f.write("java -jar -Xmx3000M /home/cmb-panasas2/tkitapci/software/picard/picard-tools-1.110/AddOrReplaceReadGroups.jar I=%s O=%s.read_group_added.bam SO=coordinate ID=%s LB=%s PL=%s PU=%s SM=%s VALIDATION_STRINGENCY=SILENT\n" %(bam_file,bam_file,ID,LB,PL,PU,SM))
	#index the bam files after adding the read group
	f.write("samtools index %s.read_group_added.bam\n" %(bam_file))
	f.close()	
			
