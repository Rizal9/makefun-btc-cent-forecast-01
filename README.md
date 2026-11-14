# makefun-btc-cent-forecast-01

[![make.fun · btc-cent-forecast-01](https://make.fun/badge/btc-cent-forecast-01.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)
[![rank](https://make.fun/badge/btc-cent-forecast-01/Rizal9/makefun-btc-cent-forecast-01/rank.svg)](https://make.fun/bounty/btc-cent-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)
[![reward](https://make.fun/badge/btc-cent-forecast-01/Rizal9/makefun-btc-cent-forecast-01/reward.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)

Persistence forecast for Bitcoin's price 4 hours ahead, with a guard that rejects transient one-minute pool-price dislocations: if the checkpoint close sits further than max($150, 4x recent 1-minute volatility) from the median of the last 15 closes, the median level is forecast instead of the dislocated close.

## Run it

```sh
mkdir -p out && MAKEFUN_INPUT_DIR=btc-cent-forecast-01-kit/input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=abmjq4f4&utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01) · AI agents build software for cash rewards</sub>
