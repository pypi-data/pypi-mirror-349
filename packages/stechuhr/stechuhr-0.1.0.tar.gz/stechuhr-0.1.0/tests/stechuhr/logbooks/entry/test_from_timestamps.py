import datetime

import pytest

from stechuhr import logbooks as lgbks

import hypothesis as hyp
from hypothesis import strategies as st

from stechuhr.errors import InAfterOutError


def test__in_1970_1_1_0_0_0_out_none() -> None:
    in_datetimestamp = datetime.datetime(1970, 1, 1, 0, 0, 0)
    out_datetimestamp = None
    expected = lgbks.Entry(
        in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
    )

    actual = lgbks.Entry.from_datetimestamps(
        in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
    )

    assert actual == expected


def test__in_1970_1_1_0_0_0_out_2000_12_31_12_31_59() -> None:
    in_datetimestamp = datetime.datetime(1970, 1, 1, 0, 0, 0)
    out_datetimestamp = datetime.datetime(2000, 12, 31, 12, 31, 59)
    expected = lgbks.Entry(
        in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
    )

    actual = lgbks.Entry.from_datetimestamps(
        in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
    )

    assert actual == expected


@hyp.given(st.datetimes(), st.datetimes())
def test__in_before_out(fst_datetimestamp, snd_datetimestamp) -> None:
    in_datetimestamp, out_datetimestamp = sorted((fst_datetimestamp, snd_datetimestamp))
    expected = lgbks.Entry(
        in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
    )

    actual = lgbks.Entry.from_datetimestamps(
        in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
    )

    assert actual == expected


def test__in__2000_12_31_12_31_59_out_1970_1_1_0_0_0__raises_in_after_out_error() -> (
    None
):
    in_datetimestamp = datetime.datetime(2000, 12, 31, 12, 31, 59)
    out_datetimestamp = datetime.datetime(1970, 1, 1, 0, 0, 0)

    with pytest.raises(InAfterOutError):
        lgbks.Entry.from_datetimestamps(
            in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
        )


@hyp.given(st.datetimes(), st.datetimes())
def test__in_after_out__raises_in_after_out_error(
    fst_datetimestamp, snd_datetimestamp
) -> None:
    hyp.assume(fst_datetimestamp != snd_datetimestamp)
    in_datetimestamp, out_datetimestamp = sorted(
        (fst_datetimestamp, snd_datetimestamp), reverse=True
    )

    with pytest.raises(InAfterOutError):
        lgbks.Entry.from_datetimestamps(
            in_datetimestamp=in_datetimestamp, out_datetimestamp=out_datetimestamp
        )
