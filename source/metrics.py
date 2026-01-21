import pandas as pandas

def produce_results(trades):

    if trades.empty:
        return{
            "number of trades": 0,
            "win_rate": None,
            "average return": None,
            "total_return": None,
        }
    wins = trades[trades["return"] > 0]
    losses = trades[trades["return"] <= 0]

    trades_num = len(trades)
    win_rate = len(wins)/trades_num
    average_return = trades["return"].mean()
    total_return = (1+trades["return"]).prod()-1 #done to account for compounding

    return{
        "number of trades": trades_num,
        "win_rate": win_rate,
        "average_return": average_return,
        "total_return": total_return
    }