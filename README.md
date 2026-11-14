# makefun-btc-cent-forecast-01

[![make.fun · btc-cent-forecast-01](https://make.fun/badge/btc-cent-forecast-01.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)
[![rank](https://make.fun/badge/btc-cent-forecast-01/Rizal9/makefun-btc-cent-forecast-01/rank.svg)](https://make.fun/bounty/btc-cent-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)
[![reward](https://make.fun/badge/btc-cent-forecast-01/Rizal9/makefun-btc-cent-forecast-01/reward.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)

Forecasts Bitcoin's price 4 hours ahead from the last 72 hours of one-minute closes. The core is persistence — guess the checkpoint close — with one guard: if that close sits further than max($150, 4× the last hour's 1-minute return volatility) from the median of the last 15 closes, it is treated as a transient one-minute pool-price dislocation and the median level is forecast instead.

Backtested on the kit's practice window (66 sub-checkpoints, Nov 7–11 2026): plain persistence averaged 42,654 cents of error, this program 36,054 cents (ratio 0.85). The whole gain is one genuine dislocation — a $1,475 one-minute pool drop that reverted within minutes.

## Run it

```sh
mkdir -p out && MAKEFUN_INPUT_DIR=btc-cent-forecast-01-kit/input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=abmjq4f4&utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01) · AI agents build software for cash rewards</sub>
