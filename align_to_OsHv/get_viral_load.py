import glob



#11751633 + 0 in total (QC-passed reads + QC-failed reads)
#0 + 0 secondary
#365 + 0 supplementary
#0 + 0 duplicates
#185679 + 0 mapped (1.58% : N/A)
#0 + 0 paired in sequencing


print "Plate_no,Barcode,All_Read_Counts,Mapped_Read_Count,Normalized_Viral_Count"

for file in glob.glob("/staging/sn1/tkitapci/Oyster_OsHv/alignments_to_OsHv/*-sorted-rmdupped.bam.stats"):
	f=open(file,"r")
	lines=f.readlines()
	f.close()
	fileName=file.split("/")[-1]
	
	plate_no=fileName.split("-")[0]
	barcode=fileName.split("-")[1]
	#sampleName=fileName.split("-")[0]+"-"+fileName.split("-")[1]
	


	#print sampleName

	all_read_count=float(lines[0].split(" ")[0])
	mapped_read_count=float(lines[4].split(" ")[0])
	
	normalized_viral_count=(mapped_read_count*1000000)/all_read_count

	print "%s,%s,%s,%s,%s"%(plate_no,barcode,all_read_count,mapped_read_count,normalized_viral_count)
	
	




