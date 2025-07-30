[![Upload Python Package](https://github.com/jgwill/jgtapy/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jgwill/jgtapy/actions/workflows/python-publish.yml)

# jgtapy
Technical Indicators for the Pandas' Dataframes


Documentation: https://pandastechindicators.readthedocs.io/en/latest/


## Installation
```
pip install -U jgtapy
```

## Example
```
>>> import pandas as pd
>>> from jgtapy import Indicators
>>> df = pd.read_csv('EURUSD60.csv')
>>> i= Indicators(df)
>>> i.accelerator_oscillator(column_name='AC'
>>> i.fractals(column_name_high='fb', column_name_low='fs')
>>> i.fractals3(column_name_high='fb3', column_name_low='fs3')
>>> i.fractals5(column_name_high='fb5', column_name_low='fs5')
>>> ... 8,13,21,34,55,89
>>> i.sma()
>>> df = i.df
>>> df.tail()
            Date   Time     Open     High      Low    Close  Volume        AC       sma
3723  2019.09.20  16:00  1.10022  1.10105  1.10010  1.10070    2888 -0.001155  1.101296
3724  2019.09.20  17:00  1.10068  1.10193  1.10054  1.10184    6116 -0.000820  1.101158
3725  2019.09.20  18:00  1.10186  1.10194  1.10095  1.10144    3757 -0.000400  1.101056
3726  2019.09.20  19:00  1.10146  1.10215  1.10121  1.10188    3069  0.000022  1.101216
3727  2019.09.20  20:00  1.10184  1.10215  1.10147  1.10167    1224  0.000388  1.101506
```

## Available Indicators

1. Accelerator Oscillator (AC)
2. Accumulation/Distribution (A/D)
3. Alligator
4. Average True Range (ATR)
5. Awesome Oscillator (AO)
6. Bears Power
7. Bollinger Bands
8. Bulls Power
9. Commodity Channel Index (CCI)
10. DeMarker (DeM)
11. Exponential Moving Average (EMA)
12. Force Index (FRC)
13. Fractals (dimension 2,3,5,8,13,21,34,55,89)
14. Gator Oscillator
15. Ichimoku Kinko Hyo
16. Market Facilitation Index (BW MFI)
17. Momentum
18. Money Flow Index (MFI)
19. Moving Average Convergence/Divergence (MACD)
20. Simple Moving Average (SMA)
21. Smoothed Moving Average (SMMA)

## Detailed Documentation

For detailed documentation on the Alligator, Awesome Oscillator (AO), Accelerator Oscillator (AC), Fractals, and Market Facilitation Index (MFI) indicators, including descriptions and usage examples, please refer to the [INDICATORS.md](INDICATORS.md) file.

### Alligator 🐊

The Alligator indicator is a combination of three smoothed moving averages with different periods and shifts. It is used to identify trends and their direction. The three lines are called the Jaw, Teeth, and Lips. The implementation can be found in the `alligator` method in `jgtapy/indicators.py`.

### Awesome Oscillator (AO) 🌟

The Awesome Oscillator is a momentum indicator that compares the 5-period simple moving average (SMA) with the 34-period SMA. It helps to identify market momentum. The implementation can be found in the `awesome_oscillator` method in `jgtapy/indicators.py`.

### Accelerator Oscillator (AC) 🚀

The Accelerator Oscillator measures the acceleration or deceleration of the current market driving force. It is derived from the Awesome Oscillator by subtracting a 5-period SMA of the AO from the AO itself. The implementation can be found in the `accelerator_oscillator` method in `jgtapy/indicators.py`.

### Fractals 🌀

Fractals are used to identify potential reversal points in the market. They consist of a series of at least five bars, with the highest high in the middle and two lower highs on each side for a bullish fractal, or the lowest low in the middle and two higher lows on each side for a bearish fractal. The implementation can be found in the `fractals` method and its variations in `jgtapy/indicators.py`.

### Market Facilitation Index (MFI) 📈

The Market Facilitation Index measures the efficiency of price movement by comparing the range of price movement to the volume. It helps to identify potential market trends and reversals. The implementation can be found in the `bw_mfi` method in `jgtapy/indicators.py`.
