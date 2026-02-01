import pandas as pd



def equity_curve(returns: pd.Series):
    returns = returns.fillna(0).astype(float)
    equity = (1+returns).cumprod()
    return equity

def drawdowns(equity: pd.Series):
    equity = equity.astype(float)
    peak = equity.cummax()
    drawdown = (equity-peak)/peak 
    
    max_drawdon = drawdown.min()
    max_dur = 0
    current_dur = 0
    for i in drawdown:
        if i < 0:
            current_dur += 1
            if current_dur > max_dur:
                max_dur = current_dur
        else:
            current_dur = 0
    return drawdown, max_drawdon, max_dur



def sharpe_ratio(returns: pd.Series):
    returns = returns.dropna().astype(float)
    if returns.std() == 0:
        return None 
    return returns.mean()/returns.std()

def calculate_trades(returns: pd.Series):
    returns = returns.dropna().astype(float)
    wins = returns[returns > 0]
    losses = returns[returns <= 0]

    if len(returns):
        win_rate = len(wins)/len(returns)
    else:
        win_rate = 0
    if len(wins):
        average_win = wins.mean()
    else:
        average_win = 0 
    if len(losses):
        average_loss = losses.mean()
    else:
        average_loss = 0
    
    if average_loss != 0:
        payoff_ratio = average_win/ abs(average_loss)
    else:
        payoff_ratio = 0
    expected = win_rate * average_win * (1-win_rate) * average_loss

    return {"win_rate": win_rate, "average_win": average_win, "average_loss": average_loss, "payoff_ratio": payoff_ratio, "expectancy": expected}



   
    

def produce_results(trades):

    if trades.empty:
        return{
            "number of trades": 0,
            "win_rate": None,
            "average return": None,
            "total_return": None,
        }
     
    returns = trades["return"]
    equity = equity_curve(returns)
    drawdowns, max_drawdown, max_drawdown_duration = drawdowns(equity)
    sharpe = sharpe_ratio(returns)
    win_rate, average_win, average_loss, expeced = calculate_trades(returns)


    

    return{
        "max_drawdown":max_drawdown,
        "max_drawdown_duration": max_drawdown_duration, 
        "sharpe_ratio": sharpe,
        "win_rate": win_rate,
        "average_win": average_win,
        "average_loss": average_loss,
        "expected": expeced,
        "final_equity": equity.iloc[-1],
    }