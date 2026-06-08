import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
import config


def _build_html(stocks):
    rows = ""
    for s in stocks:
        triggers = []
        if s["hit_price"]:
            triggers.append(f"rate {s['price_change_pct']:+.2f}%")
        if s["hit_volume"]:
            triggers.append(f"vol {s['vol_ratio']}x")
        trigger_str = " / ".join(triggers)
        color = "#d32f2f" if s["price_change_pct"] >= 0 else "#1565c0"
        rows += (
            f"<tr>"
            f"<td style='padding:8px 12px;font-weight:bold'>{s['ticker']}</td>"
            f"<td style='padding:8px 12px;text-align:right'>${s['close']:,.2f}</td>"
            f"<td style='padding:8px 12px;text-align:right;color:{color}'>{s['price_change_pct']:+.2f}%</td>"
            f"<td style='padding:8px 12px;text-align:right'>{s['vol_ratio']}x</td>"
            f"<td style='padding:8px 12px'>{trigger_str}</td>"
            f"</tr>"
        )

    return (
        f"<html><body style='font-family:Arial,sans-serif;color:#333'>"
        f"<h2 style='color:#1a237e'>US Stock Surge Alert — {date.today()}</h2>"
        f"<p>The following stocks met surge conditions.</p>"
        f"<table border='1' cellspacing='0' cellpadding='0' style='border-collapse:collapse;width:100%;max-width:700px'>"
        f"<thead style='background:#1a237e;color:white'>"
        f"<tr><th style='padding:10px 12px'>Ticker</th><th style='padding:10px 12px'>Price</th>"
        f"<th style='padding:10px 12px'>Change</th><th style='padding:10px 12px'>Vol Ratio</th>"
        f"<th style='padding:10px 12px'>Trigger</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        f"<p style='color:#888;font-size:12px'>Source: Yahoo Finance</p>"
        f"</body></html>"
    )


def send(stocks):
    subject = f"[Stock Surge Alert] {date.today()} — {len(stocks)} stocks detected"
    html = _build_html(stocks)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = config.GMAIL_USER
    msg["To"] = ", ".join(config.RECIPIENTS)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
        server.sendmail(config.GMAIL_USER, config.RECIPIENTS, msg.as_string())

    print(f"Mail sent to {config.RECIPIENTS}")