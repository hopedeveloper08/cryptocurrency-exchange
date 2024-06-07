from ta.trend import SMAIndicator, EMAIndicator, MACD, IchimokuIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands
import yfinance as yf


def indicators_result(symbol):
    try:
        df = yf.download(f'{symbol}-USD', period='1y', interval='1d').iloc[:-1]
    except Exception as e:
        raise e

    signals = {
        'Ichimoku': ichimoku_result(df),
        'SMA': sma_result(df),
        'EMA': ema_result(df),
        'MACD': macd_result(df),
        'RSI': rsi_result(df),
        'Stochastic': stochastic_result(df),
        'BollingerBands': bb_result(df),
    }
    return signals


def sma_result(df):
    sma100 = SMAIndicator(close=df['Close'], window=100)
    sma200 = SMAIndicator(close=df['Close'], window=200)

    is_buy = (
            (sma100.sma_indicator().iloc[-1] - sma200.sma_indicator().iloc[-1]) > 0 > (sma100.sma_indicator().iloc[-2] - sma200.sma_indicator().iloc[-2])
    )
    is_sell = (
            (sma100.sma_indicator().iloc[-1] - sma200.sma_indicator().iloc[-1]) < 0 < (sma100.sma_indicator().iloc[-2] - sma200.sma_indicator().iloc[-2])
    )
    return {'is_buy': is_buy, 'is_sell': is_sell}


def ema_result(df):
    ema100 = EMAIndicator(close=df['Close'], window=100)
    ema200 = EMAIndicator(close=df['Close'], window=200)

    is_buy = (
            (ema100.ema_indicator().iloc[-1] - ema200.ema_indicator().iloc[-1]) > 0 > (ema100.ema_indicator().iloc[-2] - ema200.ema_indicator().iloc[-2])
    )
    is_sell = (
            (ema100.ema_indicator().iloc[-1] - ema200.ema_indicator().iloc[-1]) < 0 < (ema100.ema_indicator().iloc[-2] - ema200.ema_indicator().iloc[-2])
    )
    return {'is_buy': is_buy, 'is_sell': is_sell}


def ichimoku_result(df):
    ichimoku = IchimokuIndicator(high=df['High'], low=df['Low'], window1=9, window2=26, window3=52, visual=True)
    senkou_a = ichimoku.ichimoku_a().values
    senkou_b = ichimoku.ichimoku_b().values

    is_buy = (
            df['Close'].iloc[-26] > max(senkou_a[-1], senkou_b[-1]) and
            max(senkou_a[-2], senkou_b[-2]) > df['Close'].iloc[-27]
    )
    is_sell = (
            df['Close'].iloc[-26] < max(senkou_a[-1], senkou_b[-1]) and
            max(senkou_a[-2], senkou_b[-2]) < df['Close'].iloc[-27]
    )
    return {'is_buy': is_buy, 'is_sell': is_sell}


def macd_result(df):
    macd = MACD(close=df['Close'])
    macd_line = macd.macd()
    signal_line = macd.macd_signal()

    is_buy = (macd_line[-1] - signal_line[-1]) > 0 > (macd_line[-2] - signal_line[-2])
    is_sell = (macd_line[-1] - signal_line[-1]) < 0 < (macd_line[-2] - signal_line[-2])
    return {'is_buy': is_buy, 'is_sell': is_sell}


def rsi_result(df):
    rsi = RSIIndicator(close=df['Close'], window=14)
    df['RSI'] = rsi.rsi()
    is_buy = df['RSI'].iloc[-1] < 30
    is_sell = df['RSI'].iloc[-1] > 70
    return {'is_buy': is_buy, 'is_sell': is_sell}


def stochastic_result(df):
    stochastic = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=14, smooth_window=3)
    df['Stochastic'] = stochastic.stoch()
    df['Stochastic_Signal'] = stochastic.stoch_signal()

    is_buy = 20 > df['Stochastic'].iloc[-1] > df['Stochastic_Signal'].iloc[-1]
    is_sell = 80 < df['Stochastic'].iloc[-1] < df['Stochastic_Signal'].iloc[-1]
    return {'is_buy': is_buy, 'is_sell': is_sell}


def bb_result(df):
    bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()

    is_buy = df['Close'].iloc[-1] < df['BB_Low'].iloc[-1]
    is_sell = df['Close'].iloc[-1] > df['BB_High'].iloc[-1]
    return {'is_buy': is_buy, 'is_sell': is_sell}
