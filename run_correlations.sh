#!/bin/bash
# Bash script to process correlation combinations
# Usage: ./run_correlations.sh [input_csv] [num_lines]

# Default values
INPUT_CSV="${1:-instrument_combinations_shuffled.csv}"
NUM_LINES="${2:-all}"

# Check if input file exists
if [ ! -f "$INPUT_CSV" ]; then
    echo "Error: Input file '$INPUT_CSV' not found"
    exit 1
fi

echo "Processing correlations from: $INPUT_CSV"
echo "----------------------------------------"

# Count total lines (excluding header)
TOTAL_LINES=$(tail -n +2 "$INPUT_CSV" | wc -l)
echo "Total combinations: $TOTAL_LINES"

# Process lines
COUNTER=0
if [ "$NUM_LINES" = "all" ]; then
    echo "Processing all lines..."
    tail -n +2 "$INPUT_CSV" | while IFS= read -r line; do
        COUNTER=$((COUNTER + 1))
        echo "starting new process for line ($COUNTER / $TOTAL_LINES)"
        python correlation_analysis.py "$line"
    done
else
    echo "Processing first $NUM_LINES lines..."
    tail -n +2 "$INPUT_CSV" | head -n "$NUM_LINES" | while IFS= read -r line; do
        COUNTER=$((COUNTER + 1))
        echo "starting new process for line ($COUNTER / $NUM_LINES)"
        python correlation_analysis.py "$line"
    done
fi

echo "----------------------------------------"
echo "Processing complete!"
