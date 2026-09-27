import pandas as pd

from src.features.feature_engineering import (
    build_feature_dataset
)


# ---------------------------------------------------------
# Execution Gap Engine
# ---------------------------------------------------------

def detect_execution_gaps(case_features):

    findings = []

    # -----------------------------------------------------
    # Signal 1:
    # Rapid closure + weak investigation
    # -----------------------------------------------------

    rapid_weak = case_features[
        (
            case_features["is_high_critical"]
        )
        &
        (
            case_features["is_closed"]
        )
        &
        (
            case_features["closure_hours"] <= 8
        )
        &
        (
            case_features["weak_investigation"]
        )
    ]

    for _, case in rapid_weak.iterrows():

        findings.append({
            "case_id": case["case_id"],
            "assessment_id": case["assessment_id"],
            "signal_type":
                "Rapid Closure + Weak Investigation",
            "priority": case["priority"],
            "closure_hours":
                case["closure_hours"],
            "evidence_count":
                case["evidence_count"],
            "steps_recorded":
                case["steps_recorded"],
            "root_cause_identified":
                case["root_cause_identified"],
            "remediation_recorded":
                case["remediation_recorded"],
            "reason":
                "High/Critical case was closed rapidly "
                "with limited investigation evidence.",
            "recommended_action":
                "Prioritize case for manual supervisory review."
        })


    # -----------------------------------------------------
    # Signal 2:
    # Critical case closed without escalation
    # -----------------------------------------------------

    critical_no_escalation = case_features[
        (
            case_features["priority"] == "Critical"
        )
        &
        (
            case_features["is_closed"]
        )
        &
        (
            ~case_features["was_escalated"]
        )
    ]

    for _, case in critical_no_escalation.iterrows():

        findings.append({
            "case_id": case["case_id"],
            "assessment_id": case["assessment_id"],
            "signal_type":
                "Critical Case Closed Without Escalation",
            "priority": case["priority"],
            "closure_hours":
                case["closure_hours"],
            "evidence_count":
                case["evidence_count"],
            "steps_recorded":
                case["steps_recorded"],
            "root_cause_identified":
                case["root_cause_identified"],
            "remediation_recorded":
                case["remediation_recorded"],
            "reason":
                "Critical case was closed without "
                "a recorded escalation.",
            "recommended_action":
                "Review escalation decision and supporting evidence."
        })


    # -----------------------------------------------------
    # Signal 3:
    # High/Critical case with weak investigation
    # -----------------------------------------------------

    weak_high_critical = case_features[
        (
            case_features["is_high_critical"]
        )
        &
        (
            case_features["weak_investigation"]
        )
    ]

    for _, case in weak_high_critical.iterrows():

        findings.append({
            "case_id": case["case_id"],
            "assessment_id": case["assessment_id"],
            "signal_type":
                "Weak Investigation",
            "priority": case["priority"],
            "closure_hours":
                case["closure_hours"],
            "evidence_count":
                case["evidence_count"],
            "steps_recorded":
                case["steps_recorded"],
            "root_cause_identified":
                case["root_cause_identified"],
            "remediation_recorded":
                case["remediation_recorded"],
            "reason":
                "High/Critical case has limited "
                "investigation evidence.",
            "recommended_action":
                "Prioritize representative investigation "
                "records for manual review."
        })


    return pd.DataFrame(findings)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    (
        alerts,
        case_features,
        monitoring
    ) = build_feature_dataset()

    findings = detect_execution_gaps(
        case_features
    )

    print("\n==========================================")
    print("SAT-SA EXECUTION GAP ENGINE")
    print("==========================================")

    print(
        "\nTotal findings:",
        len(findings)
    )

    if not findings.empty:

        print("\nSignal distribution:")

        print(
            findings[
                "signal_type"
            ].value_counts()
        )

        print("\nSample findings:")

        print(
            findings[
                [
                    "case_id",
                    "assessment_id",
                    "signal_type",
                    "priority",
                    "closure_hours",
                    "reason"
                ]
            ]
            .head(15)
            .to_string(index=False)
        )

    else:

        print(
            "\nNo execution-gap signals detected."
        )