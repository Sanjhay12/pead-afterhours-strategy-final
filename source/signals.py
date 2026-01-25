import pandas as pd
from source.configuration import parameters

def create_signals(features):
    
    eps_threshold = float(parameters["eps_surprise_threshold"])
    move_threshold = float(parameters["ah_move_threshold"])

    rows = []

    for i,row in features.iterrows():
        ticker = row.get("ticker")
        if ticker is None:
            ticker = row.get("TICKER")

        volume_ratio = row.get("volume_ratio")

        eps_surprise = row.get("eps_surprise")
        if eps_surprise is None:
            eps_surprise = row.get("eps surprise")
        ah_move = row.get("after_hours_move")
        if ah_move is None:
            ah_move = row.get("ah_move")

        #all this stuff above to avoid any inconsistencies with column names
        entry_time = row.get("entry_time_utc")
        entry_price = row.get("entry_price")

        #checking if any data is missing
        if pd.isna(eps_surprise) or pd.isna(ah_move) or pd.isna(entry_price):
            continue 

       #ignore if under thresholds     

        if abs(float(eps_surprise)) < eps_threshold:
            continue
        if abs(float(ah_move)) < move_threshold:
            continue

            #long short decisions
        if float(ah_move) > 0:
            dir = "long"
        else:
            dir = "short"

        volume_threshold = float(parameters("volume_ratio_threshold"))
        
        if pd.isna(volume_ratio):
            continue 
        if float(volume_ratio) < volume_threshold:
            continue 

        rows.append({
            "ticker" : ticker,
            "direction": dir,
            "entry_time_utc": entry_time,
            "entry_price": float(entry_price),
            "eps_surprise": float(eps_surprise),
            "ah_move": float(ah_move),
        })

    return pd.DataFrame(rows)