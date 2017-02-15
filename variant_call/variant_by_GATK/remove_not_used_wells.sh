patterns=`cat exluded_samples_on_plate_4.txt |cut -d "-" -f2 |xargs -I {} echo Plate_4-{}`

less all_bam_files.txt |grep -F -v "${patterns}" >all_bam_files_excluding_not_used_wells_from_plate_4.txt
