from unittest import TestCase
from unittest import mock
from unittest.mock import mock_open, patch

import logXchecker

valid_rules = """
[contest]
name=Cupa Nasaud
begindate=20170805
enddate=20170806
beginhour=1300
endhour=0900
bands=2
periods=2
categories=3

[log]
format=edi

[band1]
band=144
regexp=(144|145|2m)

[band2]
band=432
regexp=(430|432|435|70cm)

[period1]
begindate=20170805
enddate=20170805
beginhour=1300
endhour=1659
bands=band1,band2

[period2]
begindate=20170806
enddate=20170806
beginhour=0500
endhour=0859
bands=band1,band2

[category1]
name=Single Operator 144
regexp=(so|single)
bands=band1

[category2]
name=Single Operator 432
regexp=(so|single)
bands=band2

[category3]
name=Multi Operator
regexp=(mo|multi)
bands=band1,band2
"""

valid_rules_sections = ['contest', 'log', 'band1', 'band2', 'period1', 'period2', 'category1', 'category2', 'category3']


class TestRules(TestCase):
    @mock.patch('os.path.isfile')
    def test_init(self, mock_isfile):
        mock_isfile.return_value = True
        mo = mock.mock_open(read_data=valid_rules)
        with patch('builtins.open', mo, create=True):
            rules = logXchecker.Rules('some_rule_file.rules')

        self.assertEqual(rules.config.sections(), valid_rules_sections)
        self.assertEqual(rules.contest_begin_date, '20170805')

        self.assertEqual(rules.contest_end_date, '20170806')
        self.assertEqual(rules.contest_begin_hour, '1300')
        self.assertEqual(rules.contest_end_hour, '0900')

        self.assertEqual(rules.contest_bands_nr, 2)
        self.assertEqual(rules.contest_band(1)['band'], '144')
        self.assertEqual(rules.contest_band(2)['band'], '432')

        self.assertEqual(rules.contest_periods_nr, 2)
        self.assertEqual(rules.contest_period(1)['begindate'], '20170805')
        self.assertEqual(rules.contest_period(1)['enddate'], '20170805')
        self.assertEqual(rules.contest_period(1)['beginhour'], '1300')
        self.assertEqual(rules.contest_period(1)['endhour'], '1659')
        self.assertEqual(rules.contest_period(1)['bands'], 'band1,band2')
        self.assertEqual(list(rules.contest_period_bands(1)), ['band1', 'band2'])

        self.assertEqual(rules.contest_categories_nr, 3)
