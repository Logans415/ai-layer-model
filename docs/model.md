# AI Layer Model — version 0.4.0

 Logan Smith · [Canonical repository](https://github.com/Logans415/ai-layer-model) · CC BY 4.0

 The model separates nine runtime responsibilities into three planes. It is inspired by the usefulness of a shared layered vocabulary in networking. It does **not** claim a one-to-one correspondence with OSI, prescribe a request execution sequence, or require every system to implement every responsibility as a separate component.

 | Layer | Responsibility | Plane | Job |
 |---|---|---|---|
 | L9 | Interface / delivery | Systems | Deliver the system and its results to people or other systems. |
| L8 | Orchestration | Systems | Coordinate distinct parts, models, agents or workstreams. |
| L7 | Agentic control loop | Systems | Decide the next action, continuation and stop condition. |
| L6 | Tools / capabilities | Cognition | Expose capabilities a model-driven system can request. |
| L5 | Context / memory | Cognition | Supply the information available to a model call. |
| L4 | Inference strategy / reasoning | Cognition | Shape how a model call is run. |
| L3 | Model | Cognition | Provide the trained model capability. |
| L2 | Runtime / inference engine | Substrate | Load, schedule, execute and serve a model. |
| L1 | Hardware / compute | Substrate | Provide the physical capacity to execute work. |

 Governance, identity and authorization, safety, evaluation, observability, and resource limits cross the stack. They do not become a tenth runtime layer.

 ## Boundaries that matter

 ### L1: Hardware / compute

**What hardware runs it?** Processors, accelerators, memory, storage and the physical execution environment.

### L2: Runtime / inference engine

**What loads and runs the model?** Model loading, execution kernels, batching, scheduling and serving. A managed service still has these responsibilities.

### L3: Model

**Which model is doing the work?** The model architecture, weights and released artifact. A model call is an operation using the model, not the definition of this layer.

### L4: Inference strategy / reasoning

**How are we using the model for this call?** Supported decoding settings, prompting strategies and reasoning or output budgets. Capabilities depend on the selected model; reasoning capability can also be a property of L3.

### L5: Context / memory

**What information can it see?** Instructions, conversation, retrieved content, returned tool results and relevant stored state. Persistent memory is optional.

### L6: Tools / capabilities

**What can it request or do beyond generating text?** Functions, APIs, retrieval, file operations and other capabilities. The tool is the capability; its returned information may become L5 context. Enforcement remains with the application and tool.

### L7: Agentic control loop

**What decides the next step or when to stop?** Goal-directed control, observation, decisions and termination. This is one responsibility in an agent, not the entire assembled agent or its user interface.

### L8: Orchestration

**What coordinates the work?** Routing, delegation, workflow coordination, handoffs and shared-state coordination. Multiple agents are optional; distinguish coordination from a single control loop.

### L9: Interface / delivery

**How is the result used or delivered?** Chat, application surfaces, client rendering, integrations and delivered endpoints. An endpoint may also expose L2 serving; inspect its actual responsibility.

 ## A task through the map

 Consider a hypothetical request: “Find a time and draft a meeting invite.” The selected model is L3. Supported call settings are L4. The request, attendees and returned availability information are L5. A calendar lookup capability is L6. The application, not the model text itself, invokes the lookup under the applicable permissions.

 A control loop at L7 can decide whether to request availability, draft, continue or stop. If scheduling and drafting are separate coordinated workstreams, that coordination is L8. The chat where the draft appears is L9. This example drafts an invite for review; it does not imply permission to send one or access any real calendar.

 The same result can pass through more than one model call. The returned calendar data can become context for another call. These are responsibilities and handoffs, not a numbered conveyor belt.

 ## Components, protocols and assembled systems

 A component can have a useful primary anchor. A protocol can connect responsibilities. A product can assemble many layers. Ask what the item does, what it depends on and what it can reach. A product's dependency on a model or a GPU does not mean the product provides model weights or owns physical compute.

 A typical tool-using agent combines a model, a way of using it, context, tools and a control loop. Its exact design can vary. Persistent memory, tool use, autonomy and multi-agent orchestration are choices. L7 names the control responsibility; it does not rename the entire agent or its interface.

 ## The build and training companion

 The runtime view starts with a released model artifact. A companion view covers B1 Compute, B2 Frameworks, B3 Data, B4 Pretraining, B5 Fine-tuning/alignment, B6 Evaluation, and B7 Registry/release. The released artifact becomes the runtime L3 model. Frameworks and platforms may participate in both views; classify the activity and deployment being discussed.

 ## Using the map for security

 Place a component, trace a task, identify the operators and decision owners, then examine a boundary. Unsafe artifact loading, hostile retrieved content, excessive tool authority and unsafe downstream handling have different control points. An attack path can cross several of them.

 The map helps locate questions and responsibilities. A placement does not demonstrate that a system is safe, determine incident likelihood, or substitute for threat modeling, authorization checks or verification of controls. Risk taxonomies such as the [OWASP GenAI LLM Top 10](https://genai.owasp.org/llm-top-10/) can complement the architecture view.

 ## Scope and revision

 These are working boundaries. A useful mapping states its scope, version and evidence, and can name unresolved boundaries. See [related work](related-work.md), [mapping examples](../examples/), and [contribution guidance](../CONTRIBUTING.md).

 Machine-readable definitions: [layers.json](../model/layers.json). The skill contains an explicitly versioned copy for offline portability; release validation checks that the two copies are identical.
