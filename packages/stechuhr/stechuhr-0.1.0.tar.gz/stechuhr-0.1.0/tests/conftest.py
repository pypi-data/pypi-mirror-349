import datetime
from collections.abc import Iterable
from enum import Enum, auto

from hypothesis import strategies as st

from stechuhr import logbooks as lgbks


class EntryState(Enum):
    CLOSED = (auto(),)
    OPEN = (auto(),)
    UNDETERMINED = (auto(),)


@st.composite
def entries(
    draw,
    *,
    min_value: datetime.datetime = datetime.datetime.min,
    max_value: datetime.datetime = datetime.datetime.max,
    unfinished: EntryState = EntryState.UNDETERMINED,
) -> lgbks.Entry:
    in_datetimestamp = draw(st.datetimes(min_value=min_value, max_value=max_value))
    out_datetimestamp = None
    if unfinished is EntryState.UNDETERMINED:
        unfinished = draw(st.sampled_from((EntryState.CLOSED, EntryState.OPEN)))
    match unfinished:
        case EntryState.CLOSED:
            out_datetimestamp = draw(
                st.datetimes(min_value=in_datetimestamp, max_value=max_value)
            )
        case EntryState.OPEN:
            out_datetimestamp = None
        case EntryState.UNDETERMINED:
            assert False
    return lgbks.Entry.from_datetimestamps(in_datetimestamp, out_datetimestamp)


@st.composite
def non_overlapping_entries(
    draw,
    *,
    min_size: int = 0,
    max_size: int | None = None,
    min_value: datetime.datetime = datetime.datetime.min,
    max_value: datetime.datetime = datetime.datetime.max,
    last_unfinished: EntryState = EntryState.UNDETERMINED,
) -> Iterable[lgbks.Entry]:
    if max_size is None:
        max_size = draw(st.integers(min_value=min_size))
    target_size = draw(st.integers(min_value=min_size, max_value=max_size))
    if target_size == 0:
        return
    entry = draw(
        entries(
            min_value=min_value,
            max_value=max_value,
            unfinished=EntryState.CLOSED if target_size > 1 else last_unfinished,
        )
    )
    assert target_size <= 1 or entry.out_datetimestamp is not None, entry
    yield entry
    target_size -= 1
    while target_size > 0:
        assert entry.out_datetimestamp is not None, entry
        entry = draw(
            entries(
                min_value=entry.out_datetimestamp,
                max_value=max_value,
                unfinished=EntryState.CLOSED if target_size > 1 else last_unfinished,
            )
        )
        assert target_size <= 1 or entry.out_datetimestamp is not None, entry
        yield entry
        target_size -= 1


@st.composite
def overlapping_entries(
    draw,
    *,
    min_size: int = 2,
    max_size: int | None = None,
    min_value: datetime.datetime = datetime.datetime.min,
    max_value: datetime.datetime = datetime.datetime.max,
    last_unfinished: EntryState = EntryState.UNDETERMINED,
) -> Iterable[lgbks.Entry]:
    if min_size < 2:
        raise ValueError(
            f"Cannot produce overlapping entries with less than 2 entries {min_size=}"
        )
    if max_size is None:
        max_size = draw(st.integers(min_value=min_size))
    assert max_size is not None

    entries_ = draw(
        st.lists(
            entries(unfinished=EntryState.CLOSED),
            min_size=min_size - 1,
            max_size=max_size - 1,
        )
    )
    entry = draw(st.sampled_from(entries_))
    assert entry is not None
    raise NotImplementedError
