import pandas as pd
from source.configuration import parameters
from source.sessions import last_regular_close

def calculate_eps_surprise(eps_actual, eps_opinion):

    #surprise is (actual-opinion) / opinion, we return none if invalid

    if (eps_opinion is None) or (pd.isna(eps_opinion)) or (eps_opinion == 0):
        return None 
    
    if (eps_actual is None) or (pd.isna(eps_actual)):
        return None 
    
    return (float(eps_actual) - float(eps_opinion))/ abs(float(eps_opinion))

#func finds price we can start trading at after earnings released
def entry_price_after_earnings(bars, ticker, ERT):
    delay = int(parameters["entry_delay"]) #gets the values from config.py
    entry_time = pd.Timestamp(ERT) + pd.Timedelta(minutes=delay) 
    filtered_bars = bars[(bars["ticker"] == ticker) & (bars["timestamp_utc"]>=entry_time)] #all stocks that I can trade at any time now

    if filtered_bars.empty:
        return None, None 
    
    first_tradable_bar = filtered_bars.iloc[0]
    return first_tradable_bar["timestamp_utc"], float(first_tradable_bar["close"])

#purpose of func is to clean the raw data up into a table 
def create_features(earnings, bars, universe):
    bars = bars.sort_values(["ticker", "timestamp_utc"]).reset_index(drop=True) #ensures chronological order in terms of prices and index starts from 0 onwards
    rows = []
    for row_index,earnings_row in earnings.iterrows():
        ticker = str(earnings_row["ticker"]).strip()
        if ticker not in universe: #checks if ticker can be traded out of hours on IG
            continue 
        earnings_release_time = earnings_row["earnings_datetime_utc"]
        ERT = earnings_row["earnings_datetime_utc"]
        last_regular_session_close = last_regular_close(bars, ticker, ERT)
        entry_time, entry_price = entry_price_after_earnings(bars, ticker, ERT)
        surprise = calculate_eps_surprise(earnings_row["eps_actual"], earnings_row["eps_opinion"])
        
        after_hours_move = None 
        if last_regular_close is not None and entry_price is not None:
            after_hours_move = (entry_price / last_regular_session_close) -1

        rows.append({
            "TICKER": ticker,
            "earnings_datetime_utc" : earnings_release_time,
            "eps_actual" : ["eps_actual"],
            "eps_opinion": earnings_row["eps_opinion"],
            "eps_surprise": surprise,
            "last_regular_close": last_regular_session_close,
            "entry_time_utc": entry_time,
            "entry_price": entry_price,
            "after_hours_move": after_hours_move,
        })

    return pd.DataFrame(rows)


