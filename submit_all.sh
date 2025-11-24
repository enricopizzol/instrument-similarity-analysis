#!/bin/bash

# Array of nodes (adjust to match your cluster's node names)
declare -a NODES=(draco1 draco2 draco3 draco4 draco5 draco6 draco7)

# Array of input files (must be in the same order as nodes)
# First 6 nodes: Top 10 most liquid instruments (97% faster!)
# 7th node: POC test input
declare -a INPUTS=(
    instrument_combinations_top10_part_1.csv
    instrument_combinations_top10_part_2.csv
    instrument_combinations_top10_part_3.csv
    instrument_combinations_top10_part_4.csv
    instrument_combinations_top10_part_5.csv
    instrument_combinations_top10_part_6.csv
    input_sample.csv
)

echo "Submitting ${#NODES[@]} correlation jobs..."
echo "  - Nodes 1-6: Top 10 instruments (~1,125 rows each)"
echo "  - Node 7: POC test input"
echo "  - Total: 6,750 combinations (97% reduction)"
echo ""

for i in ${!NODES[@]}; do
    echo "[$((i+1))/${#NODES[@]}] Submitting to ${NODES[$i]} with input ${INPUTS[$i]}"
    
    # Submit job with both nodelist and INPUT variable
    sbatch --nodelist=${NODES[$i]} --export=INPUT=${INPUTS[$i]} run_corr.slurm
    
    # Small delay to avoid overwhelming the scheduler
    sleep 0.5
done

echo ""
echo "✅ All jobs submitted! Check status with: squeue -u \$USER"
