# test_rdf.py
from rdf_store import RDFItemStore
from gilded_rose import Item
from rdflib import RDF, Literal, XSD, URIRef

def main():
    print("=== Script is running! ===")

    # Initialize RDF store
    store = RDFItemStore()

    # Step 1: Test _determine_item_type()
    items_names = [
        "Aged Brie",
        "Sulfuras, Hand of Ragnaros",
        "Backstage passes to a TAFKAL80ETC concert",
        "Conjured Mana Cake",
        "+5 Dexterity Vest"
    ]

    print("\n=== Testing _determine_item_type ===")
    for name in items_names:
        item_type = store._determine_item_type(name)
        print(f"{name} -> {item_type}")

    # Step 2: Create Python Item objects
    items_obj = [
        Item("Aged Brie", 2, 0),
        Item("Conjured Mana Cake", 3, 6),
        Item("+5 Dexterity Vest", 10, 20),
        Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
        Item("Sulfuras, Hand of Ragnaros", 0, 80)
    ]

    # Step 3: Convert items to RDF and store URIs
    print("\n=== Testing item_to_rdf ===")
    uris = []
    for i, item in enumerate(items_obj, start=1):
        uri = store.item_to_rdf(item, i)
        uris.append((item, uri))
        print(f"Item URI: {uri}")

    # Step 4: Update quality in RDF graph
    store.update_quality(items_obj)

    # Step 5: Pull updated values back to Python objects
    for item, uri in uris:
        store.rdf_to_item(item, uri)

    # Step 6: Print Python items after quality update
    print("\n=== Python Items After update_quality() ===")
    for item in items_obj:
        print(item)

    # Step 7: Serialize and print RDF graph
    print("\n=== Serialized RDF Graph (Turtle format) ===")
    print(store.graph.serialize(format="turtle"))

    # Save RDF graph to a file
    store.graph.serialize("inventory.ttl", format="turtle")
    print("\nRDF graph saved to inventory.ttl")

if __name__ == "__main__":
    main()