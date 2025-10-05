import os
import pandas as pd
from datetime import datetime, timedelta
import MetaTrader5 as mt5
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

mt5_login = os.getenv("MT5_LOGIN")
mt5_password = os.getenv("MT5_PASSWORD")
mt5_server = os.getenv("MT5_SERVER")

if not mt5_login or not mt5_password or not mt5_server:
    print("Missing credentials in .env file.")
    exit(1)

initialize = mt5.initialize(login=int(mt5_login), password=mt5_password, server=mt5_login)

if not initialize:
    print("initialize() failed")
    mt5.shutdown()
    exit()
else:
    print("initialize() succeeded")

instruments_list = ["PETR4", "VALE3", "ITUB4"]
date_to = datetime.now()
date_from = date_to - timedelta(days=365)


save_path = r"\instrument-similarity-analysis\data"

os.makedirs(save_path, exist_ok=True)

for instrument in instruments_list:
    print(f"Fetching data for {instrument}...")

    ticks = mt5.copy_ticks_range(
        instrument,
        date_from,
        date_to,
        mt5.COPY_TICKS_TRADE
    )

    if ticks is None or len(ticks) == 0:
        print(f"No tick data for {instrument}")
        continue

    df = pd.DataFrame(ticks)

    df['time'] = pd.to_datetime(df['time'], unit='s')

    file_path = os.path.join(save_path, f"{instrument}_ticks.csv")
    df.to_csv(file_path, index=False)

    print(f"Saved {len(df)} rows for {instrument} → {file_path}")

mt5.shutdown()
print("\nAll done. MT5 connection closed. Data retrieval complete.")

