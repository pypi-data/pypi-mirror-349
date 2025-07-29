import pandas as pd

from contexere.scheme import abbreviate_date, abbreviate_time, decode_abbreviated_datetime


class Calendar(object):
    def __init__(self):
        self.cache_ = dict()

    def __call__(self, dt=None):
        if dt is None:
            abbreviated_datetime = abbreviate_date() + abbreviate_time()
        else:
            abbreviated_datetime = abbreviate_date(dt) + abbreviate_time(dt)
        self.cache_[abbreviated_datetime] = dt
        return abbreviated_datetime

    def __getitem__(self, abbreviated_datetime):
        if not abbreviated_datetime in self.cache_.keys():
            self.cache_[abbreviated_datetime] = decode_abbreviated_datetime(abbreviated_datetime)
        return self.cache_[abbreviated_datetime]

    def forward(self, start, horizon):
        """
        Compute abbreviated time stamp in the future

        >>> calendar = Calendar()
        >>> calendar.forward('21vMu00', pd.Timedelta('12h'))
        '21vNi00'

        Args:
            start: Abbreviated datetime string
            horizon: pd.Timedelta object (default pd.Timedelta('12h'))

        Returns:
            abbreviated datetime
        """
        start_dt = self.__getitem__(start)
        end_dt = start_dt + horizon
        return abbreviate_date(end_dt) + abbreviate_time(end_dt)

    def backward(self, start, horizon):
        """
        Compute abbreviated time stamp in the past

        >>> calendar = Calendar()
        >>> calendar.backward('21vMu00', pd.Timedelta('12h'))
        '21vMi00'

        Args:
            start: Abbreviated datetime string
            horizon: pd.Timedelta object (default pd.Timedelta('12h'))

        Returns:
            abbreviated datetime
        """
        start_dt = self.__getitem__(start)
        end_dt = start_dt - horizon
        return abbreviate_date(end_dt) + abbreviate_time(end_dt)

    def in_seconds(self, abbreviated_datetime):
        return self.__getitem__(abbreviated_datetime).timestamp()




class DailyEnumerator(object):
    """
    Iterator for counters of daily data sets.
    """

    def __init__(self, N=None, previous=None):
        if previous is not None:
            for letter in previous:
                assert letter >= 'a' and letter <= 'z'
        self.start_value = 'a'
        self.previous = previous
        self.N = N

    def __iter__(self):
        self.value = self.previous
        self.n = 0
        return self

    def __next__(self):
        if self.n == self.N:
            raise StopIteration
        self.n += 1

        if self.value is None:
            self.value = self.start_value
        else:
            self.value = self.plus_one(self.value)
        return self.value

    def plus_one(self, stump):
        if len(stump) == 0:
            return 'a'
        elif stump[-1] < 'z':
            return stump[:-1] + chr(ord(stump[-1]) + 1)
        else:
            return self.plus_one(stump[:-1]) + 'a'