# Example: a hypothetical meeting assistant

Request: “Find a time and draft a meeting invite.” This is a design example, not a claim about access to a real calendar.

| Responsibility | Placement |
|---|---|
| Selected model | L3 |
| Supported call settings | L4 |
| Request, attendees and returned availability | L5 |
| Calendar lookup capability | L6 |
| Decide whether to look up, draft, continue or stop | L7 |
| Coordinate separate scheduling and drafting workstreams, if the design has them | L8, conditional |
| Show the draft for review | L9 |

Model serving and compute remain dependencies unless the described product also provides them. The result can re-enter context for another model call. Drafting an invite does not grant permission to send one.

These placements follow the supplied design assumptions. A different implementation can divide the responsibilities differently.
