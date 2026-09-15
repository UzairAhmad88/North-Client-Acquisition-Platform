# Infrastructure Resource Graph & Dependency Mapping
Establishes bidirectional edges:
```text
Project → owns → Service → deployed_on → Cluster → contains → Node → runs → Workload → uses → Database
```
Powers real-time upstream and downstream impact queries.
