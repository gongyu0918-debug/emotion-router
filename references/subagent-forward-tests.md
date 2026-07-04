# Subagent Forward Tests

Use this maintainer-only reference to validate that the lightweight router changes
real agent behavior. This file is not part of the installed bundle.

## Protocol

1. Start a fresh subagent.
2. Prompt it with:
   `Use $emotion-skill at <path> to respond to this user request. Do not modify files.`
3. Provide only the realistic user request.
4. Do not include the expected route, scoring rubric, suspected failure, or desired answer.
5. Ask for the exact reply and the skill files read.
6. Score behavior, not keyword overlap.

## Scenario Set

| ID | User request shape | Pass behavior |
|---|---|---|
| `forward-urgency` | "This blocks today's release. Take the fastest path, handle this first, and give the minimal check." | Gives a fast minimal path, a usable first result or action, and the fastest minimal verification. |
| `forward-anger-frustration` | "This is still broken after the last two tries. Stop guessing and show where it fails before changing more." | Stops the old path, locates or names the failing check, and gives the smallest repair path without arguing. |
| `forward-confusion` | "I cannot tell what is happening now. Which step is active, where is it stuck, and what is next?" | States what is being done now, the blocker or unknown, and the next step in plain language. |
| `forward-urgency-plus-anger` | "This is still broken and it blocks shipping today. Stop repeating the same plan and fix the shortest path now." | Prioritizes the urgent fast path while avoiding defensiveness and repeated failed plans. |

## Failure Signals

Fail the result if the agent:

- exposes labels such as "you are angry" or "you are confused"
- asks to run Python or a classifier before applying the skill
- reads or asks for AGENTS.md, durable memory, user profiles, or hidden history
- treats signal examples as hard keyword rules
- gives several equal options in a confusion case
- gives a long explanation before action in an urgency case
- argues, defends, or gives only a generic apology in an anger/frustration case
