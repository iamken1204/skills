---
name: probing
description: "Investigates how code works, why it was designed that way, and whether its architecture holds up. Use for read-only code explanations, code archaeology, design rationale, and architecture critique."
---

# Probing

Investigate code without changing it. Build an evidence-backed explanation a senior engineer can use to understand a subsystem or judge its design. Read the implementation, follow the runtime path, and separate known facts from inference.

## Pick the track

- **How.** Explain architecture, runtime flow, data movement, ownership, and where behavior lives.
- **Why.** Recover design intent, historical constraints, motivating failures, and rejected alternatives.
- **Critique.** Explain the current design first, then judge whether its abstractions, boundaries, and data model fit the code.

A request can combine tracks. Run How before Critique. Run Why only when motivation or history matters.

## Ground the investigation

1. **Name the target.** Identify the behavior, symbol, subsystem, or decision in question. State a best-guess interpretation when the request is vague; do not ask about facts the repository can answer.
2. **Find the entry point.** Search for the concrete symbols and follow callers and callees. Read code rather than inferring behavior from names or directory structure.
3. **Scale the exploration.** Inspect a narrow path directly. For a subsystem that spans files or services, split 2-4 read-only explorers by distinct concerns such as data model, runtime flow, configuration, and integration boundaries. If no subagent mechanism exists, inspect those concerns sequentially.
4. **Reconcile evidence.** Resolve contradictions before writing. Keep uncertainty explicit when the available sources cannot settle it.

## Explain how it works

Trace the full path from trigger to observable result. Name the important types, state owners, boundaries, and decision points. Point to specific files and symbols. Include only code snippets that clarify a mechanism better than prose.

Return the sections that help the reader:

- **Overview.** What the subsystem does and where it fits.
- **Key concepts.** Types, services, state, and boundaries the reader must know.
- **Flow.** Trigger, calls, transformations, decisions, and output.
- **Where it lives.** The smallest useful file map.
- **Gotchas.** Non-obvious behavior, hidden coupling, or constraints a new maintainer could miss.

## Recover why it exists

Start from a concrete question whose answer could change the interpretation. Anchor it to files, symbols, and lines, then follow the evidence:

1. Read focused `git blame` and file history.
2. Follow linked change reviews, issues, design documents, and code comments.
3. Search team discussion, observability, error tracking, or product analytics when those sources are available and relevant.
4. For an explicit broad-history request, enumerate every available evidence category and report both results and gaps.

Code proves current mechanics, not original intent. Treat a stated rationale as direct evidence. Label conclusions from timing, shape, or correlation as inference. Surface competing explanations when the record supports more than one.

## Critique the design

Run the How track first. Then assess the design through the concerns that affect real maintenance:

- whether abstractions hide complexity or only add indirection;
- whether the data model matches actual access patterns;
- whether validation and errors sit at system boundaries;
- whether ownership is concentrated or scattered across callers;
- whether likely changes modify one coherent owner or many unrelated files;
- whether deletion or a simpler structure can replace existing complexity.

When independent reviewers are available, give each the same explanation, file scope, and rubric. Judge their findings rather than forwarding them. Categorize the result as **Act on**, **Consider**, **Noted**, or **Dismissed**, with evidence for each decision.

## Guardrails

- Stay read-only. Do not edit code, open changes, or turn the investigation into implementation.
- Cite file and line ranges for mechanics. Cite commits, reviews, issues, documents, or comments for intent.
- Do not present inference as fact. Name missing sources and unresolved contradictions.
- Do not dump search logs or raw subagent output. Synthesize the smallest explanation that gives the reader a working model.
- If the investigation precedes implementation, close with **Preserve**, **Change**, **Avoid**, and **Risk**, then stop.
