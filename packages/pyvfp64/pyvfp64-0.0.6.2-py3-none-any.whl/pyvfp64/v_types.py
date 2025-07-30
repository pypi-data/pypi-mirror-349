import decimal
from datetime import timedelta, datetime, date, time

from sqlalchemy import TypeDecorator, Numeric, Dialect, Integer, types, String, Float, DateTime


class CustomDecimal(TypeDecorator):
    impl = Numeric

    def process_bind_param(self, value, dialect):
        return value  # No transformation on input; can customize if needed

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        elif value == int(value):
            return int(value)
        else:
            return float(value)

    def copy(self):
        return CustomDecimal()


class CustomInterval(TypeDecorator):
    impl = types.Interval
    python_type = timedelta
    epoch = datetime.fromtimestamp(0).replace(tzinfo=None)

    def bind_processor(self, dialect: Dialect):
        impl_processor = self.impl.bind_processor(dialect)
        epoch = self.epoch

        def process(value: timedelta):
            if value is not None:
                dt_value = epoch + value
            else:
                dt_value = None
            return impl_processor(dt_value) if impl_processor else dt_value

        return process

    def result_processor(self, dialect: Dialect, coltype):
        impl_processor = self.impl.result_processor(dialect, coltype)
        epoch = self.epoch

        def process(value) -> timedelta:
            if isinstance(value, (decimal.Decimal, float, int)):
                return timedelta(seconds=int(value))
            elif isinstance(value, (float, int)):
                return timedelta(seconds=value)
            elif impl_processor:
                dt_value = impl_processor(value)
                return dt_value - epoch if dt_value else None
            else:
                return value - epoch if value else None

        return process


class CustomInteger(TypeDecorator):
    impl = Integer

    def process_bind_param(self, value, dialect):
        return value  # No transformation on input; can customize if needed

    def process_result_value(self, value, dialect):
        try:
            if value is None:
                return None
            elif value == int(value):
                return int(value)
            else:
                return float(value)
        except ValueError:
            # some strings are coming here and I don't know why
            return value

    def copy(self):
        return CustomInteger()


class DateTimeConv(TypeDecorator):
    """
    Normalize incoming values to datetime:
      • datetime.datetime     → passed through
      • datetime.date         → midnight UTC- or naive-local
      • ISO-8601 strings, with or without 'T', fractional seconds, 'Z' or offset
      • 'YYYY-MM-DD hh:mm:ss(.ffffff)' strings
      • {^YYYY-MM-DD hh:mm:ss}  (VFP timestamp)
    """
    impl = DateTime
    cache_ok = True

    def _parse_string(self, s: str) -> datetime:
        s = s.strip()
        # strip off VFP {^ … }
        if s.startswith("{^") and s.endswith("}"):
            s = s[2:-1]
        # if trailing Z, treat as UTC
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        # attempt ISO-8601
        try:
            return datetime.fromisoformat(s)
        except ValueError:
            pass

        # common fallback formats
        fmts = [
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
        ]
        for fmt in fmts:
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                continue

        # maybe plain date
        try:
            d = date.fromisoformat(s)
            return datetime.combine(d, time.min)
        except ValueError:
            pass

        raise ValueError(f"Unable to parse datetime string: {s!r}")

    def process_bind_param(self, value, dialect):
        # Python → database
        if value is None:
            return None

        if isinstance(value, str):
            value = self._parse_string(value)

        elif isinstance(value, date) and not isinstance(value, datetime):
            # promote date to datetime
            value = datetime.combine(value, time.min)

        # at this point we assume it's a datetime
        return value

    def process_result_value(self, value, dialect):
        # database → Python
        if value is None:
            return None

        if isinstance(value, str):
            value = self._parse_string(value)

        elif isinstance(value, date) and not isinstance(value, datetime):
            value = datetime.combine(value, time.min)

        return value

class TrimmedString(TypeDecorator):
    impl = String

    @property
    def python_type(self):
        return str  # or whatever python type you want it to map to

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.strip()
        return value


class CustomFloat(TypeDecorator):
    impl = Float

    @property
    def python_type(self):
        return float  # or whatever python type you want it to map to

    def process_result_value(self, value, dialect):
        if type(value) is str:
            try:
                return self.python_type(value)
            except:
                return 0

        return value


class CustomInt(TypeDecorator):
    impl = Integer

    @property
    def python_type(self):
        return int  # or whatever python type you want it to map to

    def process_result_value(self, value, dialect):
        if type(value) is str:
            try:
                return self.python_type(value)
            except:
                return 0

        return value
