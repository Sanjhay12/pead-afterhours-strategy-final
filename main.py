from pathlib import Path
from source.features import create_features
from source.metrics import produce_results
from source.io import load_universe, load_bars, load_earnings, filter_universe
from source.backtest import backtest
from source.signals import create_signals


print(" main.py started running")

dir = Path("data")

def main():
    universe = load_universe(dir / "All Sessions Shares.xlsx")
    bars = sorted(dir.glob("bars*.csv")) #ensures in order for time-series + only .csv files
    bars = load_bars(bars)
    print(bars.head())
    universe = filter_universe(universe, bars)
    earnings = load_earnings(dir / "eps_backtest_2021_2025.csv")
    print(earnings.head())

    features = create_features(earnings, bars, universe)
    print(features)
    signals = create_signals(features)
    print(signals)
    actual_backtest = backtest(signals, bars)
    print(actual_backtest)
    statistics = produce_results(actual_backtest)
    print("Summary of metrics:")
    for i, j in statistics.items():
        print("{}: {}".format(i,j)) #printing out dict


    
if __name__ == "__main__":
    main()
