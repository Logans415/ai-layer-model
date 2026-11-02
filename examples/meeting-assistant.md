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

Suppose the calendar tool is available, but the caller lacks permission
to read a particular calendar. The application or calendar service
denies the lookup. The lookup capability remains L6; IAM describes the
access control enforced at that boundary.

If the denial is supplied to a model call, it becomes L5 context.
The L7 control loop then chooses an allowed next step: asking the user
to resolve access, drafting without claiming verified availability,
or stopping. A denied lookup does not necessarily terminate the
entire task.

Model serving and compute remain dependencies unless the described product also provides them. The result can re-enter context for another model call. Drafting an invite does not grant permission to send one.

These placements follow the supplied design assumptions. A different implementation can divide the responsibilities differently.
