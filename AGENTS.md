# Emotion Router Maintainer Rules

## Runtime Boundary

The runtime skill contains only:

- `SKILL.md`
- `agents/openai.yaml`
- the three published route files under `references/`

ClawHub also includes `LICENSE`. SkillHub uses the runtime set without that file.

Keep `SKILL.md` focused on activation, priority, and one-reference navigation.
Keep each route focused on trigger, response, overlap, avoid, and short examples.
Do not put release history, package manifests, test commands, commit requirements,
benchmark claims, or legacy runtime behavior in installed Markdown.

`main` is the generic English runtime source. SkillHub-specific Chinese listing
metadata belongs on a dedicated `codex/skillhub-*` branch and must not change the
generic `main` frontmatter.

## Required Validation

Run before every commit:

```text
python -B C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
python -B scripts\markdown_skill_audit.py
python -B scripts\bundle_manifest_check.py
python -B scripts\bundle_manifest_safety_test.py
python -B scripts\marketplace_tag_audit.py
python -B scripts\smoke_test.py --strict
python -B -m compileall -q scripts
git diff --check
```

For behavior changes, run fresh no-skill versus skill subagents on the changed
route and at least one non-trigger. Do not replace live comparison with
hand-authored replies or regex routing.

Stage packages only into a fresh or empty directory. Never stage over the
repository, an ancestor, or a non-empty directory.

Create a git commit for every delivered change. Do not publish unless the user
explicitly requests it.
