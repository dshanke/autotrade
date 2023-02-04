import yfinance as yf

df = yf.download('SPY', start='2020-01-01', end='2021-10-21')
df.to_csv('spy.csv')