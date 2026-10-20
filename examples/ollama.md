# Example: Ollama

Sources checked: October 20, 2026.

**Scope:** the core role of running and serving models, rather than every possible integration.

**Primary anchor:** L2 Runtime / inference engine. Model loading and serving are the responsibilities being placed.

**Dependencies:** the model selected by the user is L3; physical compute is L1. Those dependencies do not make the core runtime role into the provider of all model weights or hardware.

Tool-calling and other integrations may connect further responsibilities. An assessment of a particular deployment should verify which features are present rather than treating this primary anchor as an exhaustive inventory.

Official evidence: [Ollama documentation](https://docs.ollama.com/) and [API introduction](https://docs.ollama.com/api/introduction). Placement is the AI Layer Model's interpretation. Recheck the deployed version when applying the example.
