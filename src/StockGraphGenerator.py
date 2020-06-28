import yfinance as yf

def make_OHLC_graph(ticker, start_date, end_date):
    df = yf.download(ticker, start_date, end_date)
    df = df[['Open', 'High', 'Low', 'Close']]
    print(df)