import yfinance as yf
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import os


def draw_chart(symbol):
    try:
        df = yf.download(f'{symbol}-USD', period='6mo', interval='1d')
    except Exception as e:
        raise e

    df.reset_index(inplace=True)
    df = df.iloc[:-1]
    df['Date'] = df['Date'].map(mdates.date2num)
    ohlc = df[['Date', 'Open', 'High', 'Low', 'Close']]

    fig, ax = plt.subplots(figsize=(12, 8))
    candlestick_ohlc(ax, ohlc.values, width=0.8, colorup='g', colordown='r')

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    ax.grid(False)

    plt.tight_layout()

    fig.savefig(os.path.join(os.getcwd(), 'static/chart.png'), dpi=150, transparent=True)
    plt.close(fig)
