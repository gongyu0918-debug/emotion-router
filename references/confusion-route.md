# Confusion Route

Use this route when the current user prompt or visible context shows active
workflow confusion about the current step, mismatch, contradiction, or next
action. Use soft cues and context; do not route ordinary explanation requests.

## Signals

- The user asks what is happening, which step is active, or why the task is stuck.
- The user's input no longer fits the current workflow state.
- The prompt contains basic misunderstandings, conflicting instructions, or drift from the work rhythm.
- English examples: `what is happening in this workflow`, `I can't tell which step is active`, `which step`, `what does this current step mean`.
- Chinese examples: `现在在做什么`, `到底卡在哪`, `哪一步`, `当前步骤是什么意思`, `这一步是什么意思`.

Route to confusion only when the user is seeking orientation. If the same prompt
primarily expresses blame, repeated failure pressure, or loss of trust in the
agent's current path, use anger/frustration instead.

## Non-Triggers

- A report, article, variable name, quoted example, or research task about
  confusion as content.
- A normal task that only mentions confusion without showing current workflow uncertainty.
- An ordinary technical explanation request such as "what does this error mean" unless the
  user also shows lost workflow orientation, conflicting instructions, or a
  mismatch with the current step.

## Prompt Pattern

1. Say what is being done now.
2. Say what is blocked, unclear, mismatched, or already known.
3. Give the next concrete step in plain language.
4. Ask at most one blocking question.

## Overlap Rules

- If urgency is also active, urgency wins. Give one fastest default path and add
  one short current-state sentence.
- If anger/frustration is also active and urgency is not active, anger/frustration
  wins. Stop the failing path first, then explain the failure point and next step plainly.

## Forbidden Behavior

- Do not dump several equal options.
- Do not stack jargon or abstractions.
- Do not make the user infer the current state.
- Do not continue at the old pace when the user is trying to regain orientation.

## First Sentence Shapes

- `Current state: I am doing <step>; the blocker is <blocker>; next I will <next step>.`
- `Plain version: <simple explanation>. The next concrete step is <step>.`

## Chinese Examples

User shape:

- `你这一步是在做什么？`
- The main agent is running an ablation test, but the user describes a different workflow or project.
- The user first sets `不超过300行` as a hard rule, then later asks for a feature that would exceed that boundary.

Expected behavior:

- State the active step, current blocker or mismatch, and next step in plain language.
- If the user names the wrong workflow, explain the mismatch instead of silently switching context.
- If instructions conflict, say which constraint is currently binding.
- Ask at most one blocking question when the next step depends on the user's choice.
