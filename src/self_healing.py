"""
Stage 5 - Self-Healing Mechanism.

When a test fails for a *non-functional* reason -- e.g. the function under
test was renamed/moved, its argument count changed, or (in a UI context) a
locator changed -- the self-healing module attempts an automatic repair
rather than surfacing it as a "real" defect. Genuine assertion failures
(the function ran fine but returned the wrong value) are left alone, since
those indicate an actual bug that a human/RL-prioritized retest should see.

This mirrors the paper's description: "self-healing module is activated...
reads logs and change diffs to automatically fix locators, update
assertions, or regenerate previously-impacted tests with the help of the
LLM" (Sec. 4) and the pseudo-algorithm's `Self_Heal(t_f, logs, diffs)` step.
"""

from dataclasses import dataclass
from typing import Optional
import inspect
import re

from src.llm_test_generator import TestCase, LLMTestGenerator
from src.requirements_parser import Requirement
from src.test_executor import ExecutionResult

NON_FUNCTIONAL_PATTERNS = [
    r"ImportError",
    r"ModuleNotFoundError",
    r"AttributeError",
    r"TypeError: .*positional argument",
    r"TypeError: .*missing \d+ required",
    r"NoSuchElementException",          # Selenium-style locator failure (illustrative)
    r"StaleElementReferenceException",  # Selenium-style locator failure (illustrative)
]


@dataclass
class HealResult:
    healed: bool
    new_test_case: Optional[TestCase] = None
    reason: str = ""


class SelfHealer:
    def __init__(self, generator: LLMTestGenerator):
        self.generator = generator

    # ------------------------------------------------------------------ #
    def classify_failure(self, exec_result: ExecutionResult) -> str:
        """Return 'non-functional' if the failure looks like a stale/broken
        test (signature/locator drift) rather than a genuine assertion
        failure exposing a real defect."""
        text = exec_result.failure_reason or ""
        if any(re.search(p, text) for p in NON_FUNCTIONAL_PATTERNS):
            return "non-functional"
        if "AssertionError" in text:
            return "functional"  # a real defect was likely found -- don't "heal" it away
        return "unknown"

    # ------------------------------------------------------------------ #
    def heal(self, exec_result: ExecutionResult, failing_case: TestCase,
              requirement: Requirement) -> HealResult:
        category = self.classify_failure(exec_result)
        if category != "non-functional":
            return HealResult(healed=False, reason=f"failure classified as '{category}'; not auto-healed")

        # Re-derive the requirement signature from the *live* function (the
        # "change diff" in a real system) rather than the possibly-stale
        # Requirement.func reference, in case the function was reassigned.
        live_func = requirement.func
        try:
            import sys as _sys
            module_obj = _sys.modules.get(requirement.module)
            if module_obj is not None and hasattr(module_obj, requirement.name):
                live_func = getattr(module_obj, requirement.name)
        except Exception:
            pass

        current_signature = f"{requirement.name}{inspect.signature(live_func)}" \
            if live_func else requirement.signature

        repaired_requirement = Requirement(
            id=requirement.id,
            name=requirement.name,
            description=requirement.description
            + " [auto-detected signature/locator change; regenerating test]",
            signature=current_signature,
            module=requirement.module,
            func=live_func,
        )

        regenerated = self.generator.generate(repaired_requirement)
        replacement = next((tc for tc in regenerated if tc.kind == failing_case.kind), regenerated[0])
        replacement.history["healed_from"] = failing_case.id
        return HealResult(healed=True, new_test_case=replacement,
                           reason="regenerated test against updated signature")
