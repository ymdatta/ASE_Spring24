import unittest
import sys
import random
sys.path.append("../src")
from src.DATA import DATA

class DataTestSuite(unittest.TestCase):
    def test_add_row(self):
        data = DATA()
        row_data = {'Clndrs': 8, 'Volume': 304, 'HpX': 193, 'Model': 70, 'origin': 1, 'Lbs-': 4732, 'Acc+': 18.5, 'Mpg+': 10}
        data.add(row_data)
        self.assertEqual(len(data.rows), 1)
        self.assertIsNotNone(data.cols)

    def test_stats(self):
        data = DATA()
        row_data1 = {'Clndrs': 8, 'Volume': 304, 'HpX': 193, 'Model': 70, 'origin': 1, 'Lbs-': 4732, 'Acc+': 18.5, 'Mpg+': 10}
        row_data2 = {'Clndrs': 6, 'Volume': 280, 'HpX': 180, 'Model': 65, 'origin': 2, 'Lbs-': 4000, 'Acc+': 20.0, 'Mpg+': 12}
        data.add(row_data1)
        data.add(row_data2)
        stats_result = data.stats()
        self.assertEqual(stats_result['.N'], 2)
        self.assertEqual(stats_result['Clndrs'], 7)
        self.assertEqual(stats_result['Volume'], 292)

    def test_csv_parsing(self):
        csv_data = "8,304,193,70,1,4732,18.5,10\n6,280,180,65,2,4000,20.0,12"
        data = DATA(src=csv_data)
        self.assertEqual(len(data.rows), 2)
        self.assertIsNotNone(data.cols)

    def test_clone(self):
        data = DATA()
        original_row = {'Clndrs': 8, 'Volume': 304, 'HpX': 193, 'Model': 70, 'origin': 1, 'Lbs-': 4732, 'Acc+': 18.5, 'Mpg+': 10}
        data.add(original_row)
        cloned_data = data.clone()
        self.assertEqual(len(cloned_data.rows), 1)
        self.assertIsNotNone(cloned_data.cols)
        self.assertEqual(cloned_data.rows[1].data, original_row)

    def test_mid(self):
        data = DATA()
        row_data1 = {'Clndrs': 8, 'Volume': 304, 'HpX': 193, 'Model': 70, 'origin': 1, 'Lbs-': 4732, 'Acc+': 18.5, 'Mpg+': 10}
        row_data2 = {'Clndrs': 6, 'Volume': 280, 'HpX': 180, 'Model': 65, 'origin': 2, 'Lbs-': 4000, 'Acc+': 20.0, 'Mpg+': 12}
        data.add(row_data1)
        data.add(row_data2)
        mid_result = data.mid()
        self.assertIsInstance(mid_result, ROW)

    def test_div(self):
        data = DATA()
        row_data1 = {'Clndrs': 8, 'Volume': 304, 'HpX': 193, 'Model': 70, 'origin': 1, 'Lbs-': 4732, 'Acc+': 18.5, 'Mpg+': 10}
        row_data2 = {'Clndrs': 6, 'Volume': 280, 'HpX': 180, 'Model': 65, 'origin': 2, 'Lbs-': 4000, 'Acc+': 20.0, 'Mpg+': 12}
        data.add(row_data1)
        data.add(row_data2)
        div_result = data.div()
        self.assertIsInstance(div_result, ROW)

    def test_small(self):
        data = DATA()
        row_data1 = {'Clndrs': 8, 'Volume': 304, 'HpX': 193, 'Model': 70, 'origin': 1, 'Lbs-': 4732, 'Acc+': 18.5, 'Mpg+': 10}
        data.add(row_data1)
        small_result = data.small()
        self.assertIsInstance(small_result, ROW)

    def test_ltod(self):
        data = DATA()
        list_data = [10, 'example', 3.14]
        ltod_result = data._ltod(list_data)
        self.assertIsInstance(ltod_result, dict)
        self.assertEqual(len(ltod_result), len(list_data))
        for i, value in enumerate(list_data):
            self.assertEqual(ltod_result[i + 1], value)

    def test_shuffle(self):
        data = DATA("../../data/auto93.csv")
        rows = list(data.rows.values())
        shuffled1 = rows.copy()
        random.shuffle(shuffled1)
        self.assertNotEqual(rows,shuffled1)
        shuffled2 = rows.copy()
        random.shuffle(shuffled2)
        self.assertNotEqual(shuffled1,shuffled2)

    def test_b_r(self):
        data = DATA("../../data/auto93.csv")
        rows = list(data.rows.values())
        lite = rows[0:5]
        dark = rows[5:]
        some = len(lite)**0.5
        self.assert(some < len(lite))
        best,rest = data.bestRest(lite,some)
        self.assertEqual(len(best),some)
        self.assertEqual(len(rest),len(rows) - len(lite)**0.5)
        for i,row in enumerate(dark):
            b = row.like(best,len(lite),2)
            r = row.like(rest,len(lite),2)
            break
        self.assertIsInstance(b,(int,float))
        self.assertIsInstance(r,(int,float))
        todo,selected = data.split(best,rest,lite,dark)
        self.assert(len(todo) > 0)
        self.assert(len(selected) > 0)


    def test_split(self):


if __name__ == '__main__':
    unittest.main()
