"""
Generate all combinations of instrument pairs with shuffled order.
"""

import pandas as pd
import random
from itertools import combinations

def generate_all_combinations():
    """Generate all combinations and shuffle them."""
    
    # Instrument list
    instruments = [
        "ALOS3", "ABEV3", "ASAI3", "AURE3", "AZZA3", "B3SA3", "BBSE3",
        "BBDC3", "BBDC4", "BRAP4", "BBAS3", "BRKM5", "BRAV3", "BPAC11",
        "CXSE3", "CEAB3", "CMIG4", "COGN3", "CPLE6", "CSAN3", "CPFE3",
        "CMIN3", "CURY3", "CVCB3", "CYRE3", "DIRR3", "ELET3", "ELET6",
        "EMBR3", "ENGI11", "ENEV3", "EGIE3", "EQTL3", "FLRY3", "GGBR4",
        "GOAU4", "HAPV3", "HYPE3", "IGTI11", "IRBR3", "ISAE4", "ITSA4",
        "ITUB4", "KLBN11", "RENT3", "LREN3", "MGLU3", "POMO4", "MBRF3",
        "BEEF3", "MOTV3", "MRVE3", "MULT3", "NATU3", "PCAR3", "PETR3",
        "PETR4", "RECV3", "PRIO3", "PSSA3", "RADL3", "RAIZ4", "RDOR3",
        "RAIL3", "SBSP3", "SANB11", "CSNA3", "SLCE3", "SMFT3", "SUZB3",
        "TAEE11", "VIVT3", "TIMS3", "TOTS3", "UGPA3", "USIM5", "VALE3",
        "VAMO3", "VBBR3", "VIVA3", "WEGE3", "YDUQ3"
    ]
    
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
    """Generate and save shuffled combinations."""
    
    print("Generating all combinations...")
    df = generate_all_combinations()
    
    print(f"Generated {len(df):,} combinations")
        
    # Save to CSV
    filename = 'instrument_combinations_shuffled.csv'
    df.to_csv(filename, index=False)
    
    print(f"\n✅ Shuffled combinations saved to: {filename}")
    print(f"File contains {len(df):,} rows")

if __name__ == "__main__":
    main()
