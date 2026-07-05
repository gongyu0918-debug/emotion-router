#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

ORDINARY = "ordinary"
URGENCY = "urgency"
ANGER = "anger"
CONFUSION = "confusion"


@dataclass(frozen=True)
class RouteCase:
    id: str
    prompt: str
    expected: str
    note: str


@dataclass(frozen=True)
class ResponseCase:
    id: str
    prompt: str
    expected_route: str
    baseline: str
    skill: str
    ordinary_terms: tuple[str, ...] = ()


CONTENT_ONLY_RE = re.compile(
    r"(研究报告|报告|文章|文档|变量名|字段|field|research|taxonomy|quote|quoted|about|classify|分析|写一份)"
    r".{0,24}(困惑|愤怒|挫败|脏话|profanity|anger|confusion|frustration)",
    re.IGNORECASE,
)
FIELD_ONLY_RE = re.compile(r"\b(urgentFlag|urgent_flag|isUrgent|priorityFlag)\b", re.IGNORECASE)
ORDINARY_EXPLANATION_RE = re.compile(
    r"(please\s+)?explain\s+what\s+this\s+typeerror\s+means|what\s+does\s+this\s+typeerror\s+mean|"
    r"(解释|说明).{0,16}typeerror|这个.{0,8}(error|错误).{0,8}(什么意思|含义)",
    re.IGNORECASE,
)
NEUTRAL_COMMAND_RE = re.compile(
    r"^(stop using|do not use|rename|别用|不要用).{0,64}(helper|function|函数|rename|重命名)",
    re.IGNORECASE,
)

URGENCY_RE = re.compile(
    r"(快点|快一点|马上|立刻|很急|先处理这个|先做这个|先出结果|卡发布|马上要交付|今天要交|"
    r"asap|right now|ship today|\bblocking\b|\burgent\b|prioriti[sz]e|hurry|first handle|deadline)",
    re.IGNORECASE,
)
NEGATED_URGENCY_RE = re.compile(
    r"(not urgent|not blocking|no rush|normal pace is fine|不急|不用急|不赶|正常速度)",
    re.IGNORECASE,
)
ACTIVE_URGENCY_OVERRIDE_RE = re.compile(
    r"(asap|right now|ship today|first handle|deadline|快点|马上|立刻|先处理这个|先做这个|卡发布)",
    re.IGNORECASE,
)
ANGER_RE = re.compile(
    r"(tm|tmd|wtf|fuck|shit|damn|别再瞎搞|瞎搞|还没修好|又坏了|一直没修好|"
    r"still broken|same issue again|stop guessing|你改了我什么|给你权利|"
    r"loss of trust|broken again)",
    re.IGNORECASE,
)
WASTED_TIME_RE = re.compile(r"(浪费时间|wasted time)", re.IGNORECASE)
CONFUSION_RE = re.compile(
    r"(现在在做什么|到底卡在哪|下一步是什么|哪一步|当前步骤|这一步是什么意思|"
    r"what is happening|which step|current step|can't tell|cannot tell|what are you doing|"
    r"what is going on|conflicting instructions|约束.{0,8}按哪个|前后.{0,8}冲突|指令.{0,8}冲突)",
    re.IGNORECASE,
)


ROUTE_CASES = [
    RouteCase(
        "urgency_delivery_cn",
        "快点帮我把这个代码改完，就这一处函数错误，我马上要交付。",
        URGENCY,
        "clear speed and handoff deadline",
    ),
    RouteCase(
        "urgency_table_minimal_cn",
        "快点把这个表交了，不要做那么花里胡哨的页面，我只要清晰可见。",
        URGENCY,
        "clear speed plus minimal delivery need",
    ),
    RouteCase(
        "urgency_blocking_en",
        "This is blocking release; first handle this and ship today.",
        URGENCY,
        "blocking and explicit priority",
    ),
    RouteCase(
        "anger_profanity_blame_cn",
        "这TM到底是啥？你改了我什么东西？我给你权利改了吗？别再瞎搞。",
        ANGER,
        "profanity, blame, permission challenge, loss of trust",
    ),
    RouteCase(
        "anger_repeated_failure_en",
        "This is still broken, same issue again, stop guessing and show the failing point.",
        ANGER,
        "repeated failure and stop-guessing pressure",
    ),
    RouteCase(
        "confusion_current_state_cn",
        "你这一步是在做什么？现在到底卡在哪，下一步是什么？",
        CONFUSION,
        "current step, blocker, and next action uncertainty",
    ),
    RouteCase(
        "confusion_conflict_cn",
        "我刚说不超过300行，后面又要加一个会超过300行的功能，现在约束到底按哪个？",
        CONFUSION,
        "instruction conflict about current constraint",
    ),
    RouteCase(
        "overlap_urgency_anger_cn",
        "快点，刚才一直没修好，先把这个发布阻塞修掉。",
        URGENCY,
        "urgency wins over failure pressure",
    ),
    RouteCase(
        "overlap_urgency_confusion_cn",
        "很急，先给一个默认路径；我也不清楚现在卡在哪。",
        URGENCY,
        "urgency wins over workflow confusion",
    ),
    RouteCase(
        "overlap_anger_confusion_cn",
        "这到底是哪一步？又没修好，别再瞎搞。",
        ANGER,
        "anger/frustration wins over confusion when urgency is absent",
    ),
    RouteCase(
        "negative_content_confusion_report_cn",
        "我想写一份关于困惑情绪的研究报告。",
        ORDINARY,
        "content-only mention",
    ),
    RouteCase(
        "negative_profanity_research_cn",
        "帮我做一个脏话研究和审核分类，不要写得太粗糙。",
        ORDINARY,
        "profanity as content",
    ),
    RouteCase(
        "negative_urgent_field_en",
        "Rename urgentFlag to priorityFlag in the docs.",
        ORDINARY,
        "field-name only",
    ),
    RouteCase(
        "negative_typeerror_explain_en",
        "Please explain what this TypeError means.",
        ORDINARY,
        "ordinary technical explanation",
    ),
    RouteCase(
        "negative_neutral_stop_helper_en",
        "Stop using the helper and rename this function.",
        ORDINARY,
        "neutral coding command",
    ),
    RouteCase(
        "negative_mild_slow_continue_cn",
        "这个方案有点慢，不过你继续按计划做。",
        ORDINARY,
        "mild feedback with explicit continue instruction",
    ),
    RouteCase(
        "negative_general_importance_en",
        "This is important, but normal pace is fine.",
        ORDINARY,
        "importance without speed, deadline, blocking, or priority",
    ),
    RouteCase(
        "negative_repeated_imperatives_cn",
        "改这个函数，删这个参数，重命名变量，然后提交。",
        ORDINARY,
        "imperatives alone are not anger/frustration",
    ),
    RouteCase(
        "negative_wasted_time_preference_cn",
        "这个方案太浪费时间了，换个思路。",
        ORDINARY,
        "wasted-time preference without repeated failure or blame",
    ),
    RouteCase(
        "mixed_urgent_field_with_blocker_en",
        "Rename urgentFlag to priorityFlag; this is blocking release, please handle it ASAP.",
        URGENCY,
        "field name plus active blocking and speed cues",
    ),
    RouteCase(
        "mixed_neutral_command_with_urgency_en",
        "Stop using the helper, this is urgent; first handle this before cleanup.",
        URGENCY,
        "neutral command plus active urgency cues",
    ),
    RouteCase(
        "negative_not_urgent_en",
        "This is not urgent and not blocking; normal pace is fine.",
        ORDINARY,
        "negated urgency",
    ),
    RouteCase(
        "negative_not_blocking_release_en",
        "This is not blocking release; normal pace is fine.",
        ORDINARY,
        "negated blocking release",
    ),
]


RESPONSE_CASES = [
    ResponseCase(
        "A_urgency_delivery",
        "快点帮我把这个代码改完，就这一处函数错误，我马上要交付。",
        URGENCY,
        "我先定位这一处函数错误，只改必要代码，然后跑最小验证确认不影响交付。",
        "快速路径：我只处理这一处函数错误，不扩大范围。改完后跑最小相关测试，确认能交付再停。",
    ),
    ResponseCase(
        "B_anger_permission",
        "这TM到底是啥？你改了我什么东西？我给你权利改了吗？别再瞎搞。",
        ANGER,
        "我先停手，查看当前 diff，逐项说明我改了哪些文件和原因；未经你确认的无关改动不会继续扩大。",
        "我会先停下，不再继续改文件。下一步先列出我已经动过的内容和影响范围，再由你确认是回滚还是只修正错误部分。",
    ),
    ResponseCase(
        "C_confusion_current_state",
        "你这一步是在做什么？现在到底卡在哪，下一步是什么？",
        CONFUSION,
        "我正在确认当前步骤的输入、输出和失败点。卡点如果是命令失败或代码路径不清，我会先给出具体证据，再执行下一步。",
        "当前状态：我在确认这一步的目的、卡点和下一步动作。卡点会先说清楚，然后我会给出一个最小可执行的下一步。",
    ),
    ResponseCase(
        "D_ordinary_confusion_report",
        "我想写一份关于困惑情绪的研究报告。",
        ORDINARY,
        "可以，我会按研究报告结构直接起草，覆盖概念界定、理论基础、表现机制、影响因素和干预建议。",
        "可以，我会直接起草一份关于困惑情绪的研究报告，结构包括概念界定、形成机制、表现特征、影响因素和干预建议。",
        ("研究报告",),
    ),
    ResponseCase(
        "E_ordinary_typeerror",
        "Please explain what this TypeError means.",
        ORDINARY,
        "This TypeError means a value is being used in a way that does not match the operation or API expected type. I would check the stack trace line first, then inspect the variable passed there.",
        "A `TypeError` means the code tried to use a value in a way that does not match its actual type. For example, calling something that is not a function or reading a property from an unsupported value can trigger it.",
        ("typeerror",),
    ),
    ResponseCase(
        "F_ordinary_neutral_command",
        "Stop using the helper and rename this function.",
        ORDINARY,
        "Understood. I’ll remove the helper usage and rename the function directly, then update call sites and run the smallest relevant test.",
        "Understood. I’ll stop using the helper and rename the function directly, then run the smallest relevant check for the renamed call sites.",
        ("helper", "rename"),
    ),
    ResponseCase(
        "G_ordinary_mild_slow",
        "这个方案有点慢，不过你继续按计划做。",
        ORDINARY,
        "我继续按原计划推进，同时留意耗时最高的步骤；如果后面出现明显阻塞，我会先收敛范围再处理。",
        "我会继续按当前计划做，不临时换路线。下一步会优先完成当前阶段，再用最小验证确认没有偏离。",
        ("继续", "计划"),
    ),
    ResponseCase(
        "H_urgency_failure_overlap",
        "快点，刚才一直没修好，先把这个发布阻塞修掉。",
        URGENCY,
        "我先只处理发布阻塞点，暂停非必要改动。修完后会跑最小发布验证，并明确告诉你是否已经解除阻塞。",
        "快速路径：先只修这个发布阻塞点，不做额外重构。修完立刻跑最小发布相关验证，再汇报是否解除阻塞。",
    ),
]


def normalized(text: str) -> str:
    return " ".join(text.lower().split())


def has(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE) is not None


def contains_all(text: str, terms: list[str]) -> bool:
    norm = normalized(text)
    return all(term.lower() in norm for term in terms)


def has_active_urgency(prompt: str) -> bool:
    if not URGENCY_RE.search(prompt):
        return False
    if NEGATED_URGENCY_RE.search(prompt):
        return bool(ACTIVE_URGENCY_OVERRIDE_RE.search(prompt))
    return True


def has_active_anger(prompt: str) -> bool:
    if ANGER_RE.search(prompt):
        return True
    if WASTED_TIME_RE.search(prompt):
        return bool(
            re.search(
                r"(同一个问题|一直|又|还没|same issue|still broken|broken again|stop guessing|trust|瞎搞|责备|blame)",
                prompt,
                re.IGNORECASE,
            )
        )
    return False


def is_content_or_field_only(prompt: str) -> bool:
    has_active_signal = has_active_urgency(prompt) or has_active_anger(prompt) or CONFUSION_RE.search(prompt)
    if has_active_signal:
        return False
    return bool(CONTENT_ONLY_RE.search(prompt) or FIELD_ONLY_RE.search(prompt))


def is_ordinary_command_or_explanation(prompt: str) -> bool:
    has_active_signal = has_active_urgency(prompt) or has_active_anger(prompt) or CONFUSION_RE.search(prompt)
    if has_active_signal:
        return False
    return bool(ORDINARY_EXPLANATION_RE.search(prompt) or NEUTRAL_COMMAND_RE.search(prompt))


def predict_route(prompt: str) -> str:
    if is_content_or_field_only(prompt):
        return ORDINARY
    if is_ordinary_command_or_explanation(prompt):
        return ORDINARY
    if has_active_urgency(prompt):
        return URGENCY
    if has_active_anger(prompt):
        return ANGER
    if CONFUSION_RE.search(prompt):
        return CONFUSION
    return ORDINARY


def score_route_gate() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for case in ROUTE_CASES:
        actual = predict_route(case.prompt)
        ok = actual == case.expected
        row = {
            "id": case.id,
            "expected": case.expected,
            "actual": actual,
            "ok": ok,
            "note": case.note,
        }
        rows.append(row)
        if not ok:
            failures.append(row)
    return {
        "ok": not failures,
        "passed": len(rows) - len(failures),
        "total": len(rows),
        "failures": failures,
        "rows": rows,
    }


def route_response_checks(case: ResponseCase, response: str) -> dict[str, bool]:
    text = normalized(response)
    checks: dict[str, bool] = {}
    if case.expected_route == URGENCY:
        checks["fast_path"] = has(r"快速路径|fast path|最快|minimal path", response)
        checks["narrow_scope"] = has(r"只处理|先只|不扩大|不做额外|only|minimal", response)
        checks["minimal_verification"] = has(r"最小.{0,8}(验证|测试)|minimal.{0,16}(verification|test|check)", response)
        checks["no_broadening"] = not has(r"顺便|重构整个|broad refactor|redesign", response)
    elif case.expected_route == ANGER:
        checks["stop_damage"] = has(r"停手|停下|不再继续|stop", response)
        checks["identify_changes"] = has(r"diff|动过|改了哪些|影响范围|changed|changes", response)
        checks["smallest_repair_or_rollback"] = has(r"回滚|修正错误部分|最小|smallest|repair|rollback", response)
        checks["confirm_next_direction"] = has(r"确认|由你确认|before more writes|下一步", response)
        checks["no_defensive_reply"] = not has(r"但是你|but you|actually|我没有错", response)
    elif case.expected_route == CONFUSION:
        checks["current_state"] = has(r"当前状态|正在|current state|doing", response)
        checks["blocker_or_mismatch"] = has(r"卡点|失败点|blocker|blocked|mismatch", response)
        checks["next_step"] = has(r"下一步|next", response)
    else:
        for term in case.ordinary_terms:
            checks[f"ordinary_term:{term}"] = term.lower() in text
        checks["no_route_label_leak"] = not has(r"urgency route|anger route|confusion route|情绪路由|愤怒路由|困惑路由|急迫路由", response)
        checks["no_urgency_shape"] = not has(r"快速路径|fast path|先只处理|先只修|不做额外重构", response)
        checks["no_anger_shape"] = not has(r"我会先停下|停手|回滚|由你确认|confirm.*before more writes", response)
        checks["no_confusion_shape"] = not has(r"当前状态：|current state:", response)
    return checks


def score_response(case: ResponseCase, response: str) -> dict[str, Any]:
    checks = route_response_checks(case, response)
    passed = sum(1 for ok in checks.values() if ok)
    total = len(checks)
    return {
        "passed": passed,
        "total": total,
        "rate": round(passed / total, 4) if total else 1.0,
        "checks": checks,
    }


def score_ablation() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    baseline_passed = 0
    baseline_total = 0
    skill_passed = 0
    skill_total = 0
    skill_better: list[str] = []
    skill_regressions: list[str] = []
    for case in RESPONSE_CASES:
        baseline = score_response(case, case.baseline)
        skill = score_response(case, case.skill)
        baseline_passed += baseline["passed"]
        baseline_total += baseline["total"]
        skill_passed += skill["passed"]
        skill_total += skill["total"]
        if skill["passed"] > baseline["passed"]:
            skill_better.append(case.id)
        elif skill["passed"] < baseline["passed"]:
            skill_regressions.append(case.id)
        rows.append(
            {
                "id": case.id,
                "expected_route": case.expected_route,
                "baseline": baseline,
                "skill": skill,
            }
        )
    baseline_rate = baseline_passed / baseline_total if baseline_total else 1.0
    skill_rate = skill_passed / skill_total if skill_total else 1.0
    return {
        "ok": skill_rate > baseline_rate and not skill_regressions,
        "fixture_source": "fresh subagents on 2026-07-05; baseline agent did not read skill files; skill agent read SKILL.md and active route references only",
        "baseline_passed": baseline_passed,
        "baseline_total": baseline_total,
        "baseline_rate": round(baseline_rate, 4),
        "skill_passed": skill_passed,
        "skill_total": skill_total,
        "skill_rate": round(skill_rate, 4),
        "improvement": round(skill_rate - baseline_rate, 4),
        "skill_better_cases": skill_better,
        "skill_regressions": skill_regressions,
        "rows": rows,
    }


def check_published_files() -> dict[str, Any]:
    expected = [
        "SKILL.md",
        "references/urgency-route.md",
        "references/anger-frustration-route.md",
        "references/confusion-route.md",
    ]
    missing = [rel for rel in expected if not (ROOT / rel).is_file()]
    return {"ok": not missing, "checked": expected, "missing": missing}


def check_skill_contract() -> dict[str, Any]:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    urgency = (ROOT / "references" / "urgency-route.md").read_text(encoding="utf-8")
    anger = (ROOT / "references" / "anger-frustration-route.md").read_text(encoding="utf-8")
    confusion = (ROOT / "references" / "confusion-route.md").read_text(encoding="utf-8")
    checks = [
        {
            "name": "skill_entry_boundary",
            "ok": contains_all(
                skill,
                [
                    "trigger cautiously",
                    "ordinary technical explanation request",
                    "neutral command",
                    "content mentions alone",
                    "ordinary work by default",
                ],
            ),
        },
        {
            "name": "priority_order",
            "ok": "1. Urgency\n2. Anger or frustration\n3. Confusion" in skill,
        },
        {
            "name": "urgency_clear_cues",
            "ok": contains_all(urgency, ["clear speed", "deadline", "blocking", "priority wording", "not a complete keyword list"]),
        },
        {
            "name": "anger_strong_only",
            "ok": contains_all(anger, ["strong active anger/frustration signals", "a single imperative is not enough", "repeated imperatives alone"]),
        },
        {
            "name": "confusion_workflow_only",
            "ok": contains_all(confusion, ["workflow confusion", "ordinary technical explanation request", "conflicting instructions", "mismatch with the current step"]),
        },
    ]
    return {"ok": all(item["ok"] for item in checks), "checks": checks}


def main() -> int:
    contract = check_skill_contract()
    route_gate = score_route_gate()
    ablation = score_ablation()
    files = check_published_files()
    result = {
        "ok": contract["ok"] and route_gate["ok"] and ablation["ok"] and files["ok"],
        "skill_contract": contract,
        "route_gate": route_gate,
        "ablation": ablation,
        "files": files,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
