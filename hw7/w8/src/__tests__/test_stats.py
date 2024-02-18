from DATA import DATA

class StatsTestSuite:
    def setup(self):
        self.filename = "../data/auto93.csv"
        self.d = DATA(self.file)

    def should_match_stats_value(self):
        assert self.d.stats(ndivs=2) == "{'.N': 398, 'Lbs-': 2970.42, 'Acc+': 15.57, 'Mpg+': 23.84}"
