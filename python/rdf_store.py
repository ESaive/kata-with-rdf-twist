# -*- coding: utf-8 -*-
"""
RDF Store for Gilded Rose inventory management.
"""

import os
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD


class RDFItemStore:
    """
    Manages items as RDF triples and updates them using SPARQL rules.
    """

    def __init__(self, schema_path=None):
        self.graph = Graph()

        self.GR = Namespace("http://example.org/gilded-rose#")
        self.graph.bind("gr", self.GR)

        if schema_path is None:
            schema_path = os.path.join(os.path.dirname(__file__), "schema.ttl")

        self.graph.parse(schema_path, format="turtle")

    # Convert Python Item -> RDF
    def item_to_rdf(self, item, index):
        uri = URIRef(f"http://example.org/item/{index}")

        self.graph.add((uri, RDF.type, self.GR.Item))
        self.graph.add((uri, self.GR.name, Literal(item.name)))
        self.graph.add((uri, self.GR.sellIn, Literal(item.sell_in, datatype=XSD.integer)))
        self.graph.add((uri, self.GR.quality, Literal(item.quality, datatype=XSD.integer)))

        if item.name == "Aged Brie":
            item_type = self.GR.AgedBrie
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            item_type = self.GR.BackstagePass
        elif item.name == "Sulfuras, Hand of Ragnaros":
            item_type = self.GR.Sulfuras
        elif "Conjured" in item.name:
            item_type = self.GR.Conjured
        else:
            item_type = self.GR.NormalItem

        self.graph.add((uri, self.GR.itemType, item_type))
        return uri

    # Convert RDF -> Python Item
    def rdf_to_item(self, item, uri):
        sell_in = self.graph.value(uri, self.GR.sellIn)
        quality = self.graph.value(uri, self.GR.quality)

        if sell_in is not None:
            item.sell_in = int(sell_in)

        if quality is not None:
            item.quality = int(quality)

    # Decrease sellIn (except Sulfuras)
    def _update_sellin(self):
        self.graph.update("""
        PREFIX gr: <http://example.org/gilded-rose#>

        DELETE { ?item gr:sellIn ?s }
        INSERT { ?item gr:sellIn ?newS }
        WHERE {
            ?item gr:sellIn ?s .
            ?item gr:itemType ?type .
            FILTER (?type != gr:Sulfuras)
            BIND(?s - 1 AS ?newS)
        }
        """)

    # Normal items
    def _update_normal_items(self):
        self.graph.update("""
        PREFIX gr: <http://example.org/gilded-rose#>

        DELETE { ?item gr:quality ?q }
        INSERT { ?item gr:quality ?newQ }
        WHERE {
            ?item gr:itemType gr:NormalItem .
            ?item gr:quality ?q .
            ?item gr:sellIn ?s .

            BIND(IF(?s < 0, ?q - 2, ?q - 1) AS ?tempQ)
            BIND(IF(?tempQ < 0, 0, ?tempQ) AS ?newQ)
        }
        """)

    # Aged Brie
    def _update_aged_brie(self):
        self.graph.update("""
        PREFIX gr: <http://example.org/gilded-rose#>

        DELETE { ?item gr:quality ?q }
        INSERT { ?item gr:quality ?newQ }
        WHERE {
            ?item gr:itemType gr:AgedBrie .
            ?item gr:quality ?q .
            ?item gr:sellIn ?s .

            BIND(IF(?s < 0, ?q + 2, ?q + 1) AS ?tempQ)
            BIND(IF(?tempQ > 50, 50, ?tempQ) AS ?newQ)
        }
        """)

    # Backstage passes
    def _update_backstage(self):
        self.graph.update("""
        PREFIX gr: <http://example.org/gilded-rose#>

        DELETE { ?item gr:quality ?q }
        INSERT { ?item gr:quality ?newQ }
        WHERE {
            ?item gr:itemType gr:BackstagePass .
            ?item gr:quality ?q .
            ?item gr:sellIn ?s .

            BIND(
                IF(?s < 0, 0,
                    IF(?s < 5, ?q + 3,
                        IF(?s < 10, ?q + 2,
                            ?q + 1)))
                AS ?tempQ
            )

            BIND(IF(?tempQ > 50, 50, ?tempQ) AS ?newQ)
        }
        """)

    # Conjured items
    def _update_conjured(self):
        self.graph.update("""
        PREFIX gr: <http://example.org/gilded-rose#>

        DELETE { ?item gr:quality ?q }
        INSERT { ?item gr:quality ?newQ }
        WHERE {
            ?item gr:itemType gr:Conjured .
            ?item gr:quality ?q .
            ?item gr:sellIn ?s .

            BIND(IF(?s < 0, ?q - 4, ?q - 2) AS ?tempQ)
            BIND(IF(?tempQ < 0, 0, ?tempQ) AS ?newQ)
        }
        """)

    # Main update function
    def update_quality(self, items):

        self.graph.update("""
        PREFIX gr: <http://example.org/gilded-rose#>
        DELETE { ?s ?p ?o }
        WHERE  { ?s a gr:Item ; ?p ?o }
        """)

        uris = []

        for i, item in enumerate(items):
            uri = self.item_to_rdf(item, i)
            uris.append((item, uri))

        self._update_sellin()
        self._update_normal_items()
        self._update_aged_brie()
        self._update_backstage()
        self._update_conjured()

        for item, uri in uris:
            self.rdf_to_item(item, uri)