# test_rdf.py

"""
Basic validation script for RDFItemStore.

This script verifies that items can be converted to RDF,
updated using SPARQL rules, and synchronized back to Python objects.
"""

from rdf_store import RDFItemStore
from gilded_rose import Item


def main():

    print("=== RDF Store Test ===\n")

    store = RDFItemStore()

    items = [
        Item("Aged Brie", 2, 0),
        Item("Conjured Mana Cake", 3, 6),
        Item("+5 Dexterity Vest", 10, 20),
        Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
        Item("Sulfuras, Hand of Ragnaros", 0, 80),
    ]

    print("Initial Items\n")

    for item in items:
        print(item)

    print("\nApplying RDF update rules...\n")

    store.update_quality(items)

    print("Items After RDF Update\n")

    for item in items:
        print(item)


if __name__ == "__main__":
    main()