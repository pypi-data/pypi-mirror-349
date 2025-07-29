"""functions for fetching data from https://data.binance.vision/"""

from __future__ import annotations

import typing

import absorb

if typing.TYPE_CHECKING:
    import datetime
    import polars as pl


CandlestickInterval = typing.Literal[
    '1s',
    '1m',
    '3m',
    '5m',
    '15m',
    '30m',
    '1h',
    '2h',
    '4h',
    '6h',
    '8h',
    '12h',
    '1d',
]


class Candles(absorb.Table):
    source = 'binance'
    write_range = 'append_only'
    parameter_types = {'pair': str, 'interval': str, 'market': str}
    default_parameters = {'market': 'spot'}
    name_template = {'custom': 'candles_{market}_{pair}_{interval}'}

    def get_schema(self) -> dict[str, type[pl.DataType] | pl.DataType]:
        import polars as pl

        return {
            'timestamp': pl.Datetime('us'),
            'open': pl.Float64,
            'high': pl.Float64,
            'low': pl.Float64,
            'close': pl.Float64,
            'n_trades': pl.Int64,
            'base_volume': pl.Float64,
            'quote_volume': pl.Float64,
            'taker_buy_base_volume': pl.Float64,
            'taker_buy_quote_volume': pl.Float64,
        }

    def collect_chunk(self, data_range: typing.Any) -> pl.DataFrame:
        if self.parameters['market'] == 'spot':
            return get_spot_candlesticks(
                pair=self.parameters['pair'],
                timestamp=data_range,
                interval=self.parameters['interval'],
                duration='daily',
            )
        else:
            raise Exception('invalid market')


class Trades(absorb.Table):
    source = 'binance'
    write_range = 'append_only'
    parameter_types = {'pair': str, 'market': str}
    default_parameters = {'market': 'spot'}
    name_template = {'custom': 'trades_{market}_{pair}'}

    def get_schema(self) -> dict[str, type[pl.DataType] | pl.DataType]:
        import polars as pl

        return {
            'timestamp': pl.Datetime('us'),
            'price': pl.Float64,
            'quantity_base': pl.Float64,
            'quantity_quote': pl.Float64,
            'buyer_is_maker': pl.Boolean,
            'best_price_match': pl.Boolean,
            'trade_id': pl.Int64,
        }

    def collect_chunk(self, data_range: typing.Any) -> pl.DataFrame:
        if self.parameters['market'] == 'spot':
            return get_spot_trades(
                pair=self.parameters['pair'],
                timestamp=data_range,
                duration='daily',
            )
        else:
            raise Exception('invalid market')


class AggregateTrades(absorb.Table):
    source = 'binance'
    write_range = 'append_only'
    parameter_types = {'pair': str, 'market': str}
    default_parameters = {'market': 'spot'}
    name_template = {'custom': 'aggregate_trades_{market}_{pair}'}

    def get_schema(self) -> dict[str, type[pl.DataType] | pl.DataType]:
        import polars as pl

        return {
            'timestamp': pl.Datetime('us'),
            'price': pl.Float64,
            'quantity': pl.Float64,
            'buyer_is_maker': pl.Boolean,
            'best_price_match': pl.Boolean,
            'aggregate_trade_id': pl.Int64,
            'first_trade_id': pl.Int64,
            'last_trade_id': pl.Int64,
        }

    def collect_chunk(self, data_range: typing.Any) -> pl.DataFrame:
        if self.parameters['market'] == 'spot':
            return get_spot_aggregate_trades(
                pair=self.parameters['pair'],
                timestamp=data_range,
                duration='daily',
            )
        else:
            raise Exception('invalid market')


def get_spot_url(
    *,
    pair: str,
    timestamp: datetime.datetime,
    datatype: typing.Literal['trades', 'aggTrades', 'klines'],
    duration: typing.Literal['daily', 'monthly'],
    interval: CandlestickInterval | None = None,
) -> str:
    import datetime
    import os

    if duration == 'daily':
        if timestamp != datetime.datetime(
            timestamp.year, timestamp.month, timestamp.day
        ):
            raise Exception('timestamp must be a specific day')
        date_str = timestamp.strftime('%Y-%m-%d')
    elif duration == 'monthly':
        if timestamp != datetime.datetime(timestamp.year, timestamp.month, 1):
            raise Exception('timestamp must be a specific month')
        date_str = timestamp.strftime('%Y-%m')
    else:
        raise Exception('invalid interval, choose daily or monthly')

    if datatype == 'klines':
        if interval is None:
            raise Exception('must specify interval')
        template = 'spot/{duration}/klines/{pair}/{interval}/{pair}-{interval}-{date_str}.zip'
    else:
        if interval is not None:
            raise Exception(
                'cannot specify interval for dataset, only specify duration'
            )
        template = (
            'spot/{duration}/{datatype}/{pair}/{pair}-{datatype}-{date_str}.zip'
        )

    root = 'https://data.binance.vision/data'
    tail = template.format(
        datatype=datatype,
        pair=pair,
        duration=duration,
        interval=interval,
        date_str=date_str,
    )
    return os.path.join(root, tail)


def get_spot_trades(
    pair: str,
    timestamp: datetime.datetime,
    duration: typing.Literal['daily', 'monthly'] = 'daily',
) -> pl.DataFrame:
    import polars as pl

    url = get_spot_url(
        pair=pair,
        timestamp=timestamp,
        datatype='trades',
        duration=duration,
    )

    raw_schema: dict[str, pl.DataType | type[pl.DataType]] = {
        'trade_id': pl.Int64,
        'price': pl.Float64,
        'quantity_base': pl.Float64,
        'quantity_quote': pl.Float64,
        'timestamp': pl.Int64,
        'buyer_is_maker': pl.Boolean,
        'best_price_match': pl.Boolean,
    }

    columns = [
        'timestamp',
        'price',
        'quantity_base',
        'quantity_quote',
        'buyer_is_maker',
        'best_price_match',
        'trade_id',
    ]

    return _process(url=url, raw_schema=raw_schema, columns=columns)


def get_spot_aggregate_trades(
    pair: str,
    timestamp: datetime.datetime,
    duration: typing.Literal['daily', 'monthly'] = 'daily',
) -> pl.DataFrame:
    import polars as pl

    url = get_spot_url(
        pair=pair,
        timestamp=timestamp,
        datatype='aggTrades',
        duration=duration,
    )

    raw_schema: dict[str, pl.DataType | type[pl.DataType]] = {
        'aggregate_trade_id': pl.Int64,
        'price': pl.Float64,
        'quantity': pl.Float64,
        'first_trade_id': pl.Int64,
        'last_trade_id': pl.Int64,
        'timestamp': pl.Int64,
        'buyer_is_maker': pl.Boolean,
        'best_price_match': pl.Boolean,
    }

    columns = [
        'timestamp',
        'price',
        'quantity',
        'buyer_is_maker',
        'best_price_match',
        'aggregate_trade_id',
        'first_trade_id',
        'last_trade_id',
    ]

    return _process(url=url, raw_schema=raw_schema, columns=columns)


def get_spot_candlesticks(
    pair: str,
    timestamp: datetime.datetime,
    interval: CandlestickInterval,
    duration: typing.Literal['daily', 'monthly'] = 'daily',
) -> pl.DataFrame:
    import polars as pl

    url = get_spot_url(
        pair=pair,
        timestamp=timestamp,
        datatype='klines',
        interval=interval,
        duration=duration,
    )

    raw_schema: dict[str, pl.DataType | type[pl.DataType]] = {
        'timestamp': pl.Int64,
        'open': pl.Float64,
        'high': pl.Float64,
        'low': pl.Float64,
        'close': pl.Float64,
        'base_volume': pl.Float64,
        'close_timestamp': pl.Int64,
        'quote_volume': pl.Float64,
        'n_trades': pl.Int64,
        'taker_buy_base_volume': pl.Float64,
        'taker_buy_quote_volume': pl.Float64,
        'ignore': pl.String,
    }

    columns = [
        'timestamp',
        'open',
        'high',
        'low',
        'close',
        'n_trades',
        'base_volume',
        'quote_volume',
        'taker_buy_base_volume',
        'taker_buy_quote_volume',
    ]

    return _process(url=url, raw_schema=raw_schema, columns=columns)


def _process(
    url: str,
    raw_schema: dict[str, pl.DataType | type[pl.DataType]],
    columns: list[str],
) -> pl.DataFrame:
    import polars as pl

    return (
        absorb.ops.download_csv_zip_to_dataframe(
            url, polars_kwargs={'schema': raw_schema, 'has_header': False}
        )
        .with_columns(pl.col.timestamp.cast(pl.Datetime('us')))
        .select(columns)
    )
