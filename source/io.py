import pandas as pd
from pathlib import Path

def load_universe(file_path):
    file_path = Path(file_path)
    dataframe = pd.read_excel(file_path, sheet_name = 0)
    if "Ticker" not in dataframe.columns:
        raise ValueError(print("Ticker column does not exist, columns are{}").format(dataframe.columns))
    
    tickers = (dataframe["Ticker"].dropna().astype(str).str.strip().str.upper())

    tickers = tickers[tickers != ""] #to remove any empty strings i.e. bugged tickers
    return set(tickers)

def filter_universe(universe, bars, liquidity = 2000000):
    filtered_universe = set()
    for i in universe:
        filtered_bars = bars[bars["ticker"] == i] #i is the ticker btw
        if filtered_bars.empty:
            continue
        average = (filtered_bars["close"]*filtered_bars["volume"]).mean()
        if average > liquidity: 
            filtered_universe.add(i)
    return filtered_universe

     

def load_earnings(file_path):

    file_path = Path(file_path)
    dataframe = pd.read_csv(file_path)

    required_columns = {"ticker", "earnings_datetime_utc", "eps_actual", "eps_opinion"}
    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(print("THere are missing columns {}").format(missing_columns))
    
    dataframe["ticker"] = dataframe["ticker"].astype(str).str.strip().str.upper()
    dataframe["earnings_datetime_utc"] = pd.to_datetime(dataframe["earnings_datetime_utc"], utc = True)
    dataframe["eps_actual"] = pd.to_numeric(dataframe["eps_actual"], errors = "coerce") #replace any values that produce errors to be replaced with NaN
    dataframe["eps_opinion"] = pd.to_numeric(dataframe["eps_opinion"], errors = "coerce")
    
    return dataframe



def load_bars(file_paths):
    
    if isinstance(file_paths, (str, Path)):
        file_paths = [file_paths]

    frames = []

    for file_path in file_paths:
        file_path = Path(file_path)
        dataframe = pd.read_csv(file_path)
        dataframe.columns = dataframe.columns.str.strip().str.lower()

        required_columns = {"ticker", "timestamp_utc", "close"}
        missing_columns = required_columns - set(dataframe.columns)
        if missing_columns:
            raise ValueError(f"Bars file {file_path.name} missing columns {missing_columns}")

        dataframe["ticker"] = dataframe["ticker"].astype(str).str.strip().str.upper()
        dataframe["timestamp_utc"] = pd.to_datetime(dataframe["timestamp_utc"], utc=True)
        dataframe["close"] = pd.to_numeric(dataframe["close"], errors="coerce")

        if "volume" in dataframe.columns:
            dataframe["volume"] = pd.to_numeric(dataframe["volume"], errors="coerce")
        else:
            dataframe["volume"] = 0

        frames.append(dataframe[["ticker", "timestamp_utc", "close", "volume"]])

    bars = pd.concat(frames, ignore_index=True)
    bars = bars.sort_values(["ticker", "timestamp_utc"]).reset_index(drop=True)

    return bars
