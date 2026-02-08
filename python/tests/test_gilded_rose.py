# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        """Normal item: name unchanged, sell_in decreases, quality never negative."""
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

        
if __name__ == '__main__':
    unittest.main()
