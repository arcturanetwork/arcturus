"""Compare bounded workflows with a flexible planner on the same tasks."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    intent: str
    needs_research: bool
    needs_publish: bool


def fixed_workflow(task: Task) -> list[str]:
    """Predictable path: skips unnecessary stages but never invents tools."""
    steps = ["classify"]
    if task.needs_research:
        steps.extend(["retrieve", "verify_sources"])
    if task.needs_publish:
        steps.extend(["request_approval", "publish"])
    return steps + ["finish"]


def flexible_planner(task: Task) -> list[str]:
    """Toy planner showing flexibility and its extra governance surface."""
    if task.intent == "summarize":
        return ["classify", "retrieve", "synthesize", "finish"]
    if task.intent == "publish":
        return ["classify", "retrieve", "synthesize", "request_approval",
                "publish", "finish"]
    return ["classify", "ask_clarifying_question", "finish"]


def evaluate_plan(task: Task, plan: list[str]) -> dict[str, object]:
    must_include = {"classify", "finish"}
    if task.needs_research:
        must_include.add("retrieve")
    if task.needs_publish:
        must_include.update({"request_approval", "publish"})
    missing = sorted(must_include - set(plan))
    unauthorized_write = "publish" in plan and not task.needs_publish
    return {"success": not missing and not unauthorized_write,
            "missing": missing, "unauthorized_write": unauthorized_write,
            "steps": len(plan)}

