import unittest
import pytest
import WorkingDays.date_utilities as wd
from WorkingDays.tests._test_setup import printVersion

# set test case version
__version__ = "220611"


def main():
    return printVersion(__version__, wd.__name__, wd.__version__)


class mainTests(unittest.TestCase):
    def test_printVersion(self):
        __testtestversion__ = __version__
        __testname__ = wd.__name__
        __testversion__ = wd.__version__
        assert printVersion(__version__, wd.__name__, wd.__version__) == printVersion(
            __testtestversion__, __testname__, __testversion__
        )
        self.assertEqual(
            printVersion(__version__, wd.__name__, wd.__version__),
            printVersion(__testtestversion__, __testname__, __testversion__),
        )



class DateCleanupTests(unittest.TestCase):
    def test_epochFormat(self):
        self.assertEqual(
            wd.dateCleanup(1571824800000, epoch=True).strftime("%Y%m%d%H%M%S"),
            "20191023100000",
        )

    def test_TZFormat(self):
        self.assertEqual(
            wd.dateCleanup("2015-03-26T10:58:51Z").strftime("%Y%m%d%H%M%S"),
            "20150326105851",
        )

    def test_germanDateFormat(self):
        self.assertEqual(
            wd.dateCleanup("07.04.2020").strftime("%Y%m%d%H%M%S"), "20200407000000"
        )

    def test_germanDateFormatWithTime(self):
        self.assertEqual(
            wd.dateCleanup("07.04.2020 12:12:12").strftime("%Y%m%d%H%M%S"),
            "20200407121212",
        )

    def test_alphaDateFormat(self):
        self.assertEqual(
            wd.dateCleanup("march 25, 2020").strftime("%Y%m%d%H%M%S"), "20200325000000"
        )

    def test_alphaDateShortFormat(self):
        self.assertEqual(
            wd.dateCleanup("MAR 25 2020").strftime("%Y%m%d%H%M%S"), "20200325000000"
        )

    def test_DateWithTimeFormat(self):
        self.assertEqual(
            wd.dateCleanup("2020-02-28 12:30:00").strftime("%Y%m%d%H%M%S"),
            "20200228123000",
        )

    def test_DateWithTimeNoSeparationFormat(self):
        self.assertEqual(
            wd.dateCleanup("2020-02-2812:30:00").strftime("%Y%m%d%H%M%S"),
            "20200228123000",
        )

    def test_DateWithColonTimeNoSeparationFormat(self):
        self.assertEqual(
            wd.dateCleanup("2020:02:2812:30:00").strftime("%Y%m%d%H%M%S"),
            "20200228123000",
        )

    def test_DayLessThanTwelve(self):
        self.assertEqual(
            wd.dateCleanup("2020-02-05").strftime("%Y%m%d%H%M%S"), "20200205000000"
        )

    def test_DateString(self):
        self.assertEqual(
            wd.dateCleanup("20200205110000").strftime("%Y%m%d%H%M%S"), "20200205110000"
        )

    def test_DateString_Ymd(self):
        self.assertEqual(
            wd.dateCleanup("20200205").strftime("%Y%m%d%H%M%S"), "20200205000000"
        )


class WorkdayTests(unittest.TestCase):
    def test_WorkdayWeekendBetweenOffset(self):
        self.assertEqual(wd.workday("08.04.2020", 3), "20200413")

    def test_WorkdayNoWeekendBetweenOffset(self):
        self.assertEqual(wd.workday("20200408", 2), "20200410")

    def test_WorkdayWeekendBetweenOffsetWithHolidays(self):
        self.assertEqual(wd.workday("20200701", 1, holidays=["20200702"]), "20200703")

    def test_WorkdayNoWeekendBetweenOffsetWithHolidays(self):
        self.assertEqual(
            wd.workday("20200702", 3, holidays=["20200703", "20200706"]), "20200709"
        )

    def test_WorkdayFridayStart(self):
        self.assertEqual(wd.workday("10.04.2020", 3), "20200415")

    def test_WorkdaySaturdayStart(self):
        self.assertEqual(wd.workday("11.04.2020", 3), "20200415")

    def test_WorkdaySundayStart(self):
        self.assertEqual(wd.workday("11.04.2020", 3), "20200415")


class CompareWorkdayStartTests(unittest.TestCase):
    def test_workdayStartWeekendBetweenOffset(self):
        self.assertEqual(wd.workdayStart("20200707", 3), "20200702")

    def test_workdayStartNoWeekendBetweenOffset(self):
        self.assertEqual(wd.workdayStart("20200710", 3), "20200707")

    def test_workdayStartWeekendBetweenOffsetWithHolidays(self):
        self.assertEqual(
            wd.workdayStart("20200707", 3, holidays=["20200703", "20200706"]),
            "20200630",
        )

    def test_workdayStartNoWeekendBetweenOffsetWithHolidays(self):
        self.assertEqual(
            wd.workdayStart("20200703", 1, holidays=["20200702"]), "20200701"
        )


class CompareWorkingDaysTests(unittest.TestCase):
    def test_compareWorkingDaysWeekendBetweenOffset(self):
        self.assertEqual(wd.compareWorkingDays("08.04.2020", "20200413"), 3)

    def test_compareWorkingDaysNegativeCompare(self):
        self.assertEqual(wd.compareWorkingDays("20200419", "20200413"), 0)

    def test_compareWorkingDaysNoWeekendBetweenOffset(self):
        self.assertEqual(wd.compareWorkingDays("20200408", "20200410"), 2)

    def test_compareWorkingDaysWeekendBetweenOffsetWithHolidays(self):
        self.assertEqual(
            wd.compareWorkingDays("20200701", "20200703", holidays=["20200702"]), 1
        )

    def test_compareWorkingDaysNoWeekendBetweenOffsetWithHolidays(self):
        self.assertEqual(
            wd.compareWorkingDays("20200701", "20200707", holidays=["20200703"]), 3
        )


class CompareLastWorkdayOfMonthTests(unittest.TestCase):
    def test_lastWorkdayOfMonthFeb(self):
        self.assertEqual(wd.lastWorkdayOfMonth("20200213"), "20200228")

    def test_lastWorkdayOfMonthLastDayNotWeekend(self):
        self.assertEqual(wd.lastWorkdayOfMonth("20200413"), "20200430")

    def test_lastWorkdayOfMonthLastDayWeekend(self):
        self.assertEqual(wd.lastWorkdayOfMonth("20200513"), "20200529")

    def test_lastWorkdayOfMonthLastDayHoliday(self):
        self.assertEqual(
            wd.lastWorkdayOfMonth("20200701", holidays=["20200730", "20200731"]),
            "20200729",
        )


class CompareLastWorkDayOfQtrTests(unittest.TestCase):
    quarters = {
        "Q1": ["Nov", "Dec", "Jan"],
        "Q2": ["Feb", "Mar", "Apr"],
        "Q3": ["May", "Jun", "Jul"],
        "Q4": ["Aug", "Sep", "Oct"],
    }

    def test_CalendarQtr(self):
        self.assertEqual(wd.lastWorkdayOfQtr("20200213"), "20200331")

    def test_FiscalQtr(self):
        self.assertEqual(wd.lastWorkdayOfQtr("20200213", key=self.quarters), "20200430")

    def test_FiscalQtrList(self):
        self.assertEqual(
            wd.lastWorkdayOfQtr(
                "20200213", Q1=["Nov", "Dec", "Jan"], Q2=["Feb", "Mar", "Apr"]
            ),
            "20200430",
        )

    def test_FiscalQtrEndsOnWeekend(self):
        self.assertEqual(wd.lastWorkdayOfQtr("20200913", key=self.quarters), "20201030")

    def test_FiscalQtrEndsOnHoliday(self):
        self.assertEqual(
            wd.lastWorkdayOfQtr(
                "20200213", holidays=["20200430", "20200731"], key=self.quarters
            ),
            "20200429",
        )


class CompareLastDayOfMonthTests(unittest.TestCase):
    def test_Feb(self):
        self.assertEqual(wd.lastDayOfMonth("20200213"), "20200229")

    def test_LastDay31(self):
        self.assertEqual(wd.lastDayOfMonth("20200313"), "20200331")

    def test_LastDay30(self):
        self.assertEqual(wd.lastDayOfMonth("20200413"), "20200430")


if __name__ == "__main__":  # pragma: no cover
    main()

suites = []
tests = [
    mainTests,
    DateCleanupTests,
    WorkdayTests,
    CompareWorkdayStartTests,
    CompareWorkingDaysTests,
    CompareLastWorkdayOfMonthTests,
    CompareLastWorkDayOfQtrTests,
    CompareLastDayOfMonthTests,
]
for test_class in tests:  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    suites.append(suite)
big_suite = unittest.TestSuite(suites)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(big_suite)
