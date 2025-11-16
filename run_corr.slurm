#!/bin/bash
#SBATCH --job-name=corr_job
#SBATCH --partition=draco
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=10:00:00
#SBATCH --output=corr_%j.out
#SBATCH --error=corr_%j.err

echo "== Starting correlation job on $(hostname), PID $$ =="

PROJECT_HOME="$HOME/instrument-similarity-analysis"

# INPUT_FILE is passed via --export from submit_all.sh
INPUT_FILE="$INPUT"
OUTPUT_FILE="correlation_${INPUT%.csv}_${SLURM_JOB_ID}.csv"

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

docker build -t corr-container .

if [ $? -ne 0 ]; then
    echo "ERROR: Docker build failed"
    exit 1
fi

# ---------------------------------------------
# 3) Run container and execute correlation job
# ---------------------------------------------
echo "== Running container for correlation task =="

docker run --rm \
    -v $SCRATCH:/work \
    -w /work \
    corr-container \
    bash -c "
        echo 'Container started';
        chmod +x correlation_batch.sh 2>/dev/null;
        bash correlation_batch.sh \"$INPUT_FILE\" transformed_data/instrument_series \"$OUTPUT_FILE\"
    "

echo "== Container finished running =="

# ---------------------------------------------
# 4) Copy results back to HOME
# ---------------------------------------------
echo "== Copying results back to HOME =="
cp "$SCRATCH/$OUTPUT_FILE" "$PROJECT_HOME/"

echo "== Job completed successfully =="
