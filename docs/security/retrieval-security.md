# RAG Retrieval Security & Document Authorization

## 1. Principle
Never retrieve unauthorized documents merely because they have high semantic similarity.
$$\text{User Request} \rightarrow \text{Zero-Trust Policy Filter} \rightarrow \text{Authorized Vector Query} \rightarrow \text{RAG Context} \rightarrow \text{Model}$$
