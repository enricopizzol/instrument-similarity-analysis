#!/bin/bash
#SBATCH --job-name=poc_corr
#SBATCH --partition=draco
#SBATCH --nodes=1
#SBATCH --nodelist=draco7
#SBATCH --ntasks=1
#SBATCH --time=02:00:00
#SBATCH --output=poc_corr_%j.out
#SBATCH --error=poc_corr_%j.err

echo "== Starting POC correlation job on $(hostname), PID $$ =="

PROJECT_HOME="$HOME/instrument-similarity-analysis"

# POC input file with all frequencies
INPUT_FILE="input_sample.csv"
OUTPUT_FILE="poc_correlation_results_${SLURM_JOB_ID}.csv"

echo "Project Home: $PROJECT_HOME"
echo "Input File:   $INPUT_FILE"
echo "Output File:  $OUTPUT_FILE"
echo "Node:         $(hostname)"
echo "Total combinations: 210 (14 frequencies × 3 methods × 5 repeats)"

# ---------------------------------------------
# 1) Copy needed files to SCRATCH
# ---------------------------------------------
echo "== Copying files to SCRATCH =="

cp "$PROJECT_HOME/Dockerfile" "$SCRATCH/"
cp "$PROJECT_HOME/requirements.txt" "$SCRATCH/"
cp "$PROJECT_HOME/correlation_analysis.py" "$SCRATCH/"
cp "$PROJECT_HOME/$INPUT_FILE" "$SCRATCH/"
cp "$PROJECT_HOME/correlation_batch.sh" "$SCRATCH/"
cp -r "$HOME/transformed_data" "$SCRATCH/"

echo "Files copied:"
ls -lh $SCRATCH/*.csv $SCRATCH/*.py $SCRATCH/*.sh

cd $SCRATCH

# ---------------------------------------------
# 2) Build Docker image
# ---------------------------------------------
echo "== Building Docker image =="

docker build -t corr-container-poc .

if [ $? -ne 0 ]; then
    echo "ERROR: Docker build failed"
    exit 1
fi

# ---------------------------------------------
# 3) Start periodic backup of results (every 2 minutes)
# ---------------------------------------------
echo "== Starting periodic backup process =="

(
    while true; do
        sleep 120  # 2 minutes
        if [ -f "$SCRATCH/$OUTPUT_FILE" ]; then
            cp "$SCRATCH/$OUTPUT_FILE" "$PROJECT_HOME/${OUTPUT_FILE%.csv}_backup.csv"
            echo "[$(date)] Backup created: ${OUTPUT_FILE%.csv}_backup.csv"
        fi
    done
) &
BACKUP_PID=$!

# ---------------------------------------------
# 4) Run container and execute correlation job
# ---------------------------------------------
echo "== Running container for POC correlation task =="
echo "== Testing all frequencies: 1ms, 5ms, 10ms, 50ms, 100ms, 500ms, 1S, 30S, 1T, 5T, 15T, 30T, 1H, 1D =="

docker run --rm \
    -v $SCRATCH:/work \
    -w /work \
    corr-container-poc \
    bash -c "
        echo 'Container started';
        chmod +x correlation_batch.sh 2>/dev/null;
        bash correlation_batch.sh \"$INPUT_FILE\" transformed_data/instrument_series \"$OUTPUT_FILE\"
    "

echo "== Container finished running =="

# Stop the backup process
kill $BACKUP_PID 2>/dev/null

# ---------------------------------------------
# 5) Copy final results back to HOME
# ---------------------------------------------
echo "== Copying final results back to HOME =="
cp "$SCRATCH/$OUTPUT_FILE" "$PROJECT_HOME/"

# Remove backup file if final copy succeeded
rm -f "$PROJECT_HOME/${OUTPUT_FILE%.csv}_backup.csv"

echo "== POC job completed successfully =="
echo "== Results saved to: $PROJECT_HOME/$OUTPUT_FILE =="
echo "== Total combinations processed: 210 =="
