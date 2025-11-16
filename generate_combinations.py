"""
Generate all combinations of instrument pairs with shuffled order.
"""

import pandas as pd
import random
from itertools import combinations

def generate_all_combinations():
    """Generate all combinations and shuffle them."""
    
    # Instrument list - filtered to only include instruments with >= 50MB data files
    instruments = sorted([
        "ABEV3", "ALOS3", "ASAI3", "B3SA3", "BBAS3", "BBDC3", "BBDC4",
        "BBSE3", "BEEF3", "BPAC11", "BRAV3", "CMIG4", "COGN3", "CPLE6",
        "CSAN3", "CSNA3", "CXSE3", "CYRE3", "ELET3", "ENEV3", "ENGI11",
        "EQTL3", "GGBR4", "HAPV3", "HYPE3", "ITSA4", "ITUB4", "KLBN11",
        "LREN3", "MGLU3", "MRVE3", "MULT3", "PETR3", "PETR4", "POMO4",
        "PRIO3", "RADL3", "RAIL3", "RAIZ4", "RDOR3", "RENT3", "SBSP3",
        "SMFT3", "SUZB3", "TIMS3", "TOTS3", "UGPA3", "USIM5", "VALE3",
        "VAMO3", "VBBR3", "VIVA3", "VIVT3", "WEGE3", "CMIN3"
    ])
    
    # Parameters
    periods = ['1Year']
    frequencies = ['1ms', '1S', '1T', '1H', '1D']
    correlations = ['pearson', 'kendall', 'spearman']
    
    # Generate all combinations
    combinations_list = []
    
    instrument_pairs = list(combinations(instruments, 2))
    
    # Number of repeats for robustness testing
    n_repeats = 10
    
    for instrument1, instrument2 in instrument_pairs:
        for period in periods:
            for frequency in frequencies:
                for correlation in correlations:
                    # Repeat each combination n_repeats times
                    for repeat in range(n_repeats):
                        combinations_list.append({
                            'instrument1': instrument1,
                            'instrument2': instrument2,
                            'period': period,
                            'frequency': frequency,
                            'correlation': correlation,
                            'repeat': repeat + 1
                        })
    
    # Convert to DataFrame
    df = pd.DataFrame(combinations_list)
    
    # Shuffle the rows
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df

def main():
    """Generate and save shuffled combinations split into 6 files."""
    
    print("Generating all combinations...")
    df = generate_all_combinations()
    
    print(f"Generated {len(df):,} combinations")
    
    # Split into 6 equal parts
    n_splits = 6
    split_size = len(df) // n_splits
    
    print(f"\nSplitting into {n_splits} files of ~{split_size:,} rows each...")
    
    for i in range(n_splits):
        start_idx = i * split_size
        # Last split gets any remaining rows
        end_idx = (i + 1) * split_size if i < n_splits - 1 else len(df)
        
        df_split = df.iloc[start_idx:end_idx]
        filename = f'instrument_combinations_part_{i+1}.csv'
        df_split.to_csv(filename, index=False)
        
        print(f"✅ Saved {filename} ({len(df_split):,} rows)")
    
    print(f"\n✅ Total: {len(df):,} combinations split into {n_splits} files")

if __name__ == "__main__":
    main()
