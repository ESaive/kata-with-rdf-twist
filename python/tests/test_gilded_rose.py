# -*- coding: utf-8 -*-
import unittest
from rdf_store import RDFItemStore, GR
from gilded_rose import Item, GildedRose

def make_item_and_store(name, sell_in, quality, item_id=0):
        store = RDFItemStore()
        item = Item(name, sell_in, quality)
        uri = store.item_to_rdf(item, item_id)
        return store, item, uri

class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    def test_item_to_rdf_and_rdf_to_item_roundtrip(self):
        store, item, uri = make_item_and_store("Normal Item", 10, 20, item_id=1)

        # ensure triples were added
        assert (uri, None, None) in store.graph

        # Use rdf_to_item to populate an Item from the graph
        store.rdf_to_item(uri, item)

        # values should remain as originally set
        self.assertEqual(10, item.sell_in)
        self.assertEqual(20, item.quality)


    def test_update_quality_normal_item_degrades(self):
        store, item, uri = make_item_and_store("Normal Item", 5, 10, item_id=2)
        store.update_quality()

        # after one update, sellIn should decrease by 1 and quality by 1
        self.assertEqual(4, int(store.graph.value(uri, GR.sellIn)))
        self.assertEqual(9, int(store.graph.value(uri, GR.quality)))


    def test_update_quality_aged_brie_increases(self):
        store, item, uri = make_item_and_store("Aged Brie", 2, 0, item_id=3)
        store.update_quality()
        self.assertEqual(1, int(store.graph.value(uri, GR.quality)))


    def test_update_quality_sulfuras_unchanged(self):
        store, item, uri = make_item_and_store("Sulfuras, Hand of Ragnaros", 0, 80, item_id=4)
        store.update_quality()
        self.assertEqual(80, int(store.graph.value(uri, GR.quality)))
        self.assertEqual(0, int(store.graph.value(uri, GR.sellIn)))


    def test_update_quality_backstage_passes(self):
        store, item, uri = make_item_and_store("Backstage passes to a TAFKAL80ETC concert", 15, 20, item_id=5)
        store.update_quality()
        # increases by 1 when more than 10 days
        self.assertEqual(21, int(store.graph.value(uri, GR.quality)))


    def test_update_quality_conjured_degrades_twice(self):
        store, item, uri = make_item_and_store("Conjured Mana Cake", 3, 6, item_id=6)
        store.update_quality()
        # conjured degrades by 2
        self.assertEqual(4, int(store.graph.value(uri, GR.quality)))

        
if __name__ == '__main__':
    unittest.main()
