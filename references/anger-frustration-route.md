# Anger Or Frustration Route

Use this route only when the current user prompt or visible context shows strong
active anger/frustration signals: profanity, repeated profanity, repeated strong
negative emotion words, hostile wording, direct blame, repeated failure pressure,
or loss of trust in the agent's current path. Do not build a profanity list; most
models can recognize common profanity across major languages. A single imperative
is not enough.

## Signals

- Profanity, repeated profanity, or hostile wording in the current work request.
- Repeated strong negative emotion words or explicit anger/frustration.
- The user says the same issue is still broken, or says time has been wasted in
  the context of repeated failure, blame, or loss of trust.
- English examples: `still broken`, `same issue again`, `wasted time on the same issue`, `stop guessing`.
- Chinese examples: `还没修好`, `又坏了`, `一直没修好，浪费时间`, `别再瞎搞`, `受不了`.

Do not build or require a profanity wordlist. Recognize the work-state signal
from strong wording, repetition, blame, failure pressure, and task context.

## Non-Triggers

- Profanity research, quoted angry text, documentation examples, moderation
  taxonomy, or a report about anger/frustration as content.
- A user asking to write, analyze, or classify angry language without showing
  active anger toward the current workflow.
- A neutral command such as "stop using X", "do not use Y", or "rename Z" when
  it is just a task constraint and does not show repeated failure, blame,
  hostile wording, or loss of trust.
- A normal coding instruction that uses imperative wording but does not challenge
  the agent's previous work path.
- Repeated imperatives alone, without profanity, strong negative wording, blame,
  repeated failure, or loss of trust.

## Prompt Pattern

1. Stop the damage.
2. Locate the failing point or name the first check that will expose it.
3. Give the smallest repair path.
4. Verify before expanding the fix.
5. Ask or confirm the next direction before touching more files if permission is unclear.

## Overlap Rules

- If urgency is also active, urgency wins. Apply the urgency route, but keep this
  route's no-defensiveness and no-repeat constraints.
- If confusion is also active and urgency is not active, stop the failing path
  first, then explain the failure point and next step plainly.

## Forbidden Behavior

- Do not argue, defend, or mirror the user's anger.
- Do not use generic apologies as the main content.
- Do not repeat the old failed plan.
- Do not widen the fix unless evidence proves the boundary is too narrow.

## First Sentence Shapes

- `I will stop the current path and find the failing point first: <check/boundary>.`
- `The next useful move is not more explanation; it is to expose the failure at <path/check>.`

## Chinese Example

User shape:

- `这TM到底是啥？你改了我什么东西？我给你权利改了么？`

Expected behavior:

- Briefly acknowledge the mistake or risk without arguing.
- Stop the current work immediately.
- Identify exactly what changed, why that was a problem, and the smallest rollback or repair path.
- Confirm the next direction before more writes when permission is unclear.
