#PBS -l walltime=5:00:00
#PBS -l nodes=1:ppn=1
#PBS -l pmem=5000MB
#PBS -l vmem=5000MB
#PBS -l mem=5000MB
#PBS -q cegs
cd /staging/sn1/tkitapci/Oyster_OsHv/alignments_Run1_Run2_Merged/
java -jar -Xmx3000M /home/cmb-panasas2/tkitapci/software/picard/picard-tools-1.110/AddOrReplaceReadGroups.jar I=/staging/sn1/tkitapci/Oyster_OsHv/alignments_Run1_Run2_Merged/Parent_52-sorted-rmdupped.bam O=/staging/sn1/tkitapci/Oyster_OsHv/alignments_Run1_Run2_Merged/Parent_52-sorted-rmdupped.bam.read_group_added.bam SO=coordinate ID=Parent_52 LB=Parent_52 PL=illumina PU=Parent_52 SM=Parent_52 VALIDATION_STRINGENCY=SILENT
samtools index /staging/sn1/tkitapci/Oyster_OsHv/alignments_Run1_Run2_Merged/Parent_52-sorted-rmdupped.bam.read_group_added.bam
