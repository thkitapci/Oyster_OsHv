#Author: T. Hamdi Kitapci
import glob, os, sys

if len(sys.argv) != 3:
	print "missing argument"
	sys.exit()

f=open("barcodes.csv","r")
barcodes=[]
for line in f:
	line=line.rstrip("\n")
	barcodes.append(line)
f.close()


	
#source_folder = sys.argv[1]
source_file=sys.argv[1]
output_folder = sys.argv[2]




os.system("mkdir %s"%(output_folder))

os.chdir(output_folder)

#job_path=output_folder +"/" + "job_kmergenie.sh"

f=open(source_file,"r")
input_files=[]
for line in f:
	line=line.rstrip("\n")
	input_files.append(line)
f.close()

#source_files=source_folder +"/" + "*.fastq"
for input_file in input_files:
	input_file=input_file.rstrip("\n")
	#Generate the barcodes file
	barcode_file_name="barcodes_%s.txt"%(os.path.basename(input_file))
	barcode_file_path=output_folder+"/"+barcode_file_name
	f=open(barcode_file_path,"w")
	for barcode in barcodes:
		barcode=barcode.split(",")[1]
		#print barcode
		#Hamdi_5_NoIndex_L006_R1_001.fastq.gz 0 AACT Plate_0
		plate_no=os.path.basename(input_file).split("_")[1]
		f.write("%s %s %s Plate_%s\n"%(input_file,plate_no,barcode,plate_no)) 	
	f.close()


		
	job_path=output_folder +"/" + "job_%s.sh"%(os.path.basename(input_file))
	f = open(job_path, 'w')
	#output_file_name=os.path.basename(input_file)

	#output_file_name=os.path.splitext(output_file_name)[0]  #remove .gz from the end so that the output file has extension .fastq

	command="python /home/cmb-07/sn1/tkitapci/Oyster_OsHV/GBS/raw_data/gbs_demultiplex_fastq.py %s %s %s" %(input_file,barcode_file_path,output_folder)
	
	f.write("#PBS -l walltime=300:00:00\n")
	f.write("#PBS -l nodes=1:ppn=1\n")
	f.write("#PBS -l pmem=12000MB\n")
	f.write("#PBS -l vmem=12000MB\n")
	f.write("#PBS -l mem=12000MB\n")
	f.write("#PBS -q cegs\n")
	f.write(command)
	f.close()
	#print command
	os.system("qsub %s" %(job_path))
