# -*- coding: utf-8 -*-
"""
RDF Store for Gilded Rose inventory management.

This module provides utilities for converting Items to/from RDF representation
and performing quality updates using RDF/SPARQL operations.
"""

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD

# Define namespace for Gilded Rose ontology
GR = Namespace("http://example.org/gilded-rose#")


class RDFItemStore:

    def __init__(self):
        """Initialize the RDF graph and load schema."""
        self.graph = Graph()
        self.graph.bind("gr", GR)
        self._load_schema()
        # Map item type URIs to handler methods for modular updates
        self._handlers = {
            GR.Sulfuras: self._handle_sulfuras,
            GR.AgedBrie: self._handle_aged_brie,
            GR.BackstagePass: self._handle_backstage_pass,
            GR.Conjured: self._handle_conjured,
            GR.Normal: self._handle_normal,
        }

    def _load_schema(self):
        """Load the RDF schema from schema.ttl file."""
        self.graph.parse("python/schema.ttl", format="turtle")


    def item_to_rdf(self, item, item_id: int) -> URIRef:
        """
        Convert an Item object to RDF triples and add to graph.

        Args:
            item: The Item object to convert
            item_id: Unique identifier for the item

        Returns:
            URIRef: The URI of the created item resource

        """
        # Create a unique URI for the item
        item_uri = GR[f"item_{item_id}"]

        # Add triples for item properties
        self.graph.add((item_uri, RDF.type, GR.Item))
        self.graph.add((item_uri, GR.name, Literal(item.name, datatype=XSD.string)))
        self.graph.add((item_uri, GR.sellIn, Literal(item.sell_in, datatype=XSD.integer)))
        self.graph.add((item_uri, GR.quality, Literal(item.quality, datatype=XSD.integer)))

        # Determine and set the appropriate itemType based on name
        item_type = self._determine_item_type(item.name)
        self.graph.add((item_uri, GR.itemType, item_type))

        return item_uri

    def rdf_to_item(self, item_uri: URIRef, item):
        """
        Update an Item object with values from RDF graph.

        Args:
            item_uri: The URI of the item in the RDF graph
            item: The Item object to update

        """
        # Query the graph for sellIn and quality values
        sell_in_literal = self.graph.value(item_uri, GR.sellIn)
        quality_literal = self.graph.value(item_uri, GR.quality)

        # Update the item object (name should not change)
        if sell_in_literal is not None:
            item.sell_in = int(sell_in_literal)

        if quality_literal is not None:
            item.quality = int(quality_literal)

    def update_quality(self):
        """
        Update quality and sellIn values for all items in the graph.

        This method is modular: each item type has a handler that computes the
        new quality value given the current `sellIn` and `quality`. Handlers
        are registered in `self._handlers` so adding new types is straightforward.
        """
        for item_uri in self.graph.subjects(RDF.type, GR.Item):
            # Determine type (default to Normal if missing)
            item_type = self.graph.value(item_uri, GR.itemType) or GR.Normal

            # Fetch current values, with graceful defaults
            sell_in_literal = self.graph.value(item_uri, GR.sellIn)
            quality_literal = self.graph.value(item_uri, GR.quality)
            try:
                sell_in = int(sell_in_literal) if sell_in_literal is not None else 0
            except Exception:
                sell_in = 0
            try:
                quality = int(quality_literal) if quality_literal is not None else 0
            except Exception:
                quality = 0

            handler = self._handlers.get(item_type, self._handle_normal)

            # Sulfuras is legendary: no changes to sellIn or quality
            if handler == self._handle_sulfuras:
                continue

            # Compute new quality via the handler (handler uses pre-decrement sell_in)
            new_sell_in, new_quality = handler(sell_in, quality)

            # Decrease sellIn for all non-legendary items
            new_sell_in = sell_in - 1

            # Persist changes
            self.graph.set((item_uri, GR.sellIn, Literal(new_sell_in, datatype=XSD.integer)))
            self.graph.set((item_uri, GR.quality, Literal(new_quality, datatype=XSD.integer)))

    def _handle_sulfuras(self, sell_in: int, quality: int):
        return sell_in, quality

    def _handle_aged_brie(self, sell_in: int, quality: int):
        q = quality + 1
        if sell_in < 0:
            q += 1
        q = min(q, 50)
        return sell_in, q

    def _handle_backstage_pass(self, sell_in: int, quality: int):
        if sell_in < 0:
            q = 0
        else:
            q = quality + 1
            if sell_in <= 10:
                q += 1
            if sell_in <= 5:
                q += 1
            q = min(q, 50)
        return sell_in, q

    def _handle_conjured(self, sell_in: int, quality: int):
        q = quality - 2
        if sell_in < 0:
            q -= 2
        q = max(q, 0)
        return sell_in, q

    def _handle_normal(self, sell_in: int, quality: int):
        q = quality - 1
        if sell_in < 0:
            q -= 1
        q = max(q, 0)
        return sell_in, q

    def _determine_item_type(self, name: str) -> URIRef:
        """
        Determine the item type based on item name.

        Args:
            name: The name of the item

        Returns:
            URIRef: The item type URI

        """
        if "Conjured" in name:
            return GR.Conjured
        elif name == "Aged Brie":
            return GR.AgedBrie
        elif name == "Sulfuras, Hand of Ragnaros":
            return GR.Sulfuras
        elif "Backstage passes" in name:
            return GR.BackstagePass
        else:
            return GR.Normal
