"""
Run the full GenAI testing pipeline (Sections 4 / 4.1 of the paper) against
the toy sample_project.calculator module across several simulated sprints,
and print a results table comparable to Table 3 / Table 4 in the paper.

Usage:
    python run_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.pipeline import GenAITestingPipeline
from sample_project import calculator


def print_table(reports):
    header = f"{'Sprint':<7}{'Generated':<11}{'Executed':<10}{'Pass':<6}{'Defects':<9}" \
             f"{'Healed':<8}{'Coverage%':<11}{'Maint.hrs':<10}{'Time(s)':<8}"
    print(header)
    print("-" * len(header))
    for r in reports:
        print(
            f"{r.sprint_number:<7}{r.generated_count:<11}{r.executed_count:<10}"
            f"{r.pass_count:<6}{r.defect_count:<9}{r.healed_count:<8}"
            f"{r.coverage_pct:<11.1f}{r.maintenance_hours:<10.1f}{r.duration_sec:<8.2f}"
        )


def main():
    print("=" * 70)
    print("GenAI-Based Software Testing Pipeline -- Demo Run")
    print("Module under test: sample_project.calculator")
    print("=" * 70)

    # Module risk profile: stand-in for "historical defect statistics" (Sec.4
    # reward term D). Functions with known recent changes / past defects get
    # a higher prior risk score, which the RL prioritizer uses to favor them.
    module_risk = {
        "REQ-FACTORIAL": 0.8,   # has a seeded boundary defect
        "REQ-IS_PRIME": 0.8,    # has a seeded boundary defect
        "REQ-DIVIDE": 0.4,
        "REQ-ADD": 0.2,
        "REQ-AVERAGE": 0.3,
    }

    pipeline = GenAITestingPipeline(calculator, "sample_project.calculator", module_risk)

    print(f"\nParsed {len(pipeline.requirements)} requirements from the module:")
    for req in pipeline.requirements:
        print(f"  - {req.id}: {req.signature}")

    print(f"\nLLM generator mode: "
          f"{'REAL API call' if pipeline.generator.use_real_llm else 'offline template fallback (no API key set)'}")

    print("\nRunning sprints...\n")
    reports = pipeline.run_sprints(n=6)

    print()
    print_table(reports)

    print("\nNotes:")
    print(" - 'Defects' counts test failures this sprint (both genuine bugs and")
    print("   any not-yet-healed non-functional breaks).")
    print(" - 'Healed' counts tests the self-healing module successfully repaired")
    print("   after a non-functional failure (signature/locator-style drift).")
    print(" - 'Maint.hrs' is a simulated maintenance-effort estimate that ramps down")
    print("   as the self-healing success rate improves sprint over sprint, mirroring")
    print("   the declining trend in Fig. 5 of the paper.")
    print(" - Coverage/defect numbers come from the real toy module + real seeded")
    print("   bugs, not from the paper's proprietary dataset -- exact figures will")
    print("   differ from the paper's reported 92%/85%/55%/60%.")


if __name__ == "__main__":
    main()
