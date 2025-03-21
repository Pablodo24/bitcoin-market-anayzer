import ccxt
import pandas as pd
import ta
from fastapi import FastAPI
import uvicorn

# إنشاء API باستخدام FastAPI
app = FastAPI()

# تعريف Binance API
exchange = ccxt.binance()

# دالة لجلب بيانات السوق وتحليلها
def get_market_analysis():
    # جلب بيانات الشموع اليابانية لآخر 100 فترة
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # تحويل التوقيت إلى تاريخ
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # حساب المتوسطات المتحركة
    df['SMA_50'] = ta.trend.sma_indicator(df['close'], window=50)
    df['EMA_20'] = ta.trend.ema_indicator(df['close'], window=20)

    # حساب مؤشر القوة النسبية RSI
    df['RSI'] = ta.momentum.rsi(df['close'], window=14)

    # حساب MACD
    df['MACD'] = ta.trend.macd(df['close'])
    df['MACD_signal'] = ta.trend.macd_signal(df['close'])

    # منطق التوصيات
    latest_data = df.iloc[-1]  # آخر بيانات متاحة
    recommendation = "WAIT"  # الافتراضي: الانتظار

    if latest_data['RSI'] < 30 and latest_data['MACD'] > latest_data['MACD_signal'] and latest_data['close'] > latest_data['EMA_20']:
        recommendation = "BUY"
    elif latest_data['RSI'] > 70 and latest_data['MACD'] < latest_data['MACD_signal'] and latest_data['close'] < latest_data['EMA_20']:
        recommendation = "SELL"

    return {
        "current_price": latest_data['close'],
        "RSI": latest_data['RSI'],
        "MACD": latest_data['MACD'],
        "MACD_signal": latest_data['MACD_signal'],
        "EMA_20": latest_data['EMA_20'],
        "SMA_50": latest_data['SMA_50'],
        "recommendation": recommendation
    }

# إنشاء API لاسترجاع البيانات
@app.get("/analysis")
def get_analysis():
    return get_market_analysis()

# تشغيل الخادم
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
