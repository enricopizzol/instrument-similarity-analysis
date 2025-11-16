#!/bin/bash
#SBATCH --job-name=corr_test
#SBATCH --partition=draco
#SBATCH --nodes=1
#SBATCH --nodelist=draco7
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --output=corr_test_%j.out
#SBATCH --error=corr_test_%j.err

echo "== Starting TEST correlation job on $(hostname), PID $$ =="

PROJECT_HOME="$HOME/instrument-similarity-analysis"

# Use the POC test input
INPUT_FILE="input_sample.csv"
OUTPUT_FILE="test_correlation_results_${SLURM_JOB_ID}.csv"

echo "Project Home: $PROJECT_HOME"
echo "Input File:   $INPUT_FILE"
echo "Output File:  $OUTPUT_FILE"
echo "Node:         $(hostname)"

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
ls -l $SCRATCH

cd $SCRATCH

# ---------------------------------------------
# 2) Build Docker image
# ---------------------------------------------
echo "== Building Docker image =="

docker build -t corr-container-test .

if [ $? -ne 0 ]; then
    echo "ERROR: Docker build failed"
    exit 1
fi

# ---------------------------------------------
# 3) Start periodic backup of results (every 2 minutes for testing)
# ---------------------------------------------
echo "== Starting periodic backup process =="

(
    while true; do
        sleep 120  # 2 minutes for testing
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
echo "== Running container for correlation task =="

docker run --rm \
    -v $SCRATCH:/work \
    -w /work \
    corr-container-test \
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

echo "== TEST job completed successfully =="
echo "== Check output file: $PROJECT_HOME/$OUTPUT_FILE =="
