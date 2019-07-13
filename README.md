# CryptoAnalyzer

## Requirements
- Python 3.7
- Pandas 0.24.2
- Tabulate 0.8.3

## How to run
- Configure **configurations.yml** as required. Make sure the **api.key** attribute is set.
- Execute ```python run.py```.

## Sample run output
```
nader$ python3 run.py
[2019-07-13 03:02:25] Starting CryptoAnalyzer..
[2019-07-13 03:02:25] Loading data from API..
[2019-07-13 03:02:29] Loaded data successfully.
[2019-07-13 03:02:30] Saved raw CSV data to data/raw/BTC_USD_20190713.csv
[2019-07-13 03:02:30] Computing weekly mean prices..
[2019-07-13 03:02:30] Saved weekly means CSV data to data/analysis/BTC_USD_weekly_means_20190713.csv
[2019-07-13 03:02:30] Finding the first 1 week(s) with highest relative span values..
[2019-07-13 03:02:30] The week(s) with highest relative span values are as follows, in descending order:
+---------------------+-----------------+
| week_start          |   relative_span |
|---------------------+-----------------|
| 2018-02-05 00:00:00 |        0.473682 |
+---------------------+-----------------+
[2019-07-13 03:02:30] Done. Exiting..
```
