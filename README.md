# StockSense 📈

An AI-powered Indian stock market analyst built with Python, Streamlit, and Groq's LLaMA 3.3 70B. Ask questions about NSE/BSE stocks in plain English and get real-time analysis, technical indicators, and interactive charts — all in one app.

---

## What it does

StockSense connects live NSE/BSE market data with a conversational AI that understands Indian markets. Instead of manually reading charts or calculating RSI values, you just ask — *"Is RELIANCE overbought right now?"* or *"Compare TCS vs Infosys fundamentals"* — and the AI responds with actual numbers pulled from the market in real time.

The app has four views:

- **Chat** — the main interface. Full conversation history with streaming AI responses. Automatically loads live data for your watchlist stocks as context before every message, so the AI always knows current prices and indicators without you having to paste anything.
- **Markets** — live Nifty 50, Sensex, and Bank Nifty index cards, plus a quick stock lookup with price metrics and fundamentals table.
- **Charts** — interactive candlestick, line, and MACD charts with toggleable Bollinger Bands and EMA overlays.
- **Compare** — side-by-side comparison of up to 6 stocks with normalised performance charts, cumulative returns, and a correlation heatmap.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | Streamlit |
| AI Model | Groq — LLaMA 3.3 70B (llama-3.3-70b-versatile) |
| Market Data | yfinance (Yahoo Finance) |
| Charts | Plotly |
| Language | Python 3.10+ |
| Exchange Support | NSE (.NS) and BSE (.BO) |
| API Key Management | python-dotenv |

---

## Project Structure

```
stocksense/
├── app.py                  # Entry point — 15 lines
├── .env                    # Your API key lives here (never committed)
├── .env.example            # Template to copy from
├── .gitignore
├── requirements.txt
│
├── config/
│   ├── keys.py             # Loads GROQ_API_KEY from .env
│   └── styles.py           # All CSS injected once at startup
│
├── views/
│   ├── sidebar.py          # Nav, watchlist, API status
│   ├── chat.py             # Chatbot — primary view
│   ├── markets.py          # Index cards + stock lookup
│   ├── charts.py           # Technical chart viewer
│   └── compare.py          # Multi-stock comparison
│
└── utils/
    ├── ai.py               # All Groq API calls (chat + stream)
    ├── data.py             # yfinance fetching + indicators
    └── charts.py           # Plotly figure builders
```

The design principle is simple — each file has one job. `app.py` only wires things together. `config/keys.py` is the only file that touches the API key. `utils/ai.py` is the only file that talks to Groq. If you need to change something, you always know exactly which file to open.

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/stocksense.git
cd stocksense
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Set up your API key**

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your actual key:

```
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free key at [console.groq.com](https://console.groq.com) — no credit card required.

**4. Run the app**

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## How to Use

### Chat View
Type any question about Indian stocks in the input box and hit Send. Add stocks to your watchlist in the sidebar — the AI will automatically have their live data as context for every message.

```
"Analyse HDFC Bank for me"
"Is RELIANCE overbought based on RSI?"
"Compare TCS vs Infosys — which is better value?"
"What does a Bank Nifty drop mean for ICICI Bank?"
"If I had ₹50,000 to invest in IT stocks, what would you suggest?"
```

### Charts View
Enter any NSE symbol and choose between Candlestick, Line, or MACD chart. Toggle Bollinger Bands and EMA lines on or off. Ask the AI to interpret what it sees.

### Compare View
Click a sector preset (Banking, IT, Auto, Pharma, Energy) or type symbols manually. Switch between normalised performance, cumulative returns, and raw price views. The correlation heatmap shows how closely the stocks move together.

---

## NSE Symbols Reference

Use standard NSE symbols — the app appends `.NS` automatically:

```
RELIANCE   TCS        INFY       HDFCBANK   ICICIBANK
SBIN       WIPRO      TATAMOTORS BAJFINANCE ADANIENT
ITC        KOTAKBANK  AXISBANK   SUNPHARMA  MARUTI
NTPC       POWERGRID  ONGC       TATASTEEL  BHARTIARTL
```

For indices, the app fetches Nifty 50 (`^NSEI`), Sensex (`^BSESN`), and Bank Nifty (`^NSEBANK`) automatically on the Markets view.

---

## Technical Indicators

The app computes five indicators locally on every stock fetch:

| Indicator | Columns | Parameters |
|---|---|---|
| Exponential Moving Average | EMA20, EMA50 | 20-day, 50-day |
| Bollinger Bands | BB_up, BB_dn, BB_mid | 20-day SMA ± 2σ |
| RSI | RSI | 14-day |
| MACD | MACD, MACD_s, MACD_h | 12/26/9 |
| Volume MA | VolMA | 20-day |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Your Groq API key from console.groq.com |

**Important:** Never commit your `.env` file. It is already listed in `.gitignore`.

---

## Dependencies

```
streamlit>=1.32.0
groq>=0.9.0
yfinance>=0.2.36
plotly>=5.20.0
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
```

---

## Known Limitations

- **Data is delayed ~15 minutes** — Yahoo Finance is not a real-time feed. Do not use this for live trading decisions.
- **Daily candles only** — no intraday data. The minimum chart granularity is one bar per day.
- **No F&O data** — futures and options chains are not available through yfinance.
- **Groq free tier rate limits** — if you hit a 429 error, wait a few seconds and retry. The free tier is generous enough for normal use.
- **Max 6 stocks in Compare** — enforced to keep charts readable.

---

## Possible Extensions

If you want to take this further:

- **Add authentication** — Streamlit has built-in auth support for multi-user deployments
- **Swap data provider** — replace `utils/data.py`'s fetch functions with Zerodha Kite or Upstox for real-time data; the rest of the app stays the same
- **Add a portfolio tracker** — store buy prices in session state and calculate P&L against live prices
- **Export reports** — use reportlab or python-docx to generate PDF/Word summaries of any stock analysis
- **Deploy to cloud** — works out of the box on Streamlit Community Cloud; just add `GROQ_API_KEY` as a secret in the dashboard

---

## License

MIT License — free to use, modify, and distribute.

---

*Built with Streamlit · Groq · yfinance · Plotly*
