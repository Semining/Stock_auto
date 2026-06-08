import screener
import mailer


def main():
    print("Screening...")
    hits = screener.scan()

    if not hits:
        print("No stocks met conditions - skipping mail")
        return

    print(f"{len(hits)} stocks detected:")
    for s in hits:
        print(f"  {s['ticker']}  {s['price_change_pct']:+.2f}%  vol {s['vol_ratio']}x")

    mailer.send(hits)


if __name__ == "__main__":
    main()