from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import pandas as pd
import MetaTrader5 as mt5
import os


def load_credentials():
    """Load MT5 credentials from .env file."""
    load_dotenv(find_dotenv())
    login = os.getenv("MT5_LOGIN")
    password = os.getenv("MT5_PASSWORD")
    server = os.getenv("MT5_SERVER")
    if not login or not password or not server:
        print("Missing credentials in .env file.")
        exit(1)
    return login, password, server


def initialize_mt5(login, password, server):
    """Initialize MT5 connection."""
    if not mt5.initialize(login=int(login), password=password, server=server):
        print("initialize() failed")
        mt5.shutdown()
        exit()
    print("initialize() succeeded")


def create_save_directory(folder_name="instrument_series"):
    """Create folder in project root to save CSV files."""
    root_dir = os.getcwd()
    save_path = os.path.join(root_dir, folder_name)
    os.makedirs(save_path, exist_ok=True)
    print(f"Directory ready: {save_path}")
    return save_path


def fetch_and_save_ticks(symbol, date_from, date_to, save_path):
    """Fetch tick data for a symbol and save to CSV."""
    print(f"Fetching data for {symbol}...", flush=True)

    ticks = mt5.copy_ticks_range(symbol, date_from, date_to, mt5.COPY_TICKS_TRADE)
    df = pd.DataFrame(ticks)

    if df.empty:
        print(f"No tick data for {symbol}", flush=True)
        return

    print(f"Formatting dataframe for {symbol}", flush=True)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    print(f"Saving {symbol}_ticks.csv", flush=True)
    file_path = os.path.join(save_path, f"{symbol}_ticks.csv")
    df.to_csv(file_path, index=False)
    print(f"Saved {len(df)} rows for {symbol} → {file_path}")


def main():
    # Load credentials and initialize MT5
    login, password, server = load_credentials()
    initialize_mt5(login, password, server)

    instruments_list = ["PETR4", "VALE3", "ITUB4", "BBDC4", "WEGE3"]
    date_to = datetime.now()
    date_from = date_to - timedelta(days=365)
    save_path = create_save_directory()

    for symbol in instruments_list:
        fetch_and_save_ticks(symbol, date_from, date_to, save_path)

    mt5.shutdown()
    print("All done. MT5 connection closed. Data retrieval complete.")


if __name__ == "__main__":
    main()
