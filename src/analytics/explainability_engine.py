
import pandas as pd

from src.features.feature_engineering import (
    build_feature_dataset
)

from src.analytics.execution_gap_engine import (
    detect_execution_gaps
)

from src.analytics.negative_space_engine import (
    detect_negative_space
)

from src.analytics.peer_benchmarking import (
    build_peer_metrics,
    detect_peer_deviations,
)

from src.analytics.prioritization_engine import (
    build_prioritization_queue,
)

from src.anomaly_detection.operational_pattern_engine import (
    detect_operational_patterns,
)


# ---------------------------------------------------------
# Explainability & Evidence Engine
# ---------------------------------------------------------

def build_explanation(assessment_id):
    """
    Build an evidence-based explanation for why an assessment
    received its supervisory priority.

    SAT-SA provides evidence and potential supervisory signals.
    It does not make a final compliance or risk judgment.
    """

    # ---------------------------------------------------------
    # 1. Load data
    # ---------------------------------------------------------

    alerts, case_features, monitoring = (
        build_feature_dataset()
    )

    assets = pd.read_csv(
        "data/synthetic/assets.csv"
    )

    # ---------------------------------------------------------
    # 2. Generate analytical findings
    # ---------------------------------------------------------

    # Execution-gap findings
    execution_findings = detect_execution_gaps(
        case_features
    )

    # Negative-space findings
    negative_space_findings = detect_negative_space(
        monitoring,
        assets
    )

    # Peer benchmarking
    peer_metrics = build_peer_metrics(
        case_features,
        execution_findings
    )

    peer_findings = detect_peer_deviations(
        peer_metrics
    )

    # Operational-pattern findings
    operational_findings = detect_operational_patterns(
        case_features
    )

    # ---------------------------------------------------------
    # 3. Get prioritization result
    # ---------------------------------------------------------

    queue = build_prioritization_queue()

    assessment_row = queue[
        queue["assessment_id"] == assessment_id
    ]

    if assessment_row.empty:

        return None

    assessment_row = assessment_row.iloc[0]

    # ---------------------------------------------------------
    # 4. Filter evidence belonging to this assessment
    # ---------------------------------------------------------

    execution_evidence = execution_findings[
        execution_findings["assessment_id"]
        == assessment_id
    ].copy()

    negative_space_evidence = negative_space_findings[
        negative_space_findings["assessment_id"]
        == assessment_id
    ].copy()

    peer_evidence = peer_findings[
        peer_findings["assessment_id"]
        == assessment_id
    ].copy()

    operational_evidence = operational_findings[
        operational_findings["assessment_id"]
        == assessment_id
    ].copy()

    # ---------------------------------------------------------
    # 5. Build explanation summary
    # ---------------------------------------------------------

    explanation = {

        "assessment_id":
            assessment_id,

        "entity_id":
            assessment_row["entity_id"],

        "review_rank":
            int(
                assessment_row["review_rank"]
            ),

        "priority_score":
            float(
                assessment_row["priority_score"]
            ),

        "review_priority":
            assessment_row["review_priority"],

        "rationale":
            assessment_row["rationale"],

        "execution_gap_count":
            len(
                execution_evidence
            ),

        "negative_space_count":
            len(
                negative_space_evidence
            ),

        "peer_deviation_count":
            len(
                peer_evidence
            ),

        "operational_pattern_count":
            len(
                operational_evidence
            ),
    }

    return (
        explanation,
        execution_evidence,
        negative_space_evidence,
        peer_evidence,
        operational_evidence,
    )


# ---------------------------------------------------------
# Display Explanation
# ---------------------------------------------------------

def display_explanation(assessment_id):

    result = build_explanation(
        assessment_id
    )

    if result is None:

        print(
            f"No assessment found for {assessment_id}."
        )

        return

    (
        explanation,
        execution_evidence,
        negative_space_evidence,
        peer_evidence,
        operational_evidence,
    ) = result

    print("\n")

    print("=" * 70)
    print("SAT-SA EXPLAINABILITY & EVIDENCE")
    print("=" * 70)

    # -----------------------------------------------------
    # Assessment Summary
    # -----------------------------------------------------

    print(
        f"\nAssessment: "
        f"{explanation['assessment_id']}"
    )

    print(
        f"Entity: "
        f"{explanation['entity_id']}"
    )

    print(
        f"Review Rank: "
        f"{explanation['review_rank']}"
    )

    print(
        f"Priority: "
        f"{explanation['review_priority']}"
    )

    print(
        f"Priority Score: "
        f"{explanation['priority_score']}"
    )

    # -----------------------------------------------------
    # Why prioritized?
    # -----------------------------------------------------

    print(
        "\nWhy was this assessment prioritized?"
    )

    print(
        f"→ {explanation['rationale']}"
    )

    # -----------------------------------------------------
    # Evidence Summary
    # -----------------------------------------------------

    print("\n" + "-" * 70)
    print("EVIDENCE SUMMARY")
    print("-" * 70)

    print(
        f"• Execution-gap findings: "
        f"{explanation['execution_gap_count']}"
    )

    print(
        f"• Negative-space findings: "
        f"{explanation['negative_space_count']}"
    )

    print(
        f"• Peer deviation findings: "
        f"{explanation['peer_deviation_count']}"
    )

    print(
        f"• Operational-pattern findings: "
        f"{explanation['operational_pattern_count']}"
    )

    # ---------------------------------------------------------
    # Execution Gap Evidence
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("1. EXECUTION GAP EVIDENCE")
    print("-" * 70)

    if execution_evidence.empty:

        print(
            "No execution-gap findings."
        )

    else:

        print(
            f"Total findings: "
            f"{len(execution_evidence)}"
        )

        print(
            execution_evidence[
                [
                    "case_id",
                    "signal_type",
                    "priority",
                    "closure_hours",
                    "evidence_count",
                    "steps_recorded",
                    "root_cause_identified",
                    "remediation_recorded",
                    "reason",
                ]
            ].to_string(
                index=False
            )
        )

    # ---------------------------------------------------------
    # Negative Space Evidence
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("2. NEGATIVE SPACE EVIDENCE")
    print("-" * 70)

    if negative_space_evidence.empty:

        print(
            "No negative-space findings."
        )

    else:

        print(
            f"Total findings: "
            f"{len(negative_space_evidence)}"
        )

        print(
            negative_space_evidence[
                [
                    "asset_id",
                    "asset_name",
                    "signal_type",
                    "coverage_percent",
                    "telemetry_available",
                    "reason",
                ]
            ].to_string(
                index=False
            )
        )

    # ---------------------------------------------------------
    # Peer Deviation Evidence
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("3. PEER DEVIATION EVIDENCE")
    print("-" * 70)

    if peer_evidence.empty:

        print(
            "No significant peer deviations."
        )

    else:

        print(
            f"Total findings: "
            f"{len(peer_evidence)}"
        )

        print(
            peer_evidence[
                [
                    "metric",
                    "metric_value",
                    "peer_average",
                    "deviation_threshold",
                    "deviation_ratio",
                    "reason",
                ]
            ].to_string(
                index=False
            )
        )

    # ---------------------------------------------------------
    # Operational Pattern Evidence
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("4. OPERATIONAL PATTERN EVIDENCE")
    print("-" * 70)

    if operational_evidence.empty:

        print(
            "No significant operational patterns detected."
        )

    else:

        print(
            f"Total findings: "
            f"{len(operational_evidence)}"
        )

        print(
            operational_evidence[
                [
                    "signal_type",
                    "affected_cases",
                    "metric_value",
                    "reason",
                    "recommended_action",
                ]
            ].to_string(
                index=False
            )
        )

    # ---------------------------------------------------------
    # Key Signals
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("5. KEY SUPERVISORY SIGNALS")
    print("-" * 70)

    key_signals_found = False

    # -----------------------------------------------------
    # Repeated weak investigations
    # -----------------------------------------------------

    repeated_weak = operational_evidence[
        operational_evidence["signal_type"]
        == "Repetitive Weak Investigation Pattern"
    ]

    if not repeated_weak.empty:

        key_signals_found = True

        total_cases = int(
            repeated_weak[
                "affected_cases"
            ].sum()
        )

        print(
            f"• Repeated weak investigations: "
            f"{total_cases} affected cases"
        )

    # -----------------------------------------------------
    # Rapid closure pattern
    # -----------------------------------------------------

    rapid_closure = operational_evidence[
        operational_evidence["signal_type"]
        == "Possible Metric-Driven Rapid Closure"
    ]

    if not rapid_closure.empty:

        key_signals_found = True

        for _, row in rapid_closure.iterrows():

            print(
                f"• Rapid High/Critical closures: "
                f"{int(row['affected_cases'])} cases; "
                f"average closure time "
                f"{row['metric_value']:.1f} hours"
            )

    # -----------------------------------------------------
    # Low investigation effort
    # -----------------------------------------------------

    low_effort = operational_evidence[
        operational_evidence["signal_type"]
        == "Low Investigation Effort Outlier"
    ]

    if not low_effort.empty:

        key_signals_found = True

        for _, row in low_effort.iterrows():

            print(
                f"• Low investigation effort: "
                f"{int(row['affected_cases'])} cases; "
                f"average investigation duration "
                f"{row['metric_value']:.1f} minutes"
            )

    # -----------------------------------------------------
    # Peer deviations
    # -----------------------------------------------------

    if not peer_evidence.empty:

        key_signals_found = True

        for _, row in peer_evidence.iterrows():

            print(
                f"• Peer deviation: "
                f"{row['metric']} = "
                f"{row['metric_value']:.2f}%"
                )

    # -----------------------------------------------------
    # Negative space
    # -----------------------------------------------------

    if not negative_space_evidence.empty:

        key_signals_found = True

        for _, row in negative_space_evidence.iterrows():

            print(
                f"• Potential monitoring blind spot: "
                f"{row['asset_name']} "
                f"({row['coverage_percent']:.1f}% coverage)"
            )

    if not key_signals_found:

        print(
            "• No major supervisory signals detected."
        )

    # ---------------------------------------------------------
    # Supervisory Review Guidance
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("6. SUPERVISORY REVIEW GUIDANCE")
    print("-" * 70)

    print(
        "→ Review representative cases associated "
        "with the flagged patterns."
    )

    print(
        "→ Examine investigation evidence, recorded "
        "steps, root-cause analysis and remediation."
    )

    print(
        "→ Review escalation decisions for relevant "
        "High/Critical cases."
    )

    print(
        "→ Examine assets associated with potential "
        "negative-space conditions."
    )

    print(
        "→ Compare relevant operational metrics with "
        "available peer assessments."
    )

    print(
        "→ Use supervisory judgment before reaching "
        "any final conclusion."
    )

    # ---------------------------------------------------------
    # Final Disclaimer
    # ---------------------------------------------------------

    print("\n" + "=" * 70)

    print(
        "IMPORTANT: SAT-SA identifies evidence and "
        "potential supervisory concerns."
    )

    print(
        "It does not make a final compliance or "
        "risk judgment."
    )

    print("=" * 70)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    # Demonstration assessment.
    # Later the dashboard will allow the supervisor
    # to select an assessment dynamically.

    display_explanation(
        "A-006"
    )


if __name__ == "__main__":

    main()

