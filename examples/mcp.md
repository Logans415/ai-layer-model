# Example: Model Context Protocol

Sources checked: October 20, 2026.

**Scope:** a protocol defining how applications connect to context-related resources/prompts and callable tools.

**Primary responsibilities in this model:** L5 Context / memory and L6 Tools / capabilities. A protocol can connect responsibilities; it need not be squeezed into one component layer.

A tool exposed by a server is a capability at L6. Information returned to a later model call can become L5 context. The protocol itself does not provide every connected model, runtime, user interface or underlying data store.

Authorization and trust boundaries are cross-cutting questions. The protocol label alone does not establish the connected system's security.

Official evidence: [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro). Placement is the AI Layer Model's interpretation; check the specification version and features in the deployment being discussed.
