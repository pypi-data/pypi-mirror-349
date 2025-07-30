import datetime
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

from stechuhr.errors import InAfterOutError


@dataclass(frozen=True, order=True)
class Entry:
    in_datetimestamp: datetime.datetime
    out_datetimestamp: datetime.datetime | None

    @classmethod
    def from_datetimestamps(
        cls,
        in_datetimestamp: datetime.datetime,
        out_datetimestamp: datetime.datetime | None = None,
    ) -> Self:
        if out_datetimestamp is not None and in_datetimestamp > out_datetimestamp:
            raise InAfterOutError(
                in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
            )
        return cls(
            in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
        )


@dataclass(frozen=True)
class Logbook:
    entries: frozenset[Entry]

    @classmethod
    def from_entries(cls, entries: Iterable[Entry]) -> Self:
        return cls(frozenset(entries))
