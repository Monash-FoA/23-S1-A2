import unittest
from ed_utils.decorators import number

from mountain import Mountain
from trail import Trail, TrailSeries, TrailSplit, TrailStore

class TestTrailMethods(unittest.TestCase):

    @number("1.1")
    def test_example(self):
        """See spec for details"""
        a, b, c, d = (Mountain(letter, 5, 5) for letter in "abcd")

        empty = Trail(None)

        series_b = TrailSeries(b, Trail(TrailSeries(d, Trail(None))))

        split = TrailSplit(
            Trail(series_b),
            empty,
            Trail(TrailSeries(c, Trail(None)))
        )

        t = Trail(TrailSeries(
            a,
            Trail(split)
        ))

        res1 = series_b.add_empty_branch_after()
        self.assertIsInstance(res1, TrailSeries)
        self.assertEqual(res1.mountain, b)
        self.assertIsInstance(res1.following.store, TrailSplit)
        self.assertEqual(res1.following.store.path_bottom.store, None)
        self.assertEqual(res1.following.store.path_top.store, None)
        self.assertEqual(res1.following.store.path_follow.store, TrailSeries(mountain=Mountain(name='d', difficulty_level=5, length=5), following=Trail(store=None)))

        res2 = split.remove_branch()
        self.assertIsInstance(res2, TrailSeries)
        self.assertEqual(res2.mountain, c)
        self.assertEqual(res2.following.store, None)

        res3 = empty.add_empty_branch_before()
        self.assertIsInstance(res3, Trail)
        self.assertIsInstance(res3.store, TrailSplit)
        self.assertEqual(res3.store.path_bottom.store, None)
        self.assertEqual(res3.store.path_top.store, None)
        self.assertEqual(res3.store.path_follow.store, None)

    @number("1.2")
    def test_empty(self):
        empty = Trail(None)
        m = Mountain("M", 1, 2)

        res1 = empty.add_mountain_before(m)

        self.assertIsInstance(res1, Trail)
        self.assertIsInstance(res1.store, TrailSeries)
        self.assertEqual(res1.store.mountain, m)
        self.assertEqual(res1.store.following.store, None)

        res2 = empty.add_empty_branch_before()
        self.assertIsInstance(res2, Trail)
        self.assertIsInstance(res2.store, TrailSplit)
        self.assertEqual(res2.store.path_bottom.store, None)
        self.assertEqual(res2.store.path_top.store, None)
        self.assertEqual(res2.store.path_follow.store, None)

    @number("1.3")
    def test_series(self):
        m = Mountain("M", 3, 4)
        empty = Trail(None)
        series = TrailSeries(m, empty)

        m2 = Mountain("I", 5, 6)

        res1 = series.add_mountain_after(m2)
        self.assertIsInstance(res1, TrailSeries)
        self.assertEqual(res1.mountain, m)
        self.assertIsInstance(res1.following.store, TrailSeries)
        self.assertEqual(res1.following.store.mountain, m2)

        res2 = series.add_mountain_before(m2)
        self.assertIsInstance(res2, TrailSeries)
        self.assertEqual(res2.mountain, m2)
        self.assertIsInstance(res2.following.store, TrailSeries)
        self.assertEqual(res2.following.store.mountain, m)

        res3 = series.add_empty_branch_after()
        self.assertIsInstance(res3, TrailSeries)
        self.assertEqual(res3.mountain, m)
        self.assertIsInstance(res3.following.store, TrailSplit)
        self.assertEqual(res3.following.store.path_bottom.store, None)
        self.assertEqual(res3.following.store.path_top.store, None)
        self.assertEqual(res3.following.store.path_follow.store, None)

        res4 = series.add_empty_branch_before()
        self.assertIsInstance(res4, TrailSplit)
        self.assertEqual(res4.path_bottom.store, None)
        self.assertEqual(res4.path_top.store, None)
        self.assertIsInstance(res4.path_follow.store, TrailSeries)
        self.assertEqual(res4.path_follow.store.mountain, m)

    @number("1.4")
    def test_split(self):
        m = Mountain("M", 7, 8)
        my_follow = TrailSeries(m, Trail(None))
        t = TrailSplit(Trail(None), Trail(None), Trail(my_follow))

        res = t.remove_branch()
        self.assertIsInstance(res, TrailSeries)
        self.assertEqual(res.mountain, m)
        self.assertEqual(res.following.store, None)
