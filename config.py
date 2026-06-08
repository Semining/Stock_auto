import os
import yaml
from dotenv import load_dotenv

load_dotenv()

with open("config.yaml", "r", encoding="utf-8") as f:
    _cfg = yaml.safe_load(f)

WATCHLIST = _cfg.get("watchlist", [])
SCAN_SP500 = _cfg.get("scan_sp500", False)
PRICE_CHANGE_PCT = _cfg["thresholds"]["price_change_pct"]
VOLUME_SURGE_RATIO = _cfg["thresholds"]["volume_surge_ratio"]
RECIPIENTS = _cfg.get("recipients", [])

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]

