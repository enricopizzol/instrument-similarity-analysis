

import glob
import os
import sys
import time
import warnings

import pandas as pd

warnings.filterwarnings('ignore')


# ============================================================================
# STEP 1: DATA TRANSFORMATION FUNCTIONS
# ============================================================================

def extract_symbol_from_filename(filename):
    """Extract symbol from filename like 'ABEV3_ticks.csv' -> 'ABEV3'"""
    basename = os.path.basename(filename)
    return basename.replace('_ticks.csv', '')


def load_and_transform_file(csv_path):
    """Load a single CSV file and apply transformations with trading hours filter"""
    symbol = extract_symbol_from_filename(csv_path)
    
    print(f"Processing {symbol}...", end=" ")
    
    # Load data
    df = pd.read_csv(csv_path)
    
    # Convert to timestamp using millisecond precision
    df['datetime'] = pd.to_datetime(df['time_msc'], unit='ms')
    
    # Extract hour for filtering
    df['hour'] = df['datetime'].dt.hour
    
    # Filter for trading hours: 10:00 AM to 5:00 PM (17:00)
    trading_hours_mask = (df['hour'] >= 10) & (df['hour'] < 17)
    df = df[trading_hours_mask].copy()
    
    # Add instrument column
    df['instrument'] = symbol
    
    # Set datetime as index
    df = df.set_index('datetime')
    
    # Apply forward fill and backward fill
    df = df.ffill().bfill()
    
    # Keep only datetime (index), last, and instrument columns
    df = df[['instrument', 'last']]
    
    print(f"✅ {len(df):,} rows")
    
    return df


def transform_all_files(dataset_folder='dataset', output_folder='clean_dataset/instrument_series'):
    """Transform all CSV files and save to individual files"""
    # Get list of all CSV files
    csv_files = glob.glob(os.path.join(dataset_folder, '*.csv'))
    
    print(f"Found {len(csv_files)} CSV files")
    print(f"Processing all files...\n")
    
    # Create output directory
    os.makedirs(output_folder, exist_ok=True)
    
    for i, csv_file in enumerate(csv_files, 1):
        try:
            df = load_and_transform_file(csv_file)
            
            # Extract instrument name and save
            symbol = extract_symbol_from_filename(csv_file)
            output_file = os.path.join(output_folder, f'{symbol}_transformed.csv')
            df.to_csv(output_file)
            
            # Progress indicator
            if i % 10 == 0:
                print(f"\nProcessed and saved {i}/{len(csv_files)} files...")
                
        except Exception as e:
            print(f"❌ Error processing {os.path.basename(csv_file)}: {str(e)}")
    
    print(f"\n✅ Successfully processed and saved {len(csv_files)} files to '{output_folder}/'")
    return output_folder


# ============================================================================
# STEP 2: CORRELATION ANALYSIS FUNCTIONS
# ============================================================================

def load_instrument_data(instrument, data_folder='clean_dataset/instrument_series'):
    """Load transformed data for a single instrument."""
    csv_path = os.path.join(data_folder, f'{instrument}_transformed.csv')
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")
    
    # Load data
    df = pd.read_csv(csv_path)
    
    # Convert datetime column to datetime type
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Set datetime as index
    df = df.set_index('datetime')
    
    # Sort index to ensure it's monotonic
    df = df.sort_index()
    
    # Keep only last price
    df = df[['last']]
    
    return df


def _ensure_unique_index(df):
    """Ensure datetime index is unique by aggregating duplicates with last()."""
    if df.index.has_duplicates:
        df = df.groupby(level=0).last()
    return df


def resample_and_fill(df, frequency):
    """
    Resample dataframe by frequency and forward fill.
    
    Frequency mapping:
    - '1ms' -> Aggregate duplicate timestamps at ms level
    - '1S' -> '1S' (seconds)
    - '1T' -> '1T' (minutes)
    - '1H' -> '1H' (hours)
    - '1D' -> '1D' (days)
    """
    # For 1ms, aggregate duplicates to ensure unique index
    if frequency == '1ms':
        return _ensure_unique_index(df)
    
    # Resample and take last value in each period
    df_resampled = df.resample(frequency).last()
    
    # Forward fill missing values
    df_resampled = df_resampled.ffill()
    
    return df_resampled


def calculate_correlation_with_timing(instrument1, instrument2, frequency, correlation_method):
    """
    Calculate correlation between two instruments with timing.
    
    Returns:
    --------
    tuple: (correlation_value, execution_time_seconds)
    """
    try:
        # Start timing
        start_time = time.time()
        
        # Load both instruments from transformed files
        df1 = load_instrument_data(instrument1)
        df2 = load_instrument_data(instrument2)
        
        # Resample both by the specified frequency
        df1_resampled = resample_and_fill(df1, frequency)
        df2_resampled = resample_and_fill(df2, frequency)
        
        # Ensure both indices are unique (defensive check)
        df1_resampled = _ensure_unique_index(df1_resampled)
        df2_resampled = _ensure_unique_index(df2_resampled)
        
        # Concatenate the two series side by side
        df_combined = pd.concat([df1_resampled, df2_resampled], axis=1)
        df_combined.columns = ['last_1', 'last_2']
        
        # Drop rows with any NaN values
        df_combined = df_combined.dropna()
        
        # Need at least 2 points to calculate correlation
        if len(df_combined) < 2:
            return None, time.time() - start_time
        
        # Calculate correlation using pandas corr method
        correlation_value = df_combined['last_1'].corr(df_combined['last_2'], method=correlation_method)
        
        # End timing
        end_time = time.time()
        execution_time = end_time - start_time
        
        return correlation_value, execution_time
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, time.time() - start_time


# ============================================================================
# TESTING
# ============================================================================

def test_mock():
    """
    Test function with mock data.
    Simulates processing: CPLE6,ITSA4,1Year,1ms,spearman,8
    """
    # Mock CSV line
    mock_csv_line = "CPLE6,ITSA4,1Year,1ms,spearman,8"

    # Process the mock line
    result = process_single_line(mock_csv_line)

    return result


# ============================================================================
# SINGLE LINE PROCESSING
# ============================================================================

def process_single_line(csv_line, output_file='correlation_results.csv'):
    """
    Process a single CSV line with correlation parameters.
    
    Parameters:
    -----------
    csv_line : str
        CSV line in format: instrument1,instrument2,period,frequency,correlation,repeat
        Example: CPLE6,ITSA4,1Year,1ms,spearman,8
    output_file : str
        Output CSV file to append results
    
    Returns:
    --------
    dict : Results dictionary
    """
    # Parse the CSV line
    parts = csv_line.strip().split(',')
    
    if len(parts) != 6:
        raise ValueError(f"Invalid CSV line format. Expected 6 fields, got {len(parts)}")
    
    instrument1, instrument2, period, frequency, correlation_method, repeat = parts
    
    # Log start
    print(f"Processing: {instrument1},{instrument2},{period},{frequency},{correlation_method},{repeat}")
    
    # Calculate correlation
    corr_value, exec_time = calculate_correlation_with_timing(
        instrument1, instrument2, frequency, correlation_method
    )
    
    # Prepare result
    result = {
        'instrument1': instrument1,
        'instrument2': instrument2,
        'period': period,
        'frequency': frequency,
        'correlation_method': correlation_method,
        'repeat': int(repeat),
        'correlation_value': corr_value,
        'execution_time_seconds': exec_time
    }
    
    # Save to CSV (append if exists)
    df_result = pd.DataFrame([result])
    
    # Check if file exists
    if os.path.exists(output_file):
        # Append without header
        df_result.to_csv(output_file, mode='a', header=False, index=False)
    else:
        # Create new file with header
        df_result.to_csv(output_file, mode='w', header=True, index=False)
    
    # Log finish
    print(f"Finished: correlation={corr_value}, time={exec_time:.4f}s, saved to {output_file}")
    
    return result


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function.
    
    Usage:
        python correlation_analysis.py "CPLE6,ITSA4,1Year,1ms,spearman,8"
        python correlation_analysis.py --test    # Run mock test
    
    The CSV line must contain: instrument1,instrument2,period,frequency,correlation,repeat
    """

    # CSV line must be provided as command line parameter
    if len(sys.argv) < 2:
        print("Error: CSV line parameter required")
        print("\nUsage:")
        print('  python correlation_analysis.py "instrument1,instrument2,period,frequency,correlation,repeat"')
        print('  python correlation_analysis.py --test    # Run mock test')
        print("\nExample:")
        print('  python correlation_analysis.py "CPLE6,ITSA4,1Year,1ms,spearman,8"')
        sys.exit(1)
    
    # Get CSV line from command line parameter
    csv_line = sys.argv[1]
    
    # Process the single line
    result = process_single_line(csv_line)
    
    return result


if __name__ == "__main__":
    test_mock()
