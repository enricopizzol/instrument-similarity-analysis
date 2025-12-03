#!/bin/bash

# Array of nodes
declare -a NODES=(draco1 draco2 draco3 draco4 draco5 draco6)

# Array of input files (POC Top 10 files)
declare -a INPUTS=(
    "instrument_combinations_top10_part_1.csv"
    "instrument_combinations_top10_part_2.csv"
    "instrument_combinations_top10_part_3.csv"
    "instrument_combinations_top10_part_4.csv"
    "instrument_combinations_top10_part_5.csv"
    "instrument_combinations_top10_part_6.csv"
)

echo "Submitting ${#NODES[@]} POC correlation jobs..."

for i in ${!NODES[@]}; do
    echo "[$((i+1))/${#NODES[@]}] Submitting to ${NODES[$i]} with input ${INPUTS[$i]}"
    
    # Submit job with both nodelist and INPUT variable
    sbatch --nodelist=${NODES[$i]} --export=INPUT=${INPUTS[$i]} run_corr.slurm
    
    # Small delay
    sleep 0.5
done

echo ""
echo "✅ All POC jobs submitted! Check status with: squeue -u \$USER"
