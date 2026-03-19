from groq import Groq
from config.keys import get_key, is_configured

MODEL = "llama-3.3-70b-versatile"

SYSTEM = """You are StockSense, an expert analyst focused exclusively on Indian stock markets (NSE/BSE).
You have deep knowledge of Nifty 50, Sensex, sectoral indices, SEBI regulations, FII/DII flows, RBI policy, and Indian macroeconomics.
When given stock data, analyze it with specific numbers. Structure responses with clear sections.
Only answer finance and investing questions. Politely decline everything else.
Never fabricate data. Use ₹ for all prices."""


def _client():
    return Groq(api_key=get_key())


def chat(messages: list) -> str:
    if not is_configured():
        return "⚠️ GROQ_API_KEY not set. Add it to your .env file and restart."
    try:
        res = _client().chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM}] + messages,
            temperature=0.4,
            max_tokens=1024,
        )
        return res.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "401" in err or "invalid_api_key" in err.lower():
            return "❌ Invalid Groq API key. Get one free at https://console.groq.com"
        if "429" in err or "rate" in err.lower():
            return "⏳ Rate limit hit. Please wait a moment."
        return f"❌ Error: {err}"


def stream(messages: list):
    if not is_configured():
        yield "⚠️ GROQ_API_KEY not set. Add it to your .env file and restart."
        return
    try:
        res = _client().chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM}] + messages,
            temperature=0.4,
            max_tokens=1024,
            stream=True,
        )
        for chunk in res:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except Exception as e:
        yield f"❌ Error: {str(e)}"
