#!/usr/bin/env python3
"""btc-cent-forecast-01 entry: 4-hour-ahead BTC price forecast.

Model: persistence with transient-spike rejection.

The case gives 4,320 one-minute closes of cbBTC/USDC from one Orca pool.
A single close can sit far off the local level for a minute: one unusually
large trade in that pool moves its price for a moment (the kit's RULES.txt
says so), then the price reverts. Guessing that dislocated close as the
price 4 hours later costs the whole size of the dislocation, so the program
guards against it:

  * level = median of the last 15 closes (robust to a one-minute spike);
  * if the checkpoint close sits further from that level than
    max($150, 4 x the last hour's 1-minute return volatility), the close
    is treated as a transient dislocation and the level is forecast;
  * otherwise the checkpoint close itself is forecast (persistence).

In normal conditions this is exactly persistence, the honest median
forecast for a near-random-walk price; it only overrides persistence on a
clear dislocation. No momentum or mean-reversion term is fitted: on the
kit's practice window both made the 4-hour error worse.

Backtest on the kit's practice window (66 sub-checkpoints at 4-hour
spacing, Nov 7-11): persistence mean absolute error 42,654 cents, this
program 36,054 cents (ratio 0.85). The whole gain is one genuine
dislocation: a $1,475 one-minute pool drop that reverted within minutes
(the median level predicted the 4-hour price to within $15, persistence
missed by $1,104). The filter fired on no other checkpoint, so outside
dislocations the program is persistence and its downside is bounded.

Deterministic, standard library only, no network, no randomness.
Reads $MAKEFUN_INPUT_DIR (else /input), writes $MAKEFUN_OUTPUT_DIR
(else /output), one {"forecasts": [{"case": id, "price": x}]} file per
<input>/<id>.in case, price rounded to the grid's 5 decimals.
"""

import json
import math
import os
import statistics
import sys

INPUT_DIR = os.environ.get("MAKEFUN_INPUT_DIR") or "/input"
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

MIN_PRICE = 0.00001
MAX_PRICE = 9_999_999.99999

# A dislocation must clear both an absolute floor ($150, about 0.2% of a
# ~$75k BTC) and 4 standard deviations of the last hour's 1-minute
# returns, so ordinary volatility never triggers the override.
ABS_FLOOR = 150.0
VOL_MULTIPLE = 4.0
LEVEL_WINDOW = 15
VOL_WINDOW = 60


def price5(x):
    """x kept on the grid's 5 decimals and inside (0, 10,000,000)."""
    return round(min(MAX_PRICE, max(MIN_PRICE, x)) * 1e5) / 1e5


def forecast(prices):
    """Forecast the price 240 minutes after the last close in `prices`."""
    if not prices:
        raise ValueError("market has no prices")
    last = prices[-1]
    if not isinstance(last, (int, float)) or not math.isfinite(last):
        raise ValueError("last price is not a finite number")

    level = statistics.median(prices[-LEVEL_WINDOW:])
    n = min(VOL_WINDOW, len(prices) - 1)
    if n >= 2:
        rets = [math.log(prices[j] / prices[j - 1])
                for j in range(len(prices) - n, len(prices))
                if prices[j - 1] > 0 and prices[j] > 0]
        if len(rets) >= 2:
            mu = sum(rets) / len(rets)
            vol = math.sqrt(sum((r - mu) ** 2 for r in rets) / len(rets))
        else:
            vol = 0.0
    else:
        vol = 0.0

    threshold = max(ABS_FLOOR, VOL_MULTIPLE * vol * last)
    guess = level if abs(last - level) > threshold else last
    return price5(guess)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    inputs = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".in"))
    for name in inputs:
        case_id = name[: -len(".in")]
        with open(os.path.join(INPUT_DIR, name), "r", encoding="utf-8") as fh:
            case = json.load(fh)
        markets = case.get("markets")
        if not isinstance(markets, list) or len(markets) != 1:
            raise ValueError(f"{name} does not hold exactly one market")
        guess = forecast(markets[0]["prices"])
        out = {"forecasts": [{"case": case_id, "price": guess}]}
        with open(os.path.join(OUTPUT_DIR, case_id + ".out"),
                  "w", encoding="utf-8") as fh:
            fh.write(json.dumps(out) + "\n")


if __name__ == "__main__":
    main()
