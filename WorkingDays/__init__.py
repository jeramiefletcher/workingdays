"""
    A Python package containing a collection of date utilities/helper
    functions.

IMPORTED FUNCTIONS:
    re
    datetime (timedelta, datetime)

FUNCTIONS:
    dateCleanup(datevalue, **kwargs)
    workday(datevalue, offset)
    calendarDay(datevalue, offset)
    workdayStart(datevalue, offset)
    compareWorkingdays(datevalue, comparedate)
    lastWorkdayofMonth(datevalue)
    lastWorkdayofQtr(datevalue, **kwargs)
    lastDayofMonth(datevalue)
    setSortValue(str)
    dateSort(DictObj)
    dateBucketing(startDT, interval, endDT=datetime.utcnow().strftime("%Y%m%d"))

MISC VARIABLES:
    __version__

"""
from ._version import version as __version__

__all__ = ["workingdays", "_version"]


def main():  # pragma: no cover
    printVersion = "version: {}"
    print(printVersion.format(__version__))


if __name__ == "__main__":  # pragma: no cover
    main()
