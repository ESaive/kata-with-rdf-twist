# simulate_days.py

"""
Simulation script for the Gilded Rose inventory.

This script runs the inventory update logic for a specified number
of days and prints the inventory status.

Recommended usage via Makefile:

    make simulate DAYS=3
"""

import sys
from gilded_rose import Item, GildedRose


def main(days=10):

    print(f"=== Gilded Rose Simulation for {days} Days ===\n")

    items = [
        Item("Aged Brie", 2, 0),
        Item("Conjured Mana Cake", 3, 6),
        Item("+5 Dexterity Vest", 10, 20),
        Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
        Item("Sulfuras, Hand of Ragnaros", 0, 80),
    ]

    gilded_rose = GildedRose(items)

    print(f"{'Day':<4} | {'Item Name':<40} | {'SellIn':<6} | {'Quality':<7}")
    print("-" * 65)

    for day in range(1, days + 1):

        gilded_rose.update_quality()

        for item in items:
            print(
                f"{day:<4} | {item.name:<40} | {item.sell_in:<6} | {item.quality:<7}"
            )

        print("-" * 65)


if __name__ == "__main__":

    days = 10

    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            pass

    main(days)