#######################################################################################
##Add read groups and sort with Picard
######################################################################################
java -jar /home/cmb-panasas2/tkitapci/software/picard/picard-tools-1.110/AddOrReplaceReadGroups.jar \
        I=$bam_file_path \
        O=$bam_file_dir/$bam_file_name-read_group_added_sorted.bam \
        SO=coordinate \
        ID=$bam_file_name \
        LB=$bam_file_name \
        PL=illumina \
        PU=$PU \
        SM=$SM \
        VALIDATION_STRINGENCY=SILENT

