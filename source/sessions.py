import pandas as pd

def check_regular_session(time: pd.Timestamp):
    #checks if regular session or not: time is 14:39 to 21:00 Universal Coordinated Time
    time = pd.Timestamp(time)
    hour = time.hour
    minute = time.minute
    if hour <14 or (hour == 15 and minute < 30):
        return False #not regular is before 14:30 and after 21:00
    
    if hour >= 21:
        return False
    return True 

#ERT is the earings release time, ticker is symbol and bar which is a df with timestamp_utc, open, high, low, close, volume etc.
#func gets price of stock closing during normal hours before earnings are announced
def last_regular_close(bars, ticker, ERT):
    bars = bars[(bars["ticker"]== ticker) & (bars["timestamp_utc"] < ERT)]

    bars = bars[bars["timestamp_utc"].apply(check_regular_session)] #keeps bars from normal market hours ONLY 


    if len(bars) == 0:
        return None
    
    return float(bars["close"].iloc[-1]) #recent closing price before earnings -using iloc instead of .tail().values to get last row
