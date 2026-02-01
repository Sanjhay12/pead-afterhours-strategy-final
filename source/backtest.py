import pandas as pd
from source.configuration import parameters

def backtest(signals,bars):

    max_holding = int(parameters["max_holding"])
    stop_loss = float(parameters["stop_loss"])
    take_profit = float(parameters["take_profit"])

    bars = bars.sort_values(["ticker", "timestamp_utc"]).reset_index(drop=True) #ensures index is from 0 onwards again
    results = [
]
    for i, row in signals.iterrows():
        ticker = row["ticker"]
        direction = row["direction"]
        entry_time = pd.to_datetime(row["entry_time_utc"], utc = True)
        entry_price = float(row["entry_price"])

        forced_exit_time = entry_time + pd.Timedelta(minutes=max_holding)

        filtered_bar = bars[(bars["ticker"] == ticker) & (bars["timestamp_utc"]>=entry_time) & (bars["timestamp_utc"] <= forced_exit_time )]

        if filtered_bar.empty:
            continue #skip the code below then

        #this code runs if the stop-loss or take-profit does not trigger i.e. we exit at last bar
        exit_time = filtered_bar.iloc[-1]["timestamp_utc"]
        exit_price = float(filtered_bar.iloc[-1]["close"])
        reason = "time"

        for i, row in filtered_bar.iterrows():
            price = float(row["close"]) #current price of bar
            
            if direction == "long":
                returns = (price/entry_price) -1
            else:
                returns = (entry_price/price) -1
            
            if returns <= -stop_loss:
                exit_time = row["timestamp_utc"]
                exit_price = price 
                reason = "stop_loss"
                break 


            if returns >= take_profit:
                exit_time = row["timestamp_utc"]
                exit_price = price 
                reason = "take_profit"
                break 

            
        #performed when break statement exits loop    
        if direction == "long":
            actual_return = (exit_price/entry_price) -1
        else:
            actual_return = (entry_price/exit_price) -1

        results.append({
            "ticker": ticker,
            "direction": direction,
            "entry_time_utc": entry_time,
            "entry_price": entry_price,
            "exit_time_utc": exit_time,
            "exit_price": float(exit_price),
            "exit_reason": reason,
            "return": actual_return,


        })
    return pd.DataFrame(results)