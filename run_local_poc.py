"""
Local POC Test - Pure Python Implementation
Emulates the behavior of run_corr.slurm without Docker/Shell scripts
"""

import pandas as pd
import sys
from pathlib import Path

# Add the current directory to path to import correlation_analysis
sys.path.insert(0, str(Path(__file__).parent))

from correlation_analysis import process_single_line

def run_local_poc_test():
    """Run the POC test locally using pure Python."""
    
    # Configuration
    PROJECT_HOME = Path.cwd()
    DATA_FOLDER = PROJECT_HOME / "transformed_data" / "instrument_series"
    INPUT_FILE = PROJECT_HOME / "input_sample.csv"
    OUTPUT_FILE = PROJECT_HOME / "test_correlation_results_local.csv"
    
    print("=" * 80)
    print("LOCAL POC TEST - Pure Python Implementation")
    print("=" * 80)
    print(f"\nProject Home: {PROJECT_HOME}")
    print(f"Data Folder: {DATA_FOLDER}")
    print(f"Input File: {INPUT_FILE}")
    print(f"Output File: {OUTPUT_FILE}")
    
    # Verify files exist
    print("\n" + "-" * 80)
    print("Verifying files...")
    print("-" * 80)
    
    if not INPUT_FILE.exists():
        print(f"❌ ERROR: Input file not found: {INPUT_FILE}")
        return
    
    if not DATA_FOLDER.exists():
        print(f"❌ ERROR: Data folder not found: {DATA_FOLDER}")
        print("   Make sure transformed_data/instrument_series exists")
        return
    
    csv_files = list(DATA_FOLDER.glob("*_transformed.csv"))
    print(f"✅ Data folder found with {len(csv_files)} CSV files")
    
    # Delete output file if it exists (fresh start)
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
        print(f"🗑️  Deleted existing output file")
    
    # Read input file
    print("\n" + "-" * 80)
    print("Reading input file...")
    print("-" * 80)
    
    input_df = pd.read_csv(INPUT_FILE)
    print(f"✅ Loaded {len(input_df)} combinations to process\n")
    print(input_df.to_string(index=False))
    
    # Process each line
    print("\n" + "=" * 80)
    print("PROCESSING CORRELATIONS")
    print("=" * 80)
    
    for idx, row in input_df.iterrows():
        # Reconstruct CSV line format
        csv_line = f"{row['instrument1']},{row['instrument2']},{row['period']},{row['frequency']},{row['correlation']},{row['repeat']}"
        
        print(f"\n[{idx+1}/{len(input_df)}] Processing: {csv_line}")
        
        try:
            # Call the correlation analysis function directly
            process_single_line(
                csv_line=csv_line,
                output_file=str(OUTPUT_FILE),
                data_folder=str(DATA_FOLDER)
            )
            print(f"  ✅ Completed")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Load and display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    if OUTPUT_FILE.exists():
        results_df = pd.read_csv(OUTPUT_FILE)
        
        print(f"\n✅ Results saved to: {OUTPUT_FILE}")
        print(f"Total rows: {len(results_df)}\n")
        
        # Display results
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 120)
        print(results_df.to_string(index=False))
        
        # Summary statistics
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        
        total = len(results_df)
        successful = results_df['correlation_value'].notna().sum()
        failed = total - successful
        
        print(f"\nTotal correlations: {total}")
        print(f"  ✅ Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"  ❌ Failed: {failed} ({failed/total*100:.1f}%)")
        
        # By method
        print("\nBy correlation method:")
        for method in results_df['correlation_method'].unique():
            method_df = results_df[results_df['correlation_method'] == method]
            success = method_df['correlation_value'].notna().sum()
            total_method = len(method_df)
            status = "✅" if success == total_method else "⚠️"
            print(f"  {status} {method}: {success}/{total_method} successful")
        
        # Execution time
        print(f"\nExecution time:")
        print(f"  Mean: {results_df['execution_time_seconds'].mean():.2f}s")
        print(f"  Total: {results_df['execution_time_seconds'].sum():.2f}s")
        
        # Correlation values (successful only)
        successful_corr = results_df[results_df['correlation_value'].notna()]['correlation_value']
        if len(successful_corr) > 0:
            print(f"\nCorrelation values (successful only):")
            print(f"  Mean: {successful_corr.mean():.4f}")
            print(f"  Range: [{successful_corr.min():.4f}, {successful_corr.max():.4f}]")
        
        print("\n" + "=" * 80)
        print("✅ POC TEST COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
    else:
        print(f"\n❌ ERROR: Output file not created: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_local_poc_test()
