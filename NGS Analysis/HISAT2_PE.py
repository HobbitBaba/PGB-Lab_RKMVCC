import os
import subprocess

# Define the directory where your paired-end FASTQ files are located
input_dir = "/mnt/WD_Blue/Sorghum/TEST/FASTQ/"

# Define the directory where you want to save the mapped BAM files
output_dir = "/mnt/WD_Blue/Sorghum/TEST/Mapped/"

# Define the location of the HISAT2 index
index_path = "/mnt/WD_Blue/Sorghum/TEST/HISAT2_Index/sbi_index"

# Define the directory for HISAT2 summary files
summary_dir = "/mnt/WD_Blue/Sorghum/TEST/Mapped/Summary/"

# Create the output and summary directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(summary_dir, exist_ok=True)

# List all the paired-end FASTQ files in the input directory
fastq_files_1 = [f for f in os.listdir(input_dir) if f.endswith("_forward.fastqsanger.gz")]

# Loop through each paired-end sample and run HISAT2
for fastq_file_1 in fastq_files_1:
    sample_name = fastq_file_1.replace("_forward.fastqsanger.gz", "")
    fastq_file_2 = fastq_file_1.replace("_forward.fastqsanger.gz", "_reverse.fastqsanger.gz")

    input_path_1 = os.path.join(input_dir, fastq_file_1)
    input_path_2 = os.path.join(input_dir, fastq_file_2)
    output_sam = os.path.join(output_dir, f"{sample_name}.sam")
    summary_file = os.path.join(summary_dir, f"{sample_name}_summary.txt")

    # Run HISAT2 command with --new-summary and --summary-file options
    hisat2_cmd = f"hisat2 -p 8 --dta -x {index_path} -1 {input_path_1} -2 {input_path_2} -S {output_sam} --new-summary --summary-file {summary_file}"
    subprocess.run(hisat2_cmd, shell=True)

    print(f"Processed: {sample_name}")

    # Convert SAM to BAM
    bam_output = os.path.join(output_dir, f"{sample_name}.bam")
    samtools_view_cmd = f"samtools view -bS {output_sam} > {bam_output}"
    subprocess.run(samtools_view_cmd, shell=True)

    # Remove the original SAM file
    os.remove(output_sam)

    # Sort BAM file
    sorted_bam_output = os.path.join(output_dir, f"{sample_name}_sorted.bam")
    samtools_sort_cmd = f"samtools sort {bam_output} -o {sorted_bam_output}"
    subprocess.run(samtools_sort_cmd, shell=True)

    # Remove the unsorted BAM file
    os.remove(bam_output)

    # Index sorted BAM file
    samtools_index_cmd = f"samtools index {sorted_bam_output}"
    subprocess.run(samtools_index_cmd, shell=True)

print("Mapping and sorting complete.")
