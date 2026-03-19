import yfinance as yf
import pandas as pd
import numpy as np

INDICES = {
    "Nifty 50":   "^NSEI",
    "Sensex":     "^BSESN",
    "Bank Nifty": "^NSEBANK",
}

TOP_STOCKS = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
    "SBIN", "HINDUNILVR", "BHARTIARTL", "ITC", "KOTAKBANK",
    "LT", "AXISBANK", "ASIANPAINT", "MARUTI", "BAJFINANCE",
    "WIPRO", "HCLTECH", "TITAN", "SUNPHARMA", "TATAMOTORS",
    "ADANIENT", "NTPC", "POWERGRID", "ONGC", "TATASTEEL",
]


def to_ticker(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if symbol.startswith("^") or symbol.endswith((".NS", ".BO")):
        return symbol
    return symbol + ".NS"


def fetch(symbol: str, period: str = "6mo"):
    ticker = to_ticker(symbol)
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        if hist.empty:
            t = yf.Ticker(symbol.upper() + ".BO")
            hist = t.history(period=period)
        if hist.empty:
            return None, None
        return t.info, hist
    except Exception:
        return None, None


def fetch_indices() -> dict:
    result = {}
    for name, sym in INDICES.items():
        try:
            t = yf.Ticker(sym)
            h = t.history(period="2d")
            if len(h) >= 2:
                cur, prev = h["Close"].iloc[-1], h["Close"].iloc[-2]
                result[name] = {"price": cur, "chg": (cur / prev - 1) * 100}
        except Exception:
            pass
    return result


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    c = df["Close"]

    df["EMA20"] = c.ewm(span=20, adjust=False).mean()
    df["EMA50"] = c.ewm(span=50, adjust=False).mean()

    sma, std = c.rolling(20).mean(), c.rolling(20).std()
    df["BB_up"]  = sma + 2 * std
    df["BB_dn"]  = sma - 2 * std
    df["BB_mid"] = sma

    delta = c.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    df["RSI"] = 100 - 100 / (1 + gain / loss.replace(0, np.nan))

    e12, e26     = c.ewm(span=12, adjust=False).mean(), c.ewm(span=26, adjust=False).mean()
    df["MACD"]   = e12 - e26
    df["MACD_s"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_h"] = df["MACD"] - df["MACD_s"]

    df["VolMA"] = df["Volume"].rolling(20).mean()
    return df


def build_context(symbol: str, info: dict, df: pd.DataFrame) -> str:
    c = df["Close"]
    cur   = c.iloc[-1]
    prev  = c.iloc[-2]  if len(c) > 1  else cur
    w_ago = c.iloc[-5]  if len(c) > 5  else cur
    m_ago = c.iloc[-21] if len(c) > 21 else cur

    lines = [
        f"STOCK: {symbol} — {info.get('longName', symbol)}",
        f"Sector: {info.get('sector','N/A')} | Industry: {info.get('industry','N/A')}",
        "",
        "PRICE:",
        f"  Current ₹{cur:.2f} | Day {(cur/prev-1)*100:+.2f}% | Week {(cur/w_ago-1)*100:+.2f}% | Month {(cur/m_ago-1)*100:+.2f}%",
        f"  52W High ₹{info.get('fiftyTwoWeekHigh','N/A')} | 52W Low ₹{info.get('fiftyTwoWeekLow','N/A')}",
        "",
        "FUNDAMENTALS:",
        f"  Market Cap: {info.get('marketCap','N/A')} | P/E: {info.get('trailingPE','N/A')} | Fwd P/E: {info.get('forwardPE','N/A')}",
        f"  EPS: {info.get('trailingEps','N/A')} | Revenue: {info.get('totalRevenue','N/A')} | Margin: {info.get('profitMargins','N/A')}",
        f"  Beta: {info.get('beta','N/A')} | Div Yield: {info.get('dividendYield','N/A')}",
        f"  50D MA: {info.get('fiftyDayAverage','N/A')} | 200D MA: {info.get('twoHundredDayAverage','N/A')}",
    ]
    if "RSI" in df.columns:
        lines.append(f"  RSI(14): {df['RSI'].iloc[-1]:.1f}")
    if "MACD" in df.columns:
        lines.append(f"  MACD: {df['MACD'].iloc[-1]:.3f} | Signal: {df['MACD_s'].iloc[-1]:.3f}")

    return "\n".join(lines)


def fmt_crore(n):
    try:
        n = float(n)
        if n >= 1e7:  return f"₹{n/1e7:.1f} Cr"
        if n >= 1e5:  return f"₹{n/1e5:.1f} L"
        return f"₹{n:,.0f}"
    except Exception:
        return str(n)
