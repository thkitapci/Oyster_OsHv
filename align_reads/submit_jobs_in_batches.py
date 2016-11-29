import os


#f=open("list_of_jobs.txt","r")

f=open("subset_of_jobs.txt","r")
jobs=f.readlines()

f.close()


#num_of_jobs_per_batch=80

num_of_jobs_per_batch=4

for i in range(0,len(jobs)):
	jobs[i]=jobs[i].rstrip("\n")




#submit num_of_jobs_per_batch jobs first
for i in range(0,num_of_jobs_per_batch):
	os.system("%s" %(jobs[i]))

#submit the rest as jobs completed

command="qstat -u tkitapci|grep -E \"\sR\s|\sQ\s\"|wc -l"

for i in range(num_of_jobs_per_batch,len(jobs)):
	num_of_process=int(os.popen(command).read())
	while num_of_process >= num_of_jobs_per_batch:
		os.system("sleep 5m")
		os.system("date")
		num_of_process=int(os.popen(command).read())
		print "There are %s processes running at the moment waiting for the next batch"%(num_of_process)	
	os.system("%s" %(jobs[i]))


