#!/bin/bash

# Script to submit multiple Slurm jobs for parallel processing
# Usage: ./submit_all.sh

# List of input files
FILES=(
    "instrument_combinations_part_1.csv"
    "instrument_combinations_part_2.csv"
    "instrument_combinations_part_3.csv"
    "instrument_combinations_part_4.csv"
    "instrument_combinations_part_5.csv"
    "instrument_combinations_part_6.csv"
)

# Loop through files and submit a job for each
for FILE in "${FILES[@]}"; do
    if [ -f "$FILE" ]; then
        echo "Submitting job for $FILE..."
        sbatch run_slurm_job.slurm "$FILE"
    else
        echo "Warning: $FILE not found, skipping."
    fi
done

echo "All jobs submitted."
