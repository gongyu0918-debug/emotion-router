# Emotion Value Model

This skill is valuable because it changes how an agent works at the moments where
coding tasks usually degrade. The output is better behavior, not a public emotion
classification.

## Priority Value

User-state signals should change work order:

| Situation | Behavior value |
|---|---|
| repeated failure | stop the old path, find the smallest failing check |
| evidence request | put basis before conclusion |
| scope protection | reduce accidental edits and config drift |
| urgent pressure | move action earlier without hiding the minimum reliable basis |
| confusion | align target before adding options |
| silent progress | surface blocker and next checkpoint |
| exploratory comparison | rank options before committing to a path |
| accepted fix | close with regression check instead of new work |

Priority order matters. Evidence beats speed because a fast answer with a false
basis creates more rework. Scope beats speed because unwanted edits are harder to
undo than a short delay. Repeated failure beats ordinary flow because the old path
has already lost trust.

## Quality Value

The agent becomes more reliable because it changes execution style:

- verification depth rises when trust depends on evidence
- explanation length shrinks when repair is more urgent than teaching
- file boundaries become explicit when scope risk is high
- progress updates become concrete during silent waits
- closeout prevents "fixed, then broken by extra cleanup"

## Alignment Value

The skill helps the agent answer the task situation, not just the sentence.

Examples:

- "Show me the basis" means evidence should precede action.
- "Only touch this file" means the allowed and forbidden scope should be visible.
- "Still broken" means the prior path is not trusted until a new failing check is named.
- "Looks good, run regression" means closeout, not another improvement pass.

## Measurement Ideas

Use these metrics when evaluating the skill:

- time to first useful evidence
- repeated same-issue correction rate
- scope violation rate
- wrong-patch rate after evidence request
- silent wait duration before status update
- post-success regression rate
- user correction rate after closeout
