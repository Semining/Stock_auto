import io
import urllib.request
import pandas as pd
import yfinance as yf
import config


def _get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    with urllib.request.urlopen(url, timeout=15) as resp:
        html = resp.read().decode("utf-8")
    tables = pd.read_html(io.StringIO(html))
    return tables[0]["Symbol"].tolist()


def _build_ticker_list():
    if config.SCAN_SP500:
        return _get_sp500_tickers()
    return config.WATCHLIST


def scan():
    tickers = _build_ticker_list()
    if not tickers:
        return []

    results = []
    data = yf.download(
        tickers,
        period="25d",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        progress=False,
        threads=True,
    )

def _fetch_news(ticker: str) -> list[dict]:
    try:
        t = yf.Ticker(ticker)
        news = t.news or []
        result = []
        for item in news[:5]:
            content = item.get("content", {})
            title = content.get("title", "")
            url = content.get("canonicalUrl", {}).get("url", "") or \
                  content.get("clickThroughUrl", {}).get("url", "")
            if title and url:
                result.append({"title": title, "url": url})
        return result
    except Exception:
        return []

    for ticker in tickers:
        try:
            df = data if len(tickers) == 1 else data[ticker]
            df = df.dropna(subset=["Close", "Volume"])
            if len(df) < 2:
                continue

            today = df.iloc[-1]
            prev = df.iloc[-2]
            avg_vol = df["Volume"].iloc[-21:-1].mean()

            price_change = (today["Close"] - prev["Close"]) / prev["Close"] * 100
            vol_ratio = today["Volume"] / avg_vol if avg_vol > 0 else 0

            hit_price = price_change >= config.PRICE_CHANGE_PCT
            hit_volume = vol_ratio >= config.VOLUME_SURGE_RATIO

            if hit_price or hit_volume:
                results.append({
                    "ticker": ticker,
                    "close": round(float(today["Close"]), 2),
                    "price_change_pct": round(float(price_change), 2),
                    "volume": int(today["Volume"]),
                    "vol_ratio": round(float(vol_ratio), 1),
                    "hit_price": hit_price,
                    "hit_volume": hit_volume,
                    "news": _fetch_news(ticker),
                })
        except Exception:
            continue

    results.sort(key=lambda x: x["price_change_pct"], reverse=True)
    return results