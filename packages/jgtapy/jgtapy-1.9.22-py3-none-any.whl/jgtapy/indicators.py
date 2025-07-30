import pandas as pd

import numpy as np

from .utils import calculate_ao, calculate_sma, calculate_smma, mad

__version__ = "1.9.22"


class Indicators:
    """
    Add technical indicators data to a pandas data frame

    Example:
    ~~~~~~~~
        >>> import pandas as pd
        >>> from jgtapy import Indicators
        >>> df = pd.read_csv('EURUSD60.csv')
        >>> i= Indicators(df)
        >>> i.accelerator_oscillator(column_name='AC')
        >>> i.sma()
        >>> df = i.df
        >>> df.tail()
                    Date   Time     Open     High      Low    Close  Volume        AC       sma
        3723  2019.09.20  16:00  1.10022  1.10105  1.10010  1.10070    2888 -0.001155  1.101296
        3724  2019.09.20  17:00  1.10068  1.10193  1.10054  1.10184    6116 -0.000820  1.101158
        3725  2019.09.20  18:00  1.10186  1.10194  1.10095  1.10144    3757 -0.000400  1.101056
        3726  2019.09.20  19:00  1.10146  1.10215  1.10121  1.10188    3069  0.000022  1.101216
        3727  2019.09.20  20:00  1.10184  1.10215  1.10147  1.10167    1224  0.000388  1.101506
    """
    index_column_name = 'Date'
    def __init__(
        self,
        df,
        open_col="Open",
        high_col="High",
        low_col="Low",
        close_col="Close",
        volume_col="Volume",
        median_col = "Median",
        index_column_name = 'Date'
    ):
        """
        Initiate Indicators object

        :param pandas data frame df: Should contain OHLC columns and Volume column
        :param str open_col: Name of Open column in df
        :param str high_col: Name of High column in df
        :param str low_col: Name of Low column in df
        :param str close_col: Name of Close column in df
        :param str volume_col: Name of Volume column in df. This column is optional
            and require only if indicator use this data.
        :param str median_col: Name of Median column in df. This column is optional
        :param str index_column_name: Name of index column in df. Default is 'Date'
        """
        self.index_column_name = index_column_name
        try:
            # Check if 'Date' is the index column
            if df.index.name == self.index_column_name:
                # Reset the index to remove 'Date' as the index column
                df.reset_index(inplace=True)
        except Exception:
            pass
        self.df = df
        self._columns = {
            "Open": open_col,
            "High": high_col,
            "Low": low_col,
            "Close": close_col,
            "Volume": volume_col,
            "Median": median_col
        }

    def sma(self, period=5, column_name="sma", apply_to="Close"):
        """
        Simple Moving Average (SMA)
        ---------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/moving_average#simple_moving_average

            >>> Indicators.sma(period=5, column_name='sma', apply_to='Close')

            :param int period: the number of calculation periods, default: 5
            :param str column_name: Column name, default: sma
            :param str apply_to: Which column use for calculation.
                Can be *"Open"*, *"High"*, *"Low"* and *"Close"*.
                **Default**: Close
            :return: None

        """
        calculate_sma(self.df, period, column_name, apply_to)

    def smma(self, period=5, column_name="smma", apply_to="Close"):
        """
        Smoothed Moving Average (SMMA)
        ---------------------
            https://www.metatrader4.com/ru/trading-platform/help/analytics/tech_indicators/moving_average#smoothed_moving_average

            >>> Indicators.smma(period=5, column_name='smma', apply_to='Close')

            :param int period: the number of calculation periods, default: 5
            :param str column_name: Column name, default: smma
            :param str apply_to: Which column use for calculation.
                Can be *"Open"*, *"High"*, *"Low"* and *"Close"*.
                **Default**: Close
            :return: None

        """
        df_smma = calculate_smma(self.df, period, column_name, apply_to)
        self.df = self.df.merge(df_smma, left_index=True, right_index=True)

    def ema(self, period=5, column_name="ema", apply_to="Close"):
        """
        Exponential Moving Average (EMA)
        ---------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/moving_average#exponential_moving_average

            >>> Indicators.ema(period=5, column_name='ema', apply_to='Close')

            :param int period: the number of calculation periods, default: 5
            :param str column_name: Column name, default: ema
            :param str apply_to: Which column use for calculation.
                Can be *"Open"*, *"High"*, *"Low"* and *"Close"*.
                **Default**: Close
            :return: None

        """
        self.df[column_name] = (
            self.df[self._columns[apply_to]].ewm(span=period, adjust=False).mean()
        )

    def awesome_oscillator(self, column_name="ao"):
        """
        Awesome Oscillator (AO)
        -----------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/awesome_oscillator

            >>> Indicators.awesome_oscillator(column_name='ao')

            :param str column_name: Column name, default: ao
            :return: None
        """
        # Data frame for storing temporary data
        df_tmp = pd.DataFrame()
        df_tmp["High"] = self.df[self._columns["High"]]
        df_tmp["Low"] = self.df[self._columns["Low"]]

        # Calculate Awesome Oscillator
        calculate_ao(df_tmp, column_name)
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def ao_ac_oscillator(self, column_name_ao="ao",column_name_ac="ac"):
        """
        Awesome Oscillator (AO) and Accelerator Oscillator (AC)
        -----------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/awesome_oscillator

            >>> Indicators.ao_ac_oscillator(column_name_ao='ao',column_name_ac='ac')

            :param str column_name_ao: Column name, default: ao
            :param str column_name_ac: Column name, default: ac
            :return: None
        """
        # Data frame for storing temporary data
        df_tmp = pd.DataFrame()
        df_tmp["High"] = self.df[self._columns["High"]]
        df_tmp["Low"] = self.df[self._columns["Low"]]

        # Calculate Awesome Oscillator
        calculate_ao(df_tmp, column_name_ao)

        df_tmp = df_tmp[[column_name_ao]]

        #@State At this point we have a column named ao that the AC REquires and already have the df_tmp it also has

        # Calculate SMA for Awesome Oscillator
        calculate_sma(df_tmp, 5, "sma_ao", "ao")

        # Calculate Accelerator Oscillator
        df_tmp[column_name_ac] = df_tmp["ao"] - df_tmp["sma_ao"]

        df_tmp = df_tmp[[column_name_ao,column_name_ac]]

        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)


    def accelerator_oscillator(self, column_name="ac"):
        """
        Accelerator Oscillator (AC)
        -----------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/accelerator_decelerator

            >>> Indicators.accelerator_oscillator(column_name='ac')

            :param str column_name: Column name, default: ac
            :return: None
        """
        pass
        # Data frame for storing temporary data
        df_tmp = pd.DataFrame()
        df_tmp["High"] = self.df[self._columns["High"]]
        df_tmp["Low"] = self.df[self._columns["Low"]]

        # Calculate Awesome Oscillator
        calculate_ao(df_tmp, "ao")

        # Calculate SMA for Awesome Oscillator
        calculate_sma(df_tmp, 5, "sma_ao", "ao")

        # Calculate Accelerator Oscillator
        df_tmp[column_name] = df_tmp["ao"] - df_tmp["sma_ao"]
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def accumulation_distribution(self, column_name="a/d"):
        """
        Accumulation/Distribution (A/D)
        ---------------------

            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/accumulation_distribution

            >>> Indicators.accumulation_distribution(column_name='a/d')

            :param str column_name: Column name, default: a/d
            :return: None

        """
        # Temporary df
        df_tmp = pd.DataFrame()
        df_tmp["close"] = self.df[self._columns["Close"]]
        df_tmp["high"] = self.df[self._columns["High"]]
        df_tmp["low"] = self.df[self._columns["Low"]]
        df_tmp["volume"] = self.df[self._columns["Volume"]]

        df_tmp["calc"] = (
            ((df_tmp["close"] - df_tmp["low"]) - (df_tmp["high"] - df_tmp["close"]))
            * df_tmp["volume"]
            / (df_tmp["high"] - df_tmp["low"])
        )

        df_tmp[column_name] = df_tmp["calc"].explode().sum()
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def alligator(
        self,
        period_jaws=13,
        period_teeth=8,
        period_lips=5,
        shift_jaws=8,
        shift_teeth=5,
        shift_lips=3,
        column_name_jaws="alligator_jaws",
        column_name_teeth="alligator_teeth",
        column_name_lips="alligator_lips",
    ):
        """
        Alligator
        ------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/alligator

            >>> Indicators.alligator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_jaws='alligator_jaw', column_name_teeth='alligator_teeth', column_name_lips='alligator_lips')

            :param int period_jaws: Period for Alligator' Jaws, default: 13
            :param int period_teeth: Period for Alligator' Teeth, default: 8
            :param int period_lips: Period for Alligator' Lips, default: 5
            :param int shift_jaws: Period for Alligator' Jaws, default: 8
            :param int shift_teeth: Period for Alligator' Teeth, default: 5
            :param int shift_lips: Period for Alligator' Lips, default: 3
            :param str column_name_jaws: Column Name for Alligator' Jaws, default: alligator_jaws
            :param str column_name_teeth: Column Name for Alligator' Teeth, default: alligator_teeth
            :param str column_name_lips: Column Name for Alligator' Lips, default: alligator_lips
            :return: None
        """
        median_col = self._columns["Median"]
        if median_col not in self.df.columns:
            df_median = self.df[[self._columns["High"], self._columns["Low"]]]
            df_median = self.df[[self._columns["High"], self._columns["Low"], self._columns["Median"]]]
        else:
            df_median = self.df[[self._columns["High"], self._columns["Low"], self._columns["Median"]]]

        df_j = calculate_smma(df_median, period_jaws, column_name_jaws, median_col)
        df_t = calculate_smma(df_median, period_teeth, column_name_teeth, median_col)
        df_l = calculate_smma(df_median, period_lips, column_name_lips, median_col)

        # Shift SMMAs
        df_j[column_name_jaws] = df_j[column_name_jaws].shift(shift_jaws)
        df_t[column_name_teeth] = df_t[column_name_teeth].shift(shift_teeth)
        df_l[column_name_lips] = df_l[column_name_lips].shift(shift_lips)

        self.df = self.df.merge(df_j, left_index=True, right_index=True)
        self.df = self.df.merge(df_t, left_index=True, right_index=True)
        self.df = self.df.merge(df_l, left_index=True, right_index=True)

    def atr(self, period=14, column_name="atr"):
        """
        Average True Range (ATR)
        ------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/average_true_range

            >>> Indicators.atr(period=14, column_name='atr')

            :param int period: Period, default: 14
            :param str column_name: Column name, default: atr
            :return: None
        """
        df_tmp = self.df[
            [self._columns["High"], self._columns["Low"], self._columns["Close"]]
        ]
        df_tmp = df_tmp.assign(
            max_min=df_tmp[self._columns["High"]] - df_tmp[self._columns["Low"]]
        )
        df_tmp["prev_close-high"] = (
            df_tmp[self._columns["Close"]].shift(1) - df_tmp[self._columns["High"]]
        )
        df_tmp["prev_close-min"] = (
            df_tmp[self._columns["Close"]].shift(1) - df_tmp[self._columns["Low"]]
        )
        df_tmp["max_val"] = df_tmp.apply(
            lambda x: max([x["max_min"], x["prev_close-high"], x["prev_close-min"]]),
            axis=1,
        )
        calculate_sma(df_tmp, period, column_name, "max_val")
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def bears_power(self, period=13, column_name="bears_power"):
        """
        Bears Power
        ------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/bears_power

            >>> Indicators.bears_power(period=13, column_name='bears_power')

            :param int period: Period, default: 13
            :param str column_name: Column name, default: bears_power
            :return: None
        """
        df_tmp = self.df[[self._columns["Close"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            ema=df_tmp[self._columns["Close"]].ewm(span=period, adjust=False).mean()
        )
        df_tmp[column_name] = df_tmp["ema"] - df_tmp[self._columns["Low"]]
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def bollinger_bands(
        self,
        period=20,
        deviation=2,
        column_name_top="bollinger_top",
        column_name_mid="bollinger_mid",
        column_name_bottom="bollinger_bottom",
    ):
        """
        Bollinger Bands
        ---------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/bollinger_bands

            >>> Indicators.bollinger_bands(self, period=20, deviation=2, column_name_top='bollinger_up', column_name_mid='bollinger_mid', column_name_bottom='bollinger_bottom')

            :param int period: Period, default 20
            :param int deviation: Number of Standard Deviations, default 2
            :param str column_name_top: default bollinger_up
            :param str column_name_mid: default bollinger_mid
            :param str column_name_bottom: default bollinger_down
            :return: None
        """
        df_tmp = self.df[[self._columns["Close"]]]
        df_tmp = df_tmp.assign(
            mid=df_tmp[self._columns["Close"]].rolling(window=period).mean()
        )
        df_tmp = df_tmp.assign(
            stdev=df_tmp[self._columns["Close"]].rolling(window=period).std(ddof=0)
        )
        df_tmp = df_tmp.assign(tl=df_tmp.mid + deviation * df_tmp.stdev)
        df_tmp = df_tmp.assign(bl=df_tmp.mid - deviation * df_tmp.stdev)

        df_tmp = df_tmp[["mid", "tl", "bl"]]
        df_tmp = df_tmp.rename(
            columns={
                "mid": column_name_mid,
                "tl": column_name_top,
                "bl": column_name_bottom,
            }
        )
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def bulls_power(self, period=13, column_name="bulls_power"):
        """
        Bulls Power
        ------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/bulls_power

            >>> Indicators.bulls_power(period=13, column_name='bulls_power')

            :param int period: Period, default: 13
            :param str column_name: Column name, default: bulls_power
            :return: None
        """
        df_tmp = self.df[[self._columns["Close"], self._columns["High"]]]
        df_tmp = df_tmp.assign(
            ema=df_tmp[self._columns["Close"]].ewm(span=period, adjust=False).mean()
        )
        df_tmp[column_name] = df_tmp[self._columns["High"]] - df_tmp["ema"]
        df_tmp = df_tmp[[column_name]]
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def cci(self, period=14, column_name="cci"):
        """
        Commodity Channel Index (CCI)
        -----------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/commodity_channel_index

            >>> Indicators.cci(period=14, column_name='cci')

            :param int period: Period, default: 14
            :param str column_name: Column name, default: cci
            :return: None
        """
        pd.set_option("display.max_columns", 500)
        df_tmp = self.df[
            [self._columns["High"], self._columns["Low"], self._columns["Close"]]
        ]
        df_tmp = df_tmp.assign(
            tp=(
                df_tmp[self._columns["High"]]
                + df_tmp[self._columns["Low"]]
                + df_tmp[self._columns["Close"]]
            )
            / 3
        )

        df_tmp = df_tmp.assign(tp_sma=df_tmp.tp.rolling(window=period).mean())
        df_tmp = df_tmp.assign(
            tp_mad=df_tmp.tp.rolling(window=period).apply(mad, raw=False)
        )
        df_tmp = df_tmp.assign(tp_min_sma=df_tmp.tp - df_tmp.tp_sma)
        df_tmp = df_tmp.assign(cci=(1 / 0.015) * (df_tmp.tp_min_sma / df_tmp.tp_mad))
        df_tmp = df_tmp[["cci"]]
        df_tmp = df_tmp.rename(columns={"cci": column_name})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def de_marker(self, period=14, column_name="dem"):
        """
        DeMarker (DeM)
        --------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/demarker

            >>> Indicators.de_marker(period=14, column_name='dem')

            :param int period: Period, default: 14
            :param str column_name: Column name, default: dem
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]

        df_tmp = df_tmp.assign(
            hdif=(
                df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(1)
            ).astype(int)
        )
        df_tmp = df_tmp.assign(
            hsub=df_tmp[self._columns["High"]] - df_tmp[self._columns["High"]].shift(1)
        )
        df_tmp = df_tmp.assign(demax=np.where(df_tmp.hdif == 0, 0, df_tmp.hsub))

        df_tmp = df_tmp.assign(
            ldif=(
                df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1)
            ).astype(int)
        )
        df_tmp = df_tmp.assign(
            lsub=df_tmp[self._columns["Low"]].shift(1) - df_tmp[self._columns["Low"]]
        )
        df_tmp = df_tmp.assign(demin=np.where(df_tmp.ldif == 0, 0, df_tmp.lsub))

        df_tmp["sma_demax"] = df_tmp["demax"].rolling(window=period).mean()
        df_tmp["sma_demin"] = df_tmp["demin"].rolling(window=period).mean()

        df_tmp = df_tmp.assign(
            dem=df_tmp.sma_demax / (df_tmp.sma_demax + df_tmp.sma_demin)
        )

        df_tmp = df_tmp[["dem"]]
        df_tmp = df_tmp.rename(columns={"dem": column_name})

        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def force_index(self, period=13, method="sma", apply_to="Close", column_name="frc"):
        """
        Force Index (FRC)
        ------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/force_index

            >>> Indicators.force_index(period=13, method='sma', apply_to='Close', column_name='frc')

            :param int period: Period, default: 13
            :param str method: Moving average method. Can be 'sma', 'smma' or 'ema'. Default: sma
            :param str apply_to: Apply indicator to column, default: Close
            :param str column_name: Column name, default: frc
            :return: None
        """
        df_tmp = self.df[[apply_to, self._columns["Volume"]]]
        if method == "sma":
            df_tmp = df_tmp.assign(ma=df_tmp[apply_to].rolling(window=period).mean())
        elif method == "smma":
            df_tmp_smma = calculate_smma(df_tmp, period, "ma", apply_to)
            df_tmp = df_tmp.merge(df_tmp_smma, left_index=True, right_index=True)
        elif method == "ema":
            df_tmp = df_tmp.assign(
                ma=df_tmp[apply_to].ewm(span=period, adjust=False).mean()
            )
        else:
            raise ValueError('The "method" can be only "sma", "ema" or "smma"')
        df_tmp = df_tmp.assign(
            frc=(df_tmp.ma - df_tmp.ma.shift(1)) * df_tmp[self._columns["Volume"]]
        )
        df_tmp = df_tmp[["frc"]]
        df_tmp = df_tmp.rename(columns={"frc": column_name})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def fractals(
        self, column_name_high="fractals_high", column_name_low="fractals_low"
    ):
        """
        Fractals
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals(column_name_high='fractals_high', column_name_low='fractals_low')

            :param str column_name_high: Column name for High values, default: fractals_high
            :param str column_name_low: Column name for Low values, default: fractals_low
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            fh=np.where(
                (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(1))
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-2)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp.assign(
            fl=np.where(
                (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(2))
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-2)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp[["fh", "fl"]]
        df_tmp = df_tmp.rename(columns={"fh": column_name_high, "fl": column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def fractals3(
        self, column_name_high="fractals3_high", column_name_low="fractals3_low"
    ):
        """
        Fractals 3
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals3(column_name_high='fractals3_high', column_name_low='fractals3_low')

            :param str column_name_high: Column name for High values, default: fractals3_high
            :param str column_name_low: Column name for Low values, default: fractals3_low
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            fh=np.where(
                (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(1)
                    )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(3)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-3)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp.assign(
            fl=np.where(
                (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(3))
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-1)
                )  & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-3)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp[["fh", "fl"]]
        df_tmp = df_tmp.rename(columns={"fh": column_name_high, "fl": column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def fractals5(
        self, column_name_high="fractals5_high", column_name_low="fractals5_low"
    ):
        """
        Fractals 5
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals5(column_name_high='fractals5_high', column_name_low='fractals5_low')

            :param str column_name_high: Column name for High values, default: fractals5_high
            :param str column_name_low: Column name for Low values, default: fractals5_low
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            fh=np.where(
                (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(1)
                    )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(3)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(4)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(5)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-3)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-4)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-5)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp.assign(
            fl=np.where(
                (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(5))
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-3)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-4)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-5)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp[["fh", "fl"]]
        df_tmp = df_tmp.rename(columns={"fh": column_name_high, "fl": column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def fractals8(
        self, column_name_high="fractals8_high", column_name_low="fractals8_low"
    ):
        """
        Fractals 8
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals8(column_name_high='fractals8_high', column_name_low='fractals8_low')

            :param str column_name_high: Column name for High values, default: fractals8_high
            :param str column_name_low: Column name for Low values, default: fractals8_low
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            fh=np.where(
                (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(1)
                    )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(3)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(4)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(5)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(6)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(7)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(8)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-3)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-4)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-5)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-6)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-7)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-8)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp.assign(
            fl=np.where(
                (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(5))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(6))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(7))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(8))
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-3)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-4)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-5)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-6)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-7)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-8)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp[["fh", "fl"]]
        df_tmp = df_tmp.rename(columns={"fh": column_name_high, "fl": column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)


    def fractals13(
        self, column_name_high="fractals13_high", column_name_low="fractals13_low"
    ):
        """
        Fractals 13
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals13(column_name_high='fractals13_high', column_name_low='fractals13_low')

            :param str column_name_high: Column name for High values, default: fractals13_high
            :param str column_name_low: Column name for Low values, default: fractals13_low
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            fh=np.where(
                (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(1)
                    )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(3)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(4)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(5)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(6)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(7)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(8)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(9)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(10)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(11)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(12)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(13)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-3)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-4)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-5)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-6)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-7)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-8)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-9)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-10)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-11)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-12)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-13)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp.assign(
            fl=np.where(
                (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(5))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(6))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(7))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(8))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(9))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(10))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(11))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(12))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(13))
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-3)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-4)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-5)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-6)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-7)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-8)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-9)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-10)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-11)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-12)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-13)
                ),
                True,
                False,
            )
        )
        df_tmp = df_tmp[["fh", "fl"]]
        df_tmp = df_tmp.rename(columns={"fh": column_name_high, "fl": column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)


    def fractals21(
        self, column_name_high="fractals21_high", column_name_low="fractals21_low"
    ):
        """
        Fractals 21
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals21(column_name_high='fractals21_high', column_name_low='fractals21_low')

            :param str column_name_high: Column name for High values, default: fractals21_high
            :param str column_name_low: Column name for Low values, default: fractals21_low
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            fh=np.where(
                (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(1)
                    )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(3)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(4)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(5)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(6)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(7)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(8)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(9)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(10)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(11)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(12)
                )
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(13))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(14))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(15))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(16))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(17))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(18))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(19))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(20))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(21))
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-1)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-3)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-4)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-5)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-6)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-7)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-8)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-9)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-10)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-11)
                )
                & (
                    df_tmp[self._columns["High"]]
                    > df_tmp[self._columns["High"]].shift(-12)
                )
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-13))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-14))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-15))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-16))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-17))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-18))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-19))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-20))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-21))
                ,
                True,
                False,
            )
        )
        df_tmp = df_tmp.assign(
            fl=np.where(
                (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(5))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(6))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(7))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(8))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(9))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(10))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(11))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(12))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(13))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(14))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(15))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(16))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(17))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(18))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(19))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(20))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(21))
                & ( df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-1) )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-2)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-3)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-4)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-5)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-6)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-7)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-8)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-9)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-10)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-11)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-12)
                )
                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-13))

                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-14))

                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-15))

                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-16))

                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-17))

                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-18))

                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-19))

                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-20))

                & (
                    df_tmp[self._columns["Low"]]
                    < df_tmp[self._columns["Low"]].shift(-21))
                ,
                True,
                False,
            )
        )
        df_tmp = df_tmp[["fh", "fl"]]
        df_tmp = df_tmp.rename(columns={"fh": column_name_high, "fl": column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)



    def fractals34(
        self, column_name_high="fractals34_high", column_name_low="fractals34_low"
    ):
        """
        Fractals 34
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals34(column_name_high='fractals34_high', column_name_low='fractals34_low')

            :param str column_name_high: Column name for High values, default: fractals34_high
            :param str column_name_low: Column name for Low values, default: fractals34_low
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            fh=np.where(
                (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(1))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(2))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(3))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(4))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(5))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(6))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(7))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(8))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(9))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(10))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(11))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(12))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(13))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(14))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(15))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(16))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(17))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(18))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(19))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(20))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(21))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(22))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(23))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(24))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(25))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(26))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(27))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(28))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(29))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(30))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(31))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(32))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(33))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(34))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-1))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-2))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-3))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-4))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-5))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-6))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-7))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-8))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-9))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-10))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-11))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-12))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-13))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-14))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-15))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-16))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-17))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-18))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-19))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-20))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-21))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-22))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-23))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-24))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-25))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-26))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-27))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-28))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-29))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-30))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-31))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-32))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-33))
                    & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-34))
                ,
                True,
                False,
            )
        )
        df_tmp = df_tmp.assign(
            fl=np.where(
               (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(5))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(6))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(7))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(8))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(9))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(10))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(11))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(12))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(13))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(14))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(15))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(16))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(17))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(18))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(19))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(20))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(21))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(22))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(23))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(24))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(25))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(26))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(27))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(28))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(29))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(30))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(31))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(32))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(33))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(34))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-5))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-6))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-7))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-8))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-9))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-10))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-11))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-12))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-13))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-14))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-15))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-16))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-17))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-18))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-19))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-20))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-21))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-22))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-23))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-24))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-25))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-26))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-27))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-28))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-29))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-30))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-31))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-32))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-33))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-34))
                ,
                True,
                False,
            )
        )
        df_tmp = df_tmp[["fh", "fl"]]
        df_tmp = df_tmp.rename(columns={"fh": column_name_high, "fl": column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)



    def fractals55(
        self, column_name_high="fractals55_high", column_name_low="fractals55_low"
    ):
        """
        Fractals 55
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals55(column_name_high='fractals55_high', column_name_low='fractals55_low')

            :param str column_name_high: Column name for High values, default: fractals55_high
            :param str column_name_low: Column name for Low values, default: fractals55_low
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            fh=np.where(
              (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(1))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(2))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(3))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(4))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(5))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(6))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(7))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(8))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(9))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(10))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(11))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(12))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(13))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(14))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(15))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(16))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(17))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(18))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(19))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(20))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(21))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(22))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(23))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(24))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(25))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(26))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(27))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(28))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(29))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(30))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(31))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(32))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(33))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(34))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(35))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(36))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(37))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(38))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(39))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(40))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(41))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(42))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(43))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(44))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(45))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(46))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(47))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(48))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(49))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(50))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(51))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(52))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(53))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(54))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(55))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-1))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-2))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-3))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-4))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-5))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-6))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-7))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-8))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-9))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-10))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-11))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-12))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-13))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-14))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-15))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-16))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-17))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-18))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-19))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-20))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-21))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-22))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-23))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-24))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-25))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-26))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-27))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-28))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-29))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-30))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-31))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-32))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-33))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-34))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-35))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-36))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-37))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-38))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-39))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-40))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-41))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-42))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-43))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-44))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-45))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-46))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-47))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-48))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-49))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-50))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-51))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-52))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-53))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-54))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-55))
                ,
                True,
                False,
            )
        )
        df_tmp = df_tmp.assign(
            fl=np.where(
                (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(5))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(6))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(7))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(8))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(9))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(10))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(11))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(12))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(13))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(14))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(15))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(16))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(17))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(18))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(19))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(20))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(21))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(22))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(23))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(24))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(25))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(26))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(27))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(28))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(29))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(30))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(31))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(32))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(33))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(34))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(35))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(36))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(37))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(38))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(39))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(40))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(41))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(42))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(43))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(44))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(45))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(46))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(47))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(48))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(49))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(50))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(51))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(52))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(53))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(54))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(55))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-5))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-6))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-7))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-8))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-9))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-10))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-11))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-12))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-13))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-14))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-15))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-16))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-17))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-18))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-19))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-20))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-21))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-22))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-23))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-24))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-25))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-26))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-27))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-28))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-29))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-30))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-31))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-32))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-33))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-34))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-35))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-36))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-37))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-38))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-39))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-40))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-41))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-42))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-43))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-44))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-45))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-46))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-47))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-48))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-49))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-50))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-51))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-52))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-53))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-54))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-55))
                ,
                True,
                False,
            )
        )
        df_tmp = df_tmp[["fh", "fl"]]
        df_tmp = df_tmp.rename(columns={"fh": column_name_high, "fl": column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)



    def fractals89(
        self, column_name_high="fractals89_high", column_name_low="fractals89_low"
    ):
        """
        Fractals 89
        ---------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/fractals

            >>> Indicators.fractals89(column_name_high='fractals89_high', column_name_low='fractals89_low')

            :param str column_name_high: Column name for High values, default: fractals89_high
            :param str column_name_low: Column name for Low values, default: fractals89_low
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            fh=np.where(
             (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(1))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(2))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(3))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(4))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(5))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(6))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(7))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(8))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(9))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(10))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(11))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(12))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(13))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(14))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(15))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(16))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(17))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(18))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(19))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(20))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(21))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(22))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(23))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(24))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(25))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(26))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(27))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(28))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(29))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(30))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(31))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(32))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(33))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(34))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(35))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(36))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(37))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(38))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(39))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(40))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(41))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(42))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(43))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(44))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(45))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(46))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(47))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(48))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(49))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(50))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(51))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(52))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(53))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(54))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(55))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(56))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(57))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(58))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(59))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(60))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(61))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(62))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(63))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(64))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(65))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(66))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(67))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(68))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(69))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(70))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(71))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(72))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(73))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(74))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(75))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(76))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(77))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(78))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(79))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(80))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(81))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(82))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(83))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(84))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(85))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(86))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(87))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(88))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(89))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-1))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-2))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-3))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-4))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-5))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-6))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-7))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-8))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-9))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-10))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-11))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-12))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-13))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-14))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-15))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-16))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-17))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-18))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-19))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-20))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-21))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-22))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-23))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-24))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-25))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-26))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-27))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-28))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-29))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-30))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-31))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-32))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-33))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-34))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-35))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-36))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-37))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-38))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-39))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-40))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-41))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-42))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-43))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-44))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-45))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-46))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-47))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-48))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-49))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-50))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-51))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-52))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-53))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-54))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-55))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-56))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-57))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-58))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-59))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-60))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-61))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-62))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-63))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-64))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-65))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-66))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-67))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-68))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-69))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-70))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-71))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-72))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-73))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-74))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-75))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-76))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-77))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-78))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-79))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-80))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-81))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-82))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-83))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-84))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-85))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-86))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-87))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-88))
                & (df_tmp[self._columns["High"]] > df_tmp[self._columns["High"]].shift(-89))
                ,
                True,
                False,
            )
        )
        df_tmp = df_tmp.assign(
            fl=np.where(
               (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(5))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(6))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(7))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(8))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(9))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(10))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(11))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(12))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(13))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(14))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(15))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(16))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(17))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(18))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(19))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(20))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(21))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(22))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(23))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(24))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(25))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(26))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(27))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(28))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(29))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(30))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(31))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(32))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(33))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(34))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(35))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(36))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(37))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(38))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(39))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(40))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(41))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(42))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(43))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(44))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(45))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(46))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(47))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(48))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(49))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(50))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(51))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(52))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(53))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(54))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(55))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(56))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(57))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(58))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(59))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(60))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(61))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(62))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(63))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(64))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(65))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(66))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(67))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(68))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(69))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(70))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(71))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(72))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(73))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(74))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(75))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(76))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(77))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(78))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(79))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(80))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(81))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(82))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(83))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(84))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(85))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(86))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(87))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(88))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(89))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-1))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-2))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-3))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-4))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-5))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-6))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-7))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-8))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-9))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-10))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-11))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-12))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-13))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-14))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-15))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-16))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-17))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-18))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-19))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-20))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-21))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-22))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-23))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-24))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-25))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-26))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-27))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-28))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-29))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-30))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-31))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-32))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-33))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-34))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-35))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-36))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-37))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-38))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-39))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-40))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-41))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-42))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-43))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-44))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-45))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-46))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-47))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-48))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-49))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-50))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-51))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-52))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-53))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-54))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-55))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-56))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-57))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-58))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-59))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-60))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-61))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-62))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-63))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-64))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-65))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-66))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-67))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-68))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-69))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-70))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-71))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-72))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-73))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-74))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-75))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-76))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-77))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-78))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-79))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-80))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-81))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-82))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-83))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-84))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-85))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-86))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-87))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-88))
                & (df_tmp[self._columns["Low"]] < df_tmp[self._columns["Low"]].shift(-89))
                ,
                True,
                False,
            )
        )
        df_tmp = df_tmp[["fh", "fl"]]
        df_tmp = df_tmp.rename(columns={"fh": column_name_high, "fl": column_name_low})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)


    def gator(
        self,
        period_jaws=13,
        period_teeth=8,
        period_lips=5,
        shift_jaws=8,
        shift_teeth=5,
        shift_lips=3,
        column_name_val1="value1",
        column_name_val2="value2",
    ):
        """
        Gator Oscillator
        -----------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/gator_oscillator

            >>> Indicators.gator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_val1='value1', column_name_val2='value2')

            :param int period_jaws: Jaws period, default: 13
            :param int period_teeth: Teeth period, default: 8
            :param int period_lips: Lips period, default: 5
            :param int shift_jaws: Jaws shift, default: 8
            :param int shift_teeth: Teeth shift, default: 5
            :param int shift_lips: Lips shift, default: 3
            :param str column_name_val1: Column name for Value1, default value1
            :param str column_name_val2: Column name for Value2, default value2
            :return: None
        """
        df_tmp = self.df[[self._columns["High"], self._columns["Low"]]]
        df_tmp = df_tmp.assign(
            hc=(df_tmp[self._columns["High"]] + df_tmp[self._columns["Low"]]) / 2
        )
        df_j = calculate_smma(df_tmp, period_jaws, "jaws", "hc")
        df_t = calculate_smma(df_tmp, period_teeth, "teeth", "hc")
        df_l = calculate_smma(df_tmp, period_lips, "lips", "hc")

        # Shift SMMAs
        df_j["jaws"] = df_j["jaws"].shift(shift_jaws)
        df_t["teeth"] = df_t["teeth"].shift(shift_teeth)
        df_l["lips"] = df_l["lips"].shift(shift_lips)

        df_tmp = df_tmp.merge(df_j, left_index=True, right_index=True)
        df_tmp = df_tmp.merge(df_t, left_index=True, right_index=True)
        df_tmp = df_tmp.merge(df_l, left_index=True, right_index=True)

        df_tmp = df_tmp.assign(val1=df_tmp["jaws"] - df_tmp["teeth"])
        df_tmp = df_tmp.assign(val2=-(df_tmp["teeth"] - df_tmp["lips"]))

        df_tmp = df_tmp[["val1", "val2"]]
        df_tmp = df_tmp.rename(
            columns={"val1": column_name_val1, "val2": column_name_val2}
        )

        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def ichimoku_kinko_hyo(
        self,
        period_tenkan_sen=9,
        period_kijun_sen=26,
        period_senkou_span_b=52,
        column_name_chikou_span="chikou_span",
        column_name_tenkan_sen="tenkan_sen",
        column_name_kijun_sen="kijun_sen",
        column_name_senkou_span_a="senkou_span_a",
        column_name_senkou_span_b="senkou_span_b",
    ):
        """
        Ichimoku Kinko Hyo
        ------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/ichimoku

            >>> Indicators.ichimoku_kinko_hyo(period_tenkan_sen=9, period_kijun_sen=26, period_senkou_span_b=52, column_name_chikou_span='chikou_span', column_name_tenkan_sen='tenkan_sen', column_name_kijun_sen='kijun_sen', column_name_senkou_span_a='senkou_span_a', column_name_senkou_span_b='senkou_span_b')

            :param int period_tenkan_sen: Period for Tenkan-sen, default: 9
            :param int period_kijun_sen: Period for Kijun-sen, default: 26
            :param int period_senkou_span_b: Period for Senkou-span, default: 52
            :param str column_name_chikou_span: Column name for Chikou-span, default: chikou_span
            :param str column_name_tenkan_sen: Column name for Tenkan-sen, default: tenkan_sen
            :param str column_name_kijun_sen: Column name for Kijun-sen, default: kijun_sen
            :param str column_name_senkou_span_a: Column name for Senkou Span A, default: senkou_span_a
            :param str column_name_senkou_span_b: Column name for Senkou Span B, default: senkou_span_b
            :return: None
        """
        df_tmp = self.df[
            [self._columns["High"], self._columns["Low"], self._columns["Close"]]
        ]

        df_tmp = df_tmp.assign(
            tenkan_h=df_tmp[self._columns["High"]]
            .rolling(window=period_tenkan_sen)
            .max()
        )
        df_tmp = df_tmp.assign(
            tenkan_l=df_tmp[self._columns["Low"]]
            .rolling(window=period_tenkan_sen)
            .min()
        )
        df_tmp = df_tmp.assign(tenkan=(df_tmp.tenkan_h + df_tmp.tenkan_l) / 2)
        del df_tmp["tenkan_h"]
        del df_tmp["tenkan_l"]

        df_tmp = df_tmp.assign(
            kijun_h=df_tmp[self._columns["High"]].rolling(window=period_kijun_sen).max()
        )
        df_tmp = df_tmp.assign(
            kijun_l=df_tmp[self._columns["Low"]].rolling(window=period_kijun_sen).min()
        )
        df_tmp = df_tmp.assign(kijun=(df_tmp.kijun_h + df_tmp.kijun_l) / 2)
        del df_tmp["kijun_h"]
        del df_tmp["kijun_l"]

        df_tmp = df_tmp.assign(
            ssa=((df_tmp.tenkan + df_tmp.kijun) / 2).shift(period_kijun_sen)
        )

        df_tmp = df_tmp.assign(
            ssb_h=df_tmp[self._columns["High"]]
            .rolling(window=period_senkou_span_b)
            .max()
        )
        df_tmp = df_tmp.assign(
            ssb_l=df_tmp[self._columns["Low"]]
            .rolling(window=period_senkou_span_b)
            .min()
        )
        df_tmp = df_tmp.assign(
            ssb=((df_tmp.ssb_h + df_tmp.ssb_l) / 2).shift(period_kijun_sen)
        )
        del df_tmp["ssb_h"]
        del df_tmp["ssb_l"]

        df_tmp = df_tmp.assign(
            chikou=df_tmp[self._columns["Close"]].shift(-period_kijun_sen)
        )

        df_tmp = df_tmp[["tenkan", "kijun", "ssa", "ssb", "chikou"]]
        df_tmp = df_tmp.rename(
            columns={
                "tenkan": column_name_tenkan_sen,
                "kijun": column_name_kijun_sen,
                "ssa": column_name_senkou_span_a,
                "ssb": column_name_senkou_span_b,
                "chikou": column_name_chikou_span,
            }
        )

        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def bw_mfi(self, column_name="bw_mfi"):
        """
        Market Facilitation Index (BW MFI)
        ----------------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/market_facilitation_index

            >>> Indicators.bw_mfi(column_name='bw_mfi')

            :param str column_name: Column name, default: bw_mfi
            :return: None
        """
        df_tmp = self.df[
            [self._columns["High"], self._columns["Low"], self._columns["Volume"]]
        ]
        df_tmp = df_tmp.assign(
            bw=(df_tmp[self._columns["High"]] - df_tmp[self._columns["Low"]])
            / df_tmp[self._columns["Volume"]]
            * 100000
        )
        df_tmp = df_tmp[["bw"]]
        df_tmp = df_tmp.rename(columns={"bw": column_name})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def momentum(self, period=14, column_name="momentum"):
        """
        Momentum
        --------
            https://www.metatrader4.com/ru/trading-platform/help/analytics/tech_indicators/momentum

            >>> Indicators.momentum(period=14, column_name='momentum')

            :param int period: Period, default: 14
            :param strr column_name: Column name, default: momentum
            :return:
        """
        close = self._columns["Close"]
        df_tmp = self.df[[close]]
        df_tmp = df_tmp.assign(m=df_tmp[close] / df_tmp[close].shift(period) * 100)
        df_tmp = df_tmp[["m"]]
        df_tmp = df_tmp.rename(columns={"m": column_name})
        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def mfi(self, period=5, column_name="mfi"):
        """
        Money Flow Index (MFI)
        -----------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/money_flow_index

            >>> Indicators.mfi(period=5, column_name='mfi')
        :param int period: Period, default: 5
        :param str column_name: Column name, default: mfi
        :return: None
        """
        high, low, close, volume = (
            self._columns["High"],
            self._columns["Low"],
            self._columns["Close"],
            self._columns["Volume"],
        )
        df_tmp = self.df[[high, low, close, volume]]

        df_tmp = df_tmp.assign(tp=(df_tmp[high] + df_tmp[low] + df_tmp[close]) / 3)
        df_tmp = df_tmp.assign(mf=df_tmp["tp"] * df_tmp[volume])

        df_tmp = df_tmp.assign(
            pmf=np.where(df_tmp["tp"] > df_tmp["tp"].shift(1), df_tmp["mf"], 0.0)
        )
        df_tmp = df_tmp.assign(
            nmf=np.where(df_tmp["tp"] < df_tmp["tp"].shift(1), df_tmp["mf"], 0.0)
        )

        df_tmp["pmfs"] = df_tmp.pmf.rolling(window=period).sum()
        df_tmp["nmfs"] = df_tmp.nmf.rolling(window=period).sum()

        del df_tmp["tp"]
        del df_tmp["mf"]
        del df_tmp["pmf"]
        del df_tmp["nmf"]

        df_tmp = df_tmp.round(decimals=10)
        df_tmp = df_tmp.assign(mr=df_tmp.pmfs / df_tmp.nmfs)
        df_tmp = df_tmp.assign(mfi=100 - (100 / (1 + df_tmp.mr)))

        df_tmp = df_tmp[["mfi"]]
        df_tmp = df_tmp.rename(columns={"mfi": column_name})

        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)

    def macd(
        self,
        period_fast=12,
        period_slow=26,
        period_signal=9,
        column_name_value="macd_value",
        column_name_signal="macd_signal",
    ):
        """
        Moving Average Convergence/Divergence (MACD)
        --------------------------------------------
            https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/macd

            >>> Indicators.macd(self, period_fast=12, period_slow=26, period_signal=9, column_name_value='macd_value', column_name_signal='macd_signal')

            :param int period_fast: Period for Fast EMA, default: 12
            :param int period_slow: Period for Slow EMA, default: 26
            :param int period_signal: Period for Signal Line, default 9
            :param str column_name_value: Column name for MACD Value, default macd_value
            :param str column_name_signal: Column name for MACD Signal, default macd_signal
            :return: None
        """
        close = self._columns["Close"]
        df_tmp = self.df[[close]]

        df_tmp = df_tmp.assign(
            fast=df_tmp[close].ewm(span=period_fast, adjust=False).mean()
        )
        df_tmp = df_tmp.assign(
            slow=df_tmp[close].ewm(span=period_slow, adjust=False).mean()
        )
        df_tmp = df_tmp.assign(value=df_tmp["fast"] - df_tmp["slow"])
        df_tmp = df_tmp.assign(
            signal=df_tmp["value"].rolling(window=period_signal).mean()
        )

        df_tmp = df_tmp[["value", "signal"]]
        df_tmp = df_tmp.rename(
            columns={"value": column_name_value, "signal": column_name_signal}
        )

        self.df = self.df.merge(df_tmp, left_index=True, right_index=True)


    def pds_add_ohlc_stc_columns(__df,
                       cleanupOriginalColumn=True,quiet=True):
        if not 'Open' in __df.columns:
            __df['Open'] = __df[['BidOpen', 'AskOpen']].mean(axis=1)
            __df['High'] = __df[['BidHigh', 'AskHigh']].mean(axis=1)
            __df['Low'] = __df[['BidLow', 'AskLow']].mean(axis=1)
            __df['Close'] = __df[['BidClose', 'AskClose']].mean(axis=1)
            #Median
            __df['Median']= ((__df['High'] + __df['Low']) / 2)
        if cleanupOriginalColumn:
            __df=Indicators.__cleanse_original_columns(__df,quiet)
        return __df


    def __cleanse_original_columns(__df,_quiet=True):
        __df=Indicators.pds_cleanse_original_columns(__df,_quiet)
        return __df

    def pds_cleanse_original_columns(__df,_quiet=True):
        __df=Indicators.jgtpd_drop_col_by_name(__df,'AskHigh',1,_quiet)
        __df=Indicators.jgtpd_drop_col_by_name(__df,'BidHigh',1,_quiet)
        __df=Indicators.jgtpd_drop_col_by_name(__df,'AskLow',1,_quiet)
        __df=Indicators.jgtpd_drop_col_by_name(__df,'BidLow',1,_quiet)
        __df=Indicators.jgtpd_drop_col_by_name(__df,'AskClose',1,_quiet)
        __df=Indicators.jgtpd_drop_col_by_name(__df,'BidClose',1,_quiet)
        __df=Indicators.jgtpd_drop_col_by_name(__df,'BidOpen',1,_quiet)
        __df=Indicators.jgtpd_drop_col_by_name(__df,'AskOpen',1,_quiet)
        return __df

    def jgtpd_drop_col_by_name(_df,colname,_axis = 1,_quiet=False):
        """Drop Column in DF by Name

        Args:
                _df (DataFrame source)
                ctxcolname (column name from)
                _axis (  axis)
                _quiet (quiet output)

        Returns:
            Clean DataFrame
        """
        if colname in _df.columns:
            return _df.drop(_df.loc[:, colname:colname].columns,axis = _axis)
        else:
            if not _quiet:
                print('Col:' + colname + ' was not there')
            return _df



    def jgt_create_ids_indicators_as_instance(__df,
                       enableGatorOscillator=False,
                       enableMFI=False,
                       cleanupOriginalColumn=True,
                       quiet=False):
        """
        Adds various JGT indicators to the given DataFrame and returns an instance of the Indicators class.

        Args:
            df (pandas.DataFrame): The DataFrame to which the indicators will be added.
            enableGatorOscillator (bool, optional): Whether to enable the Gator Oscillator indicator. Defaults to False.
            enableMFI (bool, optional): Whether to enable the Money Flow Index (MFI) indicator. Defaults to False.
            cleanupOriginalColumn (bool, optional): Whether to clean up the original columns. Defaults to True.
            quiet (bool, optional): Whether to suppress the output. Defaults to False.

        Returns:
            Indicators: An instance of the Indicators class with the added indicators.
        """
        if not quiet:
            print("Adding indicators...")
        # if not 'pen' in self.df.columns:
        #     __df=__.rename(columns={'bidopen': 'BidOpen', 'bidhigh': 'BidHigh','bidclose':'BidClose','bidlow':'BidLow','askopen': 'AskOpen', 'askhigh': 'AskHigh','askclose':'AskClose','asklow':'AskLow','tickqty':'Volume','date':'Date'})
        __df=Indicators.pds_add_ohlc_stc_columns(__df,cleanupOriginalColumn)
        i=Indicators(__df)
        i.accelerator_oscillator( column_name= 'ac')
        i.alligator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_jaws='jaw', column_name_teeth='teeth', column_name_lips='lips')
        i.alligator(period_jaws=89, period_teeth=55, period_lips=34, shift_jaws=55, shift_teeth=34, shift_lips=21, column_name_jaws='bjaw', column_name_teeth='bteeth', column_name_lips='blips')
        i.awesome_oscillator(column_name='ao')
        i.fractals(column_name_high='fb', column_name_low='fs')
        i.fractals3(column_name_high='fb3', column_name_low='fs3')
        i.fractals5(column_name_high='fb5', column_name_low='fs5')
        i.fractals8(column_name_high='fb8', column_name_low='fs8')
        i.fractals13(column_name_high='fb13', column_name_low='fs13')
        i.fractals21(column_name_high='fb21', column_name_low='fs21')
        i.fractals34(column_name_high='fb34', column_name_low='fs34')
        i.fractals55(column_name_high='fb55', column_name_low='fs55')
        i.fractals89(column_name_high='fb89', column_name_low='fs89')

        if enableGatorOscillator:
            i.gator(period_jaws=13, period_teeth=8, period_lips=5, shift_jaws=8, shift_teeth=5, shift_lips=3, column_name_val1='gl', column_name_val2='gh')
        if enableMFI:
            i.bw_mfi(column_name='mfi')
        return i


    def jgt_create_ids_indicators_as_dataframe(dfsrc,
                           enableGatorOscillator=False,
                           enableMFI=False,
                           cleanupOriginalColumn=True,
                           dropnavalue=True,
                           quiet=False):
        """
        Creates a pandas dataframe with JGT indicators based on the input dataframe.

        Args:
        dfsrc (pandas.DataFrame): The input dataframe.
        enableGatorOscillator (bool): Whether to enable the Gator Oscillator indicator. Default is False.
        enableMFI (bool): Whether to enable the Money Flow Index indicator. Default is False.
        cleanupOriginalColumn (bool): Whether to clean up the original column. Default is True.
        dropnavalue (bool): Whether to drop rows with NaN values. Default is True.
        quiet (bool): Whether to suppress print statements. Default is False.

        Returns:
        pandas.DataFrame: The dataframe with JGT indicators.
        """
        i=Indicators.jgt_create_ids_indicators_as_instance(dfsrc,
                           enableGatorOscillator,
                           enableMFI,
                           cleanupOriginalColumn,
                           quiet)
        dfresult=i.df
        if dropnavalue:
            dfresult = dfresult.dropna()
        try:
            dfresult=dfresult.set_index(Indicators.index_column_name)
        except TypeError:
            pass
        if not quiet:
            print("done adding indicators :)")
        return dfresult

