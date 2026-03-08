# simulate_days.py
from rdf_store import RDFItemStore
from gilded_rose import Item

def main(days=10):
    print(f"=== Gilded Rose Simulation for {days} Days ===\n")

    # Initialize RDF store
    store = RDFItemStore()

    # Create initial items
    items = [
        Item("Aged Brie", 2, 0),
        Item("Conjured Mana Cake", 3, 6),
        Item("+5 Dexterity Vest", 10, 20),
        Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
        Item("Sulfuras, Hand of Ragnaros", 0, 80)
    ]

    # Print header
    print(f"{'Day':<4} | {'Item Name':<40} | {'SellIn':<6} | {'Quality':<7}")
    print("-"*65)

    # Run simulation
    for day in range(1, days + 1):
        # Update quality using RDF store
        store.update_quality(items)

        # Print current day items
        for item in items:
            print(f"{day:<4} | {item.name:<40} | {item.sell_in:<6} | {item.quality:<7}")
        print("-"*65)

    # Optional: save final RDF graph
    store.graph.serialize("inventory_final.ttl", format="turtle")
    print("\nRDF graph saved to inventory_final.ttl")

if __name__ == "__main__":
    main(days=15)  # simulate 15 days