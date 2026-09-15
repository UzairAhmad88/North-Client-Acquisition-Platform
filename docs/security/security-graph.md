# Security Knowledge Graph & Blast Radius

## 1. Graph Relationships
Models the entire security topology:
- `(User) -[:AUTHENTICATES_VIA]-> (Device)`
- `(User) -[:ACCESSES]-> (Application)`
- `(Application) -[:QUERIES]-> (Dataset)`
- `(Threat) -[:TARGETS]-> (Asset)`
- `(Asset) -[:EXPOSES]-> (Vulnerability)`
