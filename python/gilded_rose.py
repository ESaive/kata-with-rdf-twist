# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        # Use the RDF-backed item store to perform updates.
        # This wraps existing Item objects into an RDF graph, runs the RDF-based
        # update logic, then syncs the updated sell_in and quality values back
        # into the original Item instances.
        from rdf_store import RDFItemStore

        store = RDFItemStore()
        uri_item_pairs = []
        for idx, item in enumerate(self.items):
            uri = store.item_to_rdf(item, idx)
            uri_item_pairs.append((uri, item))

        # Perform RDF-based update
        store.update_quality()

        # Sync updated values back to Python Item objects
        for uri, item in uri_item_pairs:
            store.rdf_to_item(uri, item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
