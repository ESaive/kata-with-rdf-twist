# RDF Implementation – Gilded Rose Kata

## Overview

This project extends the classic Gilded Rose Kata by storing the inventory using RDF (Resource Description Framework). Instead of relying only on in-memory structures, item data is represented as RDF triples using the **rdflib** Python library.

The goal is to demonstrate how semantic data models can integrate with application logic.

---

## Key Components

### RDF Store

The module `rdf_store.py` manages the RDF graph.

It is responsible for:

* Initializing the RDF graph
* Loading the schema (`schema.ttl`)
* Storing item properties as RDF triples
* Updating item values
* Exporting the graph to Turtle format

---

### RDF Schema

The schema is defined in:

```
schema.ttl
```

It defines:

* `Item` class
* `name` property
* `sellIn` property
* `quality` property

This provides a semantic structure for representing inventory items.

---

### Simulation Script

The file:

```
simulate_days.py
```

runs a multi-day simulation of the inventory updates.

Run with:

```
python simulate_days.py
```

The script prints the daily inventory status and exports the RDF graph.

---

### RDF Output

After the simulation completes, the RDF graph is saved as:

```
inventory_final.ttl
```

This file contains the final inventory state in Turtle format.

---

## Technologies Used

* Python
* rdflib
* RDF / Turtle serialization

---

## Result

The system now supports storing and exporting inventory data as RDF while preserving the original Gilded Rose business rules.
