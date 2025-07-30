import datetime

from typing import TYPE_CHECKING


class InAfterOutError(ValueError):
    def __init__(
        self, in_datetimestamp: datetime.datetime, out_datetimestamp: datetime.datetime
    ) -> None:
        super().__init__(f"{in_datetimestamp=} > {out_datetimestamp=}")


class OverlappingEntriesError(ValueError):
    def __init__(self, entry1: "Entry", entry2: "Entry") -> None:
        super().__init__(f"{entry1=} overlaps with {entry2=}")


if TYPE_CHECKING:
    from stechuhr.logbooks import Entry
