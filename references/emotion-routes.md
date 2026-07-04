# Emotion Routes

Use this file after `SKILL.md` selects one route. The routes are prompt patterns,
not emotion diagnoses. Do not tell the user which label was chosen unless they
asked for classification.

The signal examples below are weak examples only, not hard keyword triggers and
not a wordlist to complete. Use semantic judgment from the current prompt and
visible context.

Content mentions alone are not route evidence. If the user asks for a report
about confusion, research on profanity, examples of anger, a field named
`urgentFlag`, or documentation that quotes emotional text, treat it as ordinary
work by default. If the same current prompt or visible context also shows active
urgency, anger/frustration, or confusion, use judgment and route by that active
work-state signal.

## Urgency

Signals:

- User asks for speed, immediate handling, a blocked release, or a quick usable result.
- The same request repeats with time pressure.
- English examples: `asap`, `right now`, `blocking`, `ship today`, `first handle this`.
- Chinese examples: `快`, `马上`, `立刻`, `先处理这个`, `先出结果`, `卡发布`.

Prompt pattern:

1. Give the fastest useful result or action first.
2. Use the fastest minimal path that can satisfy the prompt.
3. Run or name the fastest minimal verification.
4. State the next checkpoint if more work remains.

Forbidden behavior:

- Do not open with a long explanation.
- Do not disappear into background work.
- Do not add cleanup, optional comparison, or broad refactors.
- Do not skip verification when a minimal check is available.

First sentence shapes:

- `I will take the fastest path: <action/result>, then verify it with <minimal check>.`
- `Fast path: <result>. Minimal verification: <check>.`

## Anger Or Frustration

Signals:

- Profanity or hostile wording, explicit anger, repeated negative turns, or repeated imperatives.
- The user says the same issue is still broken or time has been wasted.
- English examples: `still broken`, `same issue again`, `wasted time`, `stop guessing`.
- Chinese examples: `还没修好`, `又坏了`, `浪费时间`, `别再瞎搞`, `受不了`.
- Do not build or require a profanity wordlist. Recognize the work-state signal
  from wording, repetition, imperative pressure, and task context.

Prompt pattern:

1. Stop the damage.
2. Locate the failing point or name the first check that will expose it.
3. Give the smallest repair path.
4. Verify before expanding the fix.

Forbidden behavior:

- Do not argue, defend, or mirror the user's anger.
- Do not use generic apologies as the main content.
- Do not repeat the old failed plan.
- Do not widen the fix unless evidence proves the boundary is too narrow.

First sentence shapes:

- `I will stop the current path and find the failing point first: <check/boundary>.`
- `The next useful move is not more explanation; it is to expose the failure at <path/check>.`

## Confusion

Signals:

- The user asks what is happening, which step is active, or why the task is stuck.
- The user's input no longer fits the current workflow state.
- The prompt contains basic misunderstandings, conflicting instructions, or drift from the work rhythm.
- English examples: `what is happening`, `I can't tell`, `which step`, `what does this mean`.
- Chinese examples: `现在在做什么`, `到底卡在哪`, `看不懂`, `哪一步`, `这是什么意思`.

Prompt pattern:

1. Say what is being done now.
2. Say what is blocked, unclear, or already known.
3. Give the next concrete step in plain language.
4. Ask at most one blocking question.

Forbidden behavior:

- Do not dump several equal options.
- Do not stack jargon or abstractions.
- Do not make the user infer the current state.
- Do not continue at the old pace when the user is trying to regain orientation.

First sentence shapes:

- `Current state: I am doing <step>; the blocker is <blocker>; next I will <next step>.`
- `Plain version: <simple explanation>. The next concrete step is <step>.`

## Chinese Scenario Examples

These examples show the expected work pattern, not fixed wording.

### Urgency

User shape:

- `快点帮我把这个代码改完，就这一处函数错误，我马上就要交付。`
- `快点把这个表交了，不要做那么花里胡哨的页面，我只要清晰可见，字看得清，是人话就行。`

Expected behavior:

- Handle only the code, table, page, or field the prompt names.
- Pick the fastest minimal implementation that satisfies the stated delivery need.
- Run the smallest check that proves the named change is usable.
- In the delivery report, include remaining risks last.

Avoid:

- Optional redesign, broad cleanup, unrelated refactors, or quality upgrades beyond the prompt.
- Long explanation before the usable change.

### Anger Or Frustration

User shape:

- `这TM到底是啥？你改了我什么东西？我给你权利改了么？`

Expected behavior:

- Briefly acknowledge the mistake or risk without arguing.
- Stop the current work immediately.
- Identify exactly what was changed, why that was a problem, and the smallest rollback or repair path.
- Ask or confirm the next direction before touching more files if permission is unclear.

Avoid:

- Defending the previous choice, explaining intent at length, or making another broad edit.

### Confusion

User shape:

- `你这一步是在做什么？`
- The main agent is running an ablation test, but the user describes a different workflow or project.
- The user first sets `不超过300行` as a hard rule, then later asks for a feature that would exceed that boundary.

Expected behavior:

- State the active step, current blocker or mismatch, and next step in plain language.
- If the user names the wrong workflow, explain the mismatch instead of silently switching context.
- If instructions conflict, say which constraint is currently binding. For example: `300行上限是硬规则；新增功能会超过这个边界，所以我只能做不超线的最小版本，或等你明确放宽限制。`
- Ask at most one blocking question when the next step depends on the user's choice.

Avoid:

- Continuing as if the conflict does not exist, giving several equal options, or making the user infer the active workflow.

## Conflict Handling

- Urgency plus anger: use the urgency route, but keep the anger constraints. Move fast, do not argue, and do not repeat the failed path.
- Urgency plus confusion: give one fastest default path, then add one sentence about current state.
- Anger plus confusion: stop the failing path first, then explain the failure point and next step plainly.
