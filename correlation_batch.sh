#!/bin/bash

INPUT_CSV=$1
DATA_FOLDER=$2
OUTPUT_CSV=${3:-correlation_results.csv}

if [ -z "$INPUT_CSV" ] || [ -z "$DATA_FOLDER" ]; then
    echo "Usage: $0 <input_csv> <data_folder> [output_csv]"
    exit 1
fi

echo "Running Correlation Job"
echo "Input: $INPUT_CSV"
echo "Data: $DATA_FOLDER"
echo "Output: $OUTPUT_CSV"

mkdir -p "$(dirname "$OUTPUT_CSV")"

echo "Processing lines..."
count=0

while IFS= read -r line || [ -n "$line" ]; do
    [[ -z "$line" ]] && continue

    if [[ "$line" == *"instrument1"* ]]; then
        continue
    fi
    
    ((count++))
    echo "Processing [$count]: $line"
    
    python correlation_analysis.py "$line" --data-dir "$DATA_FOLDER" --output "$OUTPUT_CSV"
    
done < "$INPUT_CSV"

echo "Job Completed. Processed $count lines."
