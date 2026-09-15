# Process Discovery and Model Mining

## Algorithms
The Discovery Engine reconstructs workflow topologies directly from event streams:
1. **Directly-Follows Graphs (DFG)**: Frequency and duration matrix between consecutive activity pairs.
2. **Inductive Miner & Alpha Miner**: Constructs block-structured process trees guaranteed to be sound and deadlock-free.
3. **Petri Net Synthesis**: Translates mined behaviors into Place/Transition nets with token replay semantics.
4. **BPMN 2.0 Generation**: Emits industry-standard XML/JSON BPMN definitions with gateways, swimlanes, and conditional flows.\n