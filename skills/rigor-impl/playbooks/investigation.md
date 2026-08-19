### Investigation

**You own the answer. Plan, route, write.**

Read-only requests: "how does X work?", "why was Y built this way?", "are we sure about Z?", "should we do X or Y?". They produce a cited explanation or a recommendation, not a code change.

1. Route through `references/how.md` (Explain mode for narrow questions, Critique mode for "are we sure?"). For motivation questions, also route through `references/why.md`.
2. Throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only investigation`. The four-item version is for code-shaped work.
3. Produce the how-shaped output (Overview / Key concepts / How it works / Where things live / Gotchas), or a recommendation with a tradeoffs table if the request is a decision between alternatives.
4. Apply `references/unslop.md` to the reply.

Do not implement or run Architect unless the investigation precedes a code change. If it does, hand back to the user and re-route to Bug fix or Feature.

**Reply:** the investigation output. For "are we sure?" answers, include your real judgment with reasons. Push back if the premise is wrong (see Autonomy).
