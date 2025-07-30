import io
from datetime import timedelta
from functools import partial, reduce
from typing import Any, Callable, Collection, List, Optional, Union, cast, \
    NamedTuple, MutableMapping

import pandas as pd

from .model import ChargerTransaction, Leg, Trip

to_numeric = partial(pd.to_numeric, errors='coerce')

DF_BiFunc = Callable[[pd.DataFrame, pd.DataFrame], pd.DataFrame]


def _identity(x):
    return x


class Data(NamedTuple):
    """Alternate shape for leg data."""

    index: List[pd.Timestamp]
    data: List[tuple]


def get_data_frame(self: Union[Leg, Trip],
                   data_types: Union[str, Collection[str]],
                   resolution: Union[str, timedelta, None] = None,
                   conversion: Optional[Callable[[str], Any]] = to_numeric
                   ) -> pd.DataFrame:
    """
    Return available measurements as a time-series :code:`DataTable`.

    :code:`Series` will be named :code:`{TYPE}_{FIELD}` in the order given
    by :code:`data_types`.

    Data will be interpolated to the specified resolution.

    :param data_types: Data types to fetch.
    :param resolution: Target resolution. If :code:`None` (the default) then
        it will use the approximate resolution of the first requested type.
    :param conversion: Conversion to apply to all values. If :code:`None`
        then all values will be strings.
    """
    if isinstance(data_types, str):
        data_types = [data_types]

    if conversion is None:
        conversion = _identity

    collected: MutableMapping[str, Optional[Data]] = {
        dt: Data([], []) for dt in data_types
    }
    for m in self.get_data(include=data_types):
        collected[m.type].index.append(pd.to_datetime(int(m.timestamp),
                                                      unit='ms'))
        collected[m.type].data.append(tuple(conversion(v)
                                            for v in m.data.split(',')))

    if resolution is None and len(data_types) > 1:
        try:
            index = collected[data_types[0]].index
            resolution = index[1] - index[0]
        except IndexError:
            raise ValueError('No data for first type and no resolution given')

    new_index = None
    if resolution is not None:
        start = pd.to_datetime(self.start_time).ceil(resolution)
        end = pd.to_datetime(self.end_time).ceil(resolution)
        new_index = pd.date_range(start=start, end=end, freq=resolution)
        # np.datetime64 cannot hold timezone
        new_index = new_index.tz_localize(None)

    type_defs = self._client.get_types()

    converted: List[pd.DataFrame] = []
    for dt in data_types:
        if len(collected[dt].index) == 0:
            continue

        index = pd.DatetimeIndex(collected[dt].index)
        data = collected[dt].data
        columns = ['{} {}'.format(dt, field.name)
                   for field in type_defs[dt].fields]
        del collected[dt]  # allow GC of the data during loop
        df = pd.DataFrame.from_records(data=data,
                                       index=index,
                                       columns=columns)

        if not index.is_unique:
            # https://csrf.atlassian.net/browse/PLAT-222
            df = df[~index.duplicated()]
            index = df.index

        if new_index is not None:
            df = df \
                .reindex(index.union(new_index)) \
                .interpolate(method='index') \
                .reindex(new_index)

        if not df.empty:
            converted.append(df)

    if len(converted) == 0:
        return pd.DataFrame()
    else:
        return reduce(cast(DF_BiFunc, pd.DataFrame.join), converted)


def get_gradient_frame(self: Leg, **kwargs) -> pd.DataFrame:
    """
    Return computed gradient data as a time-series :code:`DataTable`.

    :param generate: Request and wait for generation if not available
    :param timeout: How long to wait if requesting generation
    """
    type_defs = self._client.get_types()
    columns = ['9 ' + field.name for field in type_defs['9'].fields]

    data = self.get_gradient(**kwargs)
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame.from_records(
        ((pd.to_datetime(int(m.timestamp), unit='ms'), *(
            pd.to_numeric(v) for v in m.data.split(','))) for m in data),
        index='timestamp',
        columns=['timestamp', *columns]
    )
    return df


def get_transaction_frame(self: ChargerTransaction) -> pd.DataFrame:
    """Return meter readings as a time-series :code:`DataTable`."""
    response = self._client.get(self.uri + '/data',
                                headers={'Accept': 'text/csv'})
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text),
                     names=['timestamp', 'value'],
                     dtype={'timestamp': 'int64',
                            'value': 'float64'},
                     index_col='timestamp')
    df.index = pd.to_datetime(df.index, unit='ms')
    return df


Leg.get_data_frame = get_data_frame
Trip.get_data_frame = get_data_frame
Leg.get_gradient_frame = get_gradient_frame
ChargerTransaction.get_data_frame = get_transaction_frame
